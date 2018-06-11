import os.path
import sys
import time
import hashlib
from shared import common
from shared import database


def run():
    
    db = database.DbTool()
    db.open()
    
    rows = db.get_pstitems()    
    count = 0
    total = len(rows)
    for r in rows:
        item_id = r[0]
        psttype = r[1]

        if count % 1000 == 0:
            print "Processing pstitem {0} of {1} [item_id {2}]".format(count, total, item_id)
            db.commit()
        count += 1
        
        #process emails and attachments separately; attachments are processed as fileitems
        if psttype != common.PSTTYPE_ATTACHMENT and psttype != common.PSTTYPE_NOTE: 

            all_text = []

            ips = db.get_itemproperties_by_item(item_id)
            for ip in ips:
                prop_id    = ip[0]
                prop_value = ip[1]

                all_text.append(str(prop_id))
                all_text.append(' : ')
                all_text.append(str(prop_value))
                all_text.append('\n')

            md5sum = hashlib.md5(''.join(all_text)).hexdigest()

            db.create_data_dedup_nonemailpst(item_id, md5sum)

    db.commit()
    db.close()
