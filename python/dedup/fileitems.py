import os.path
import sys
import time
from shared import common
from shared import database


def run():
    timer_start = time.time()

    md5 = {}

    rootpath = common.get_path_files_processed()
    count = 1
    total = len(os.listdir(rootpath))

    db = database.DbTool()
    db.open()
    
    for d in os.listdir(rootpath):
        print "[fi] Processing source {0} of {1} [dir {2}]".format(count, total, d)
        count += 1
                
        d_path = os.path.join(rootpath, d, "*")
        
        cmd = "md5sum {0}".format(d_path);
        result = common.exec_cmd(cmd)

        lines = result[0].split("\n")
        for line in lines:
            if len(line) > 0:
                data = line.split()
                checksum = data[0]
                filepath = data[1]
                head, tail = os.path.split(filepath)
                item_id, ext = os.path.splitext(tail)

                if checksum in md5:
                    canon_id = md5[checksum]
                    db.create_item_relationship(item_id, common.IS_DUPLICATE_RELTYPE_ID, canon_id, "md5sum")
                else:
                    md5[checksum] = item_id
        
        db.commit() #commit for each source

    db.close()
    print common.display_elapsed(timer_start, "STEP COMPLETED: dedup fileitems")
