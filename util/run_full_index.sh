#!/bin/bash

# This script written by William Webber.

# Run a full indexing of a PST collection.
#
# NOTE: this will drop any existing databases and begin the full
# extraction process from scratch!
#
# Prerequisites: 
#
# 1. Must be run from the directory above the current directory.
# 2. The file python/shared/config.py must contain the correct
#       database information, and be expressed in a way that is
#       source'able by bash (e.g. no spaces around '=').
# 3. The user DB_USER in config.py must exist and have permissions 
#       to create the database DB_NAME in mysql.  Do something like:
#
#           create user '<DB_USER>'@'localhost' identified by '<DB_PASSWORD>'
#           grant all privileges on <DB_NAME>.* to '<DB_USER>'@'localhost'.

error() {
    echo $* 1>&2
    exit 1
}

USAGE="$0 <pst-directory>"

CONFIG="python/config.properties"

MYSQL_JAR=lib/mysql-connector-java.jar
TIKA_JAR=lib/tika-app.jar

if [ ! -f $MYSQL_JAR -o ! -f $TIKA_JAR ]
then
    error "Missing necessary JARs"
fi

CLASSPATH="$CLASSPATH:$MYSQL_JAR:$TIKA_JAR"
export CLASSPATH

if [ $# -ne 1 ]
then
    error "$USAGE"
fi

pstdir=$1

if [ ! -d $pstdir ]
then
    error "Directory '$pstdir' does not exist or is not a directory"
fi

if [ ! -f $CONFIG ]
then
    error "Configuration files '$CONFIG' does not exist"
fi

source $CONFIG || error "Error sourcing '$CONFIG'"

if [ -z "$DB_USER" -o -z "$DB_PASSWORD" -o -z "$DB_NAME" -o -z "$OUTPUT_ROOT" ]
then
    error "Expected database variables not read from $CONFIG"
fi

run_mysql_nodb() {
    mysql -u $DB_USER --password=$DB_PASSWORD
}

run_mysql() {
    mysql -u $DB_USER --password=$DB_PASSWORD $DB_NAME
}

echo ">> Resetting file output directory"

if [ -d $OUTPUT_ROOT ]
then
    chmod -R u+w $OUTPUT_ROOT
    rm -rf $OUTPUT_ROOT
fi

mkdir $OUTPUT_ROOT

echo ">> Recreating database '$DB_NAME'"

echo "DROP DATABASE IF EXISTS $DB_NAME" | run_mysql_nodb
echo "CREATE DATABASE $DB_NAME" | run_mysql_nodb

echo ">> Setting up database"

run_mysql < sql/setup.sql
run_mysql < sql/load_data.sql
run_mysql < sql/sprocs.sql

run_python() {
    echo ">> $(date +"%T"): Running '$*'"
    python $* || error "*** ERROR: '$*' failed"
    echo ">> $(date +"%T"): Finished '$*'"
}

run_python python/pst_extract.py $pstdir
run_python python/mimetype_detect.py
run_python python/containers_extract.py
run_python python/id_loader.py
run_python python/find_threads.py
run_python python/dedup_all.py
run_python python/tika_extract.py
run_python python/origin_loader.py

echo ">> $(date +"%T"): adding foreign keys and indexes"

run_mysql < sql/add_fk.sql
run_mysql < sql/add_indexes.sql

run_python python/itemdata_loader.py
run_python python/redact.py

echo ">> $(date +"%T"): adding full-text indexes"

run_mysql < sql/add_fulltext_indexes.sql

echo ">> $(date +"%T"): adding dataitems"

run_mysql < sql/load_dataitems.sql

echo ">> $(date +"%T"): creating distro view"

run_mysql < sql/distro_view.sql

echo ">> DONE: now extract distro"

