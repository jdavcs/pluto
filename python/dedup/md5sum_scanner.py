import os.path
import sys
import time
from shared import common
from shared import database


def run():
    md5 = {}

    db = database.DbTool()
    db.open()

    fileitems = db.get_md5sums()
    total = len(fileitems)
    count = 0
    for r in fileitems:
        item_id   = r[0]
        md5sum = r[1]

        if count % 1000 == 0:
            print 'Processing item {0} of {1} [id# {2}]'.format(count, total, item_id)
            db.commit()
        count += 1
        
        if md5sum in md5:
            primary_id = md5[md5sum]
            db.create_item_relationship(item_id, common.IS_DUPLICATE_RELTYPE_ID, primary_id, "md5sum-2")
        else:
            md5[md5sum] = item_id

    db.commit();
    db.close()
