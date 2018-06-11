import os.path
import sys
import time
from shared import config
from shared import common
from shared import database
from shared import mimetype_detector as mdet
from pst_tree_reader import PstTreeReader

BATCH = 1


"""Required arguments: input_path to directory with 1+ pst files, each representing a source/custodian.
   All files must be pst files.
   NOTE: RUNNING THIS CODE WILL ERASE YOUR OUTPUT DIRECTORY specified in your config.properties file.
""" 
def run():
    timer_start = time.time()
    
    db = database.DbTool()
    db.open()

    _validate_input(db)

    _create_output_dirs()

    path_in = sys.argv[1]
    _extract_sources(db, path_in)
    
    db.commit() #final commit (cleanup)
    db.close()

    print common.display_elapsed(timer_start, "extract sources/top-level pst files")


def _extract_sources(db, path_in):
    total = len(os.listdir(path_in))
    counter = 1

    for f in os.listdir(path_in): # loop through pst files
        print "Processing source {0} of {1}: {2}".format(counter, total, f)
        counter += 1

        f_path = os.path.join(path_in, f)
        size = os.path.getsize(f_path)

        source_id = db.create_source(f, size) # store source in db

        path_out = common.get_path_files_processed_source(source_id)
        if not os.path.exists(path_out):
            os.mkdir(path_out) # create dir for extracted files from pst file      

        store_folders = 1 #we ignore pstfolders in attachment-pst files
        reader = PstTreeReader(db, source_id, None, 0, f_path, path_out, store_folders, BATCH)
        reader.read()

        db.commit() #commit for each source


def _create_output_dirs():

    cnf = config.ConfigReader()
    outputRoot = cnf.get('OUTPUT_ROOT')

    #this wipes out the contents of the output directory
    if os.path.exists(outputRoot):
        cmd = "chmod -R 777 {0}/*".format(outputRoot) #chmod to make them removable
        common.exec_cmd(cmd)
        
        cmd = "rm {0}/* -rf".format(outputRoot) #remove
        common.exec_cmd(cmd)
   

    path_files = "{0}files/".format(outputRoot)
    if not os.path.exists(path_files):
        os.mkdir(path_files)
    
    path_files_orig = "{0}files/original_by_container/".format(outputRoot)
    if not os.path.exists(path_files_orig):
        os.mkdir(path_files_orig)
    
    path_files_proc = "{0}files/processed/".format(outputRoot)
    if not os.path.exists(path_files_proc):
        os.mkdir(path_files_proc)
    
    path_files_text = "{0}files/text/".format(outputRoot)
    if not os.path.exists(path_files_text):
        os.mkdir(path_files_text)
    
    path_pst = "{0}pstitems/".format(outputRoot)
    if not os.path.exists(path_pst):
        os.mkdir(path_pst)
    
    path_pst_text = "{0}pstitems/text/".format(outputRoot)
    if not os.path.exists(path_pst_text):
        os.mkdir(path_pst_text)

    path_tikalogs = "{0}{1}/".format(outputRoot, cnf.get('TIKA_LOG_RELPATH'))
    if not os.path.exists(path_tikalogs):
        os.mkdir(path_tikalogs)


def _validate_input(db):
    #validate: # of arguments
    if len(sys.argv) != 2:
        print "ERROR: input_path missing"
        sys.exit()
        
    #validate: source files format
    in_path = sys.argv[1]
    mdetect = mdet.MimetypeDetector(db)
    for f in os.listdir(in_path):
        f_path = os.path.join(in_path, f)
        if not os.path.isfile(f_path):
            print "ERROR: found directory instead of file:", f_path
            sys.exit()

        mime_details = mdetect.get_mimetype_data(f_path)[2]
        if not common.MIME_PATTERN_PST in mime_details:
            print "ERROR: found non-pst file at top level:", f_path
            print "  detected type: ", mime_details
            sys.exit()
