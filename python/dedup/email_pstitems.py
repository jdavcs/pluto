import os.path
import sys
import time
from shared import common
from shared import database
from shared import property


def run():
    duplicates = 0
    messageids = {}
    itemids = set()
    
    db = database.DbTool()
    db.open()

    property_id = property.PST_MESSAGEID_ID
    
    ip = db.get_itemproperties_by_property(property_id)
    count = 0
    total = len(ip)

    for r in ip:
        item_id = r[0]

        if not item_id in itemids: #ignore duplicate item_ids!
            itemids.add(item_id)

            value = str(r[1]).strip()

            if count % 100 == 0:
                print "[epi] Processing pstitem {0} of {1} [item_id {2}]".format(count, total, item_id)            
            count += 1 

            if value in messageids:
                canon_id = messageids[value]
                db.create_item_relationship(item_id, common.IS_DUPLICATE_RELTYPE_ID, canon_id, "messageid-2")
                duplicates += 1
            else:
                messageids[value] = item_id

    db.commit()
    db.close()
