import os.path
import shutil
from shared import common
from shared import database
from pst import pst_tree_reader


def extract(db, citem, batch):
    item_id = citem[0]
    source_id = citem[1]
    level = citem[2]
    type_id = citem[3]
    extension = citem[4]
        
    path_in_f = "{0}{1}".format(item_id, extension)
    path_in_dir = common.get_path_files_processed_source(source_id)
    path_in = os.path.join(path_in_dir, path_in_f) # path to container file

    if type_id == common.CONTAINERTYPE_PST:
        process_pst(db, path_in, item_id, source_id, level, extension, path_in_dir, batch)
    else:
        process_non_pst(db, path_in, item_id, source_id, level, type_id, extension, path_in_dir)

    db.commit() #MUST commit for each container


def process_pst(db, path_in, item_id, source_id, level, extension, path_dir_in, batch):
    parent_item_id = item_id
    level = level + 1
    path_out = path_dir_in
    store_folders =0

    #extract pst file; all items will be stored in the database
    reader = pst_tree_reader.PstTreeReader(db, source_id, parent_item_id, level, path_in, path_out, store_folders, batch)
    reader.read()

    db.commit() #added this: otherwise the next statement will not find any children

    children = db.get_pstitems_by_parent(item_id)
    if len(children) > 0:
        db.update_container(item_id, 1)   # mark as extracted
    else:
        db.update_container(item_id, 0)   # mark as NOT extracted


def process_non_pst(db, path_in, item_id, source_id, level, type_id, extension, path_in_dir):
    path_out = common.get_path_files_original_container(item_id) # path for extracted files
    os.mkdir(path_out)

    _extract_files(type_id, path_in, path_out)

    # change permissions for further program execution
    cmd = "chmod 770 -R {0}".format(path_out)
    result = common.exec_cmd(cmd)

    # check if any files were extracted
    extracted_files = 0
    for root, dirs, files in os.walk(path_out):
        extracted_files += len(files)

    if extracted_files == 0:
        db.update_container(item_id, 0)   # mark as NOT extracted
        os.rmdir(path_out)           # remove container directory
    else:
        db.update_container(item_id, 1)   # mark as extracted            
        source_dir = path_out       # dir with extracted files
        target_dir = path_in_dir    # dir for processed files
        _process_non_pst_extracted(db, item_id, source_id, level+1, source_dir, target_dir) # add to db and copy to output location 

    # set permissions for extracted files
# 02/01/13: not essential; interferes with removing files on next run.
#    cmd = "find {0}* -type f -print0 | xargs -0 chmod 440".format(path_out)
#    common.exec_cmd(cmd)
#    cmd = "find {0}* -type d -print0 | xargs -0 chmod 550".format(path_out)
#    common.exec_cmd(cmd)


def _extract_files(type, path_in, path_out):
    if type == common.CONTAINERTYPE_ZIP:
        _extract_zip(path_in, path_out)
    elif type == common.CONTAINERTYPE_GZIP:
        _extract_gzip(path_in, path_out)
    elif type == common.CONTAINERTYPE_TAR:
        _extract_tar(path_in, path_out)
    elif type == common.CONTAINERTYPE_JAR:
        _extract_jar(path_in, path_out)


def _extract_zip(path_in, path_out):
    _extract_zipjar(path_in, path_out)


def _extract_gzip(path_in, path_out):    
    root, file = os.path.split(path_in) 
    filename, ext = os.path.splitext(file)
    path_out_file = os.path.join(path_out, filename)

    cmd = """gunzip -c {0} > {1}""".format(path_in, path_out_file)
    result = common.exec_cmd(cmd)
    if result[1] is not None and result[1] != "":
        print "ERROR: container-extraction-1: " + result[1]

def _extract_tar(path_in, path_out):
    pass
    cmd = """tar -xf {0} -C {1}""".format(path_in, path_out)
    result = common.exec_cmd(cmd)
    if result[1] is not None and result[1] != "":
        print "ERROR: container-extraction-2: " + result[1]

def _extract_jar(path_in, path_out):
    _extract_zipjar(path_in, path_out)


def _extract_zipjar(path_in, path_out):
    message = "No errors detected"
    cmd_test = """unzip -qtP '' {0}""".format(path_in)
    result_test = common.exec_cmd(cmd_test)

    if result_test[1] is not None and result_test[1] != "":
        print "ERROR: container-extraction-3: " + result_test[1]

    if result_test[0].startswith(message):
        cmd = """unzip -q {0} -d {1}""".format(path_in, path_out)
        result = common.exec_cmd(cmd)

        if result[1] is not None and result[1] != "":
            print "ERROR: container-extraction-4: " + result[1]


def _process_non_pst_extracted(db, parent_item_id, source_id, level, path_in, path_out):
    for root_path, dirs, files in os.walk(path_in):
        for f in files: # loop through extracted files
            f_path_in = os.path.join(root_path, f)
            filesize = os.path.getsize(f_path_in)
            original_name, extension = os.path.splitext(f)

            #if has extension: rename original to lowercase extension
            if extension is not None and len(extension) > 0:
                extension = extension.lower()
                new_filename = original_name + extension
                new_f_path_in = os.path.join(root_path, new_filename)            
                os.rename(f_path_in, new_f_path_in)
                f_path_in = new_f_path_in
            
            #create db item + fileitem
            item_id = db.create_item(source_id, parent_item_id, level)            
            db.create_fileitem(item_id, original_name, extension, filesize, -1)        

            #store file in output/
            filename_out = "{0}{1}".format(item_id, extension)
            f_path_out = os.path.join(path_out, filename_out)
            shutil.copyfile(f_path_in, f_path_out)
