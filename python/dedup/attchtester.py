import os.path
import sys
import time
import hashlib
from shared import common
from shared import database


class AttchTester(object):

    def __init__(self):
        pass
    
    def run(self):
        db = database.DbTool()
        db.open()  

        duplicates = db.get_records("select item1_id, item2_id from item_relationship where reltype_id = 3")
        count = 0
        total = len(duplicates)
        for d in duplicates:
            dupl_id = d[0]
            orig_id = d[1]

            if count % 1000 == 0:
                print "Processing {0} of {1} [item_id {2}]".format(count, total, dupl_id)
            count += 1

            attch_dupl = self._get_attachment_hashes(dupl_id, db)
            attch_orig = self._get_attachment_hashes(orig_id, db)

            if len(attch_dupl) != len(attch_orig):
                raise Exception(str(dupl_id) + " --- " + str(orig_id))

        db.close()

    def _get_attachment_hashes(self, parent_id, db):
        sql = """SELECT d.item_id, d.file_md5sum 
            FROM item i INNER JOIN data_dedup d ON d.item_id = i.id 
            AND i.parent_id = """ + str(parent_id)
        return db.get_records(sql)
