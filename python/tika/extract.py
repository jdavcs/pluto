import os.path
import sys
import time
from shared import common
from shared import config
from shared import database

from multiprocessing import Pool
import itertools

BATCH = 3
PARALLEL_PROC = 6


# Loops through sources directories, calls java for each directory 
#   and uses tika to extract text (write to file) and meta data (write to db),
def run():
    timer_start = time.time()

    rootpath_in = common.get_path_files_processed()
    path_out = common.get_path_files_text()
    log_filename = "paths-" + str(BATCH) + ".log"
    path_log = os.path.join(common.get_path_tikalogs(), log_filename)
    path_firstpathlog = path_log + "-1"

    process_sources(rootpath_in, path_out, BATCH, path_firstpathlog) #initial run: extract all you can, record errors
    process_errorlog(path_out, BATCH, path_log) #recursively process paths for missed files (java io error)
    store_text(path_out) #store extracted text in db

    print common.display_elapsed(timer_start, "tika extract meta data and text")


def process_dir(d, rootpath_in, path_out, BATCH, path_pathlog):
    cnf = config.ConfigReader()
    path_in = os.path.join(rootpath_in, d)
    print "From %s to %s" % (path_in, path_out)
    cmd = "java -cp {0} pluto.TikaExtractor {1} {2} 1 {3} {4} {5}".format(
            cnf.get('JAVA_CLASSPATH'), path_in, path_out, BATCH, path_pathlog, common.CONFIG_FILE_NAME)
    print cmd
    result = common.exec_cmd(cmd)
    
    if len(result[1]) > 0: #we only print out errors in execution; the rest is logged in the java file
        print "\nERRORS FROM JVM EXECUTION from dir {0}:".format(d)
        print "{0}\n".format(result[1])


def process_dir_star(args):
    process_dir(*args)


# Now is multi-processed
def process_sources(rootpath_in, path_out, BATCH, path_pathlog):
    cnf = config.ConfigReader()    
    count = 1
    total = len(os.listdir(rootpath_in))

    dirs = os.listdir(rootpath_in)
    p = Pool(PARALLEL_PROC)

    pool_args = itertools.izip(dirs, itertools.repeat(rootpath_in),
            itertools.repeat(path_out), itertools.repeat(BATCH),
            itertools.repeat(path_pathlog))

    p.map(process_dir_star, pool_args)

    for d in os.listdir(rootpath_in):
        print "Processing source {0} of {1} [dir {2}]".format(count, total, d)
        count += 1

        path_in = os.path.join(rootpath_in, d)
        print "From %s to %s" % (path_in, path_out)
        #cmd = "java -cp {0} pluto.TikaExtractor {1} {2} 1 {3} {4}".format(self._cnf.JAVA_CLASSPATH, path_in, path_out, BATCH, path_pathlog)

        cmd = "java -cp {0} pluto.TikaExtractor {1} {2} 1 {3} {4} {5}".format(
            cnf.get('JAVA_CLASSPATH'), path_in, path_out, BATCH, path_pathlog, common.CONFIG_FILE_NAME)

        result = common.exec_cmd(cmd)
        
        if len(result[1]) > 0: #we only print out errors in execution; the rest is logged in the java file
            print "\nERRORS FROM JVM EXECUTION from dir {0}:".format(d)
            print "{0}\n".format(result[1])


def process_errorlog(path_out, BATCH, path_log):
    cnf = config.ConfigReader()    
    max = 20
    iteration = 1
    while True:
        path_thislog = path_log + "-" + str(iteration)
        # continue only if current log exists (i.e. new log file has been created at previous iteration) or you iterations < max
        if not os.path.exists(path_thislog) or iteration > max: break
        
        print "PROCESSING iteration " + str(iteration)
        iteration += 1
        path_nextlog = path_log + "-" + str(iteration)

        cmd = "java -cp {0} pluto.TikaExtractor {1} {2} 2 {3} {4} {5}".format(
                cnf.get('JAVA_CLASSPATH'), path_thislog, path_out, BATCH, path_nextlog, common.CONFIG_FILE_NAME)
        result = common.exec_cmd(cmd)

        if len(result[0]) > 0: 
            print "\nRESULTS OF JVM EXECUTION"
            print "{0}\n".format(result[0])
        
        if len(result[1]) > 0: #we only print out errors in execution; the rest is logged in the java file
            print "\nERRORS FROM JVM EXECUTION"
            print "{0}\n".format(result[1])

    print "COMPLETED at iteration " + str(iteration -1 )


def store_text(path):
    cnf = config.ConfigReader()    
    p_type = common.PROPERTYTYPE_FILEITEM
    p_name = cnf.get('EXTRACTED_TEXT_PROPERTY_NAME')

    db = database.DbTool()
    db.open()

    property_id = db.get_property_id(p_type, p_name)
    
    total = len(os.listdir(path))
    count = 1

    for f in os.listdir(path):
        if count % 100 == 0:
            print "Processing file {0} of {1} [{2}]".format(count, total, f)
            db.commit() #commit every 100: extracted texts can be large
        count += 1

        f_path = os.path.join(path, f)
        if os.path.getsize(f_path) > 0:
            item_id = int(f)
            file = open(f_path)
            value = file.read()
            file.close()
            db.create_item_property(item_id, property_id, value, BATCH)

    db.commit()
    db.close()
