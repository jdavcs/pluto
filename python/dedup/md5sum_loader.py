import os.path
import sys
import time
from shared import common
from shared import database


def run():

    rootpath = common.get_path_files_processed()
    
    db = database.DbTool()
    db.open()

    fileitems = db.get_fileitems()
    total = len(fileitems)
    count = 0
    for r in fileitems:
        item_id   = r[0]
        source_id = r[1]
        extension = r[2]

        if count % 1000 == 0:
            print 'Processing item {0} of {1} [id# {2}]'.format(count, total, item_id)
            db.commit()
        count += 1

        f_path = os.path.join(rootpath, str(source_id), str(item_id) + extension)
        
        cmd = "md5sum \"{0}\"".format(f_path);
        result = common.exec_cmd(cmd)
        data = result[0].split()
        checksum = data[0]

        db.update_file_md5sum(item_id, checksum)

    db.commit();
    db.close()
