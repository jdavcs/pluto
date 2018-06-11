import os.path
import sys
import time
import hashlib
from shared import common
from shared import database


class HashTester(object):

    def __init__(self):
        db = database.DbTool()
        db.open()  
        self._load_hashes(db)
        self._load_duplicates(db)
        db.close()

    def _load_hashes(self, db):
        self._hash_dict = {}
        sql = """SELECT 
            h.item_id, 
            h.hash_D, 
            h.hash_F, 
            h.hash_FD, 
            h.hash_B, 
            h.hash_BD, 
            h.hash_BF, 
            h.hash_BFD, 
            h.hash_M, 
            h.hash_MD, 
            h.hash_MF, 
            h.hash_MFD, 
            h.hash_MB, 
            h.hash_MBD, 
            h.hash_MBF, 
            h.hash_MBFD 
            from data_dedup_hash h""" 
        hash_rows = db.get_records(sql)
        for hr in hash_rows:
            item_id = hr[0]
            self._hash_dict[item_id] = hr

    def _load_duplicates(self, db):
        self._duplicates = db.get_records("select item1_id, item2_id from item_relationship where reltype_id = 1 and value = 'messageid'")

    def run(self):
        db = database.DbTool()
        db.open()  

        reltype_id = 3 #is duplicate of by MDB
        
        count = 0
        total = len(self._duplicates)
        for d in self._duplicates:
            dupl_id = d[0]
            orig_id = d[1]

            dupl_hash_B = self._get_hash(dupl_id, 4)
            orig_hash_B = self._get_hash(orig_id, 4)

            dupl_hash_D = self._get_hash(dupl_id, 1)
            orig_hash_D = self._get_hash(orig_id, 1)

            if dupl_hash_D == orig_hash_D and dupl_hash_B == orig_hash_B:
                db.create_item_relationship(dupl_id, reltype_id, orig_id, 'MDB')


            if count % 100 == 0:
                print "Processing {0} of {1} [item_id {2}]".format(count, total, dupl_id)
                db.commit()
            count += 1

        db.commit()
        db.close()

    def _get_hash(self, item_id, position):
        hashrow = self._hash_dict[item_id]
        return hashrow[position]
