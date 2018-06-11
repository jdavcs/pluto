import sys
from shared import common
from shared import database


def run():
    file_dict = {}
    pst_dict = {}
    email_dict = {}
    
    db = database.DbTool()
    db.open()
    
    rows = db.get_dedup_data() 
    count = 0
    total = len(rows)
    for r in rows:
        item_id       = r[0]
        file_checksum = r[1]
        pst_checksum  = r[2]
        pst_messageid = r[3]

        if count % 1000 == 0:
            print "Processing item {0} of {1} [item_id {2}]".format(count, total, item_id)
            db.commit()
        count += 1

        if file_checksum is not None:
            process_item(item_id, file_checksum, file_dict, "md5sum-file", db)
        elif pst_checksum is not None:
            process_item(item_id, pst_checksum, pst_dict, "md5sum-pst", db)
        elif pst_messageid is not None:
            process_item(item_id, pst_messageid, email_dict, "messageid", db)

    db.commit()
    db.close()


def process_item(item_id, value, dict, duplicate_type, db):
    if value in dict:
        primary_id = dict[value]
    #    print "creating: " + str(item_id) + " is duplicate of " + str(primary_id) + " by " + duplicate_type
        db.create_item_relationship(item_id, common.IS_DUPLICATE_RELTYPE_ID, primary_id, duplicate_type)
    else:
        dict[value] = item_id
