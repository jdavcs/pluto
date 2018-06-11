## Requirements

Two JAR files are required: tika and mysql-connector java.

The `mysql-connector-java` file is here. The tika JAR file
can be downloaded using the `get_tika_jar.sh` script (it is
quite large).

The utility script `util/run_fill_index.py` expects there to be
two JAR files:

```
lib/mysql-connector-java.jar
lib/tika-app.jar
```

Symbolic links from these locations to the actual JAR files
should be created, e.g.:

```bash
cd lib
ln -s mysql-connector-java-5.1.22-bin.jar mysql-connector-java.jar
ln -s tika-app-1.1.jar tika-app.jar
```
