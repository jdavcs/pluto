import os.path
import sys
import time
from shared import common
from shared import database

def main():
    timer_start = time.time()

    mid_dict = {} #dictionary: key = messageid, value = item_id
    repl_dict = {}  #dictionary: key = item_id-reply, value = item_id-original
    
    db = database.DbTool()
    db.open()

    mid_property_id = db.get_property_id(common.PROPERTYTYPE_PSTITEM_NOTE, "messageid")
    mids = db.get_itemproperties_by_property(mid_property_id)

    total = len(mids)
    count = 1
    for ip in mids:
        item_id = ip[0]
        messageid = str(ip[1]).strip() #ignore value_text - none there
        mid_dict[messageid] = item_id

        if count % 100 == 0:
            print "Processing item-property {0} of {1} [item_id {2}]".format(count, total, item_id)            
        count += 1 

    irt_property_id = db.get_property_id(common.PROPERTYTYPE_PSTITEM_NOTE, "in_reply_to")
    irts = db.get_itemproperties_by_property(irt_property_id)

    for ip in irts:
        item_id = ip[0]
        inreplyto = str(ip[1]).strip() #ignore value_text - none there

        if inreplyto in mid_dict:
            repl_dict[item_id] = mid_dict[inreplyto]

    count = 1
    total = len(repl_dict)
    for repl in repl_dict:
        if count % 100 == 0:
            print "Storing reply {0} of {1} [item_ids: {2}, {3}]".format(count, total, item1_id, item2_id) 
        count += 1 
        
        item1_id = repl
        item2_id = repl_dict[repl]
        db.create_item_relationship(item1_id, common.IS_REPLYTO_RELTYPE_ID, item2_id, "by messageid")

    print "found {0} replies".format(len(repl_dict))

    db.commit()
    db.close()

    print common.display_elapsed(timer_start, "threading email")


if __name__ == '__main__': main()
