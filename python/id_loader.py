import os.path
import sys
import time
from shared import common
from shared import database


def main():
    db = database.DbTool()
    db.open()

    slist = db.get_source_list() # source list
    s_count = 0
    s_total = len(slist)
    for s in slist:
        s_count += 1

        source_id = s[0]

        children = {} #key = parent_id; val = list of children ids
        psttypes = {}
        top_item_ids = []
    
        ilist = db.get_items_by_source(source_id) # item list

        i_count = 1
        i_total = len(ilist)
        for i in ilist: 
            if (i_count % 10 == 0):
               print "\t/* Processing item {0} of {1} / source {2} of {3} */".format(i_count, i_total, s_count, s_total)
            i_count += 1

            item_id = i[0]
            parent_id = i[1]
            psttype_id = i[2]

            psttypes[item_id] = psttype_id

            if parent_id is None:
                top_item_ids.append(item_id) #found top-level item!
            else: 

                if parent_id in children:            # if child list exists - fetch it!
                    child_list = children[parent_id] 
                else:                               # otherwise - create and load it!
                    child_list = []
                    children[parent_id] = child_list

                child_list.append(item_id)          # append child to list

        prefix = "{0}-".format(str(source_id).zfill(4))
        process_items(db, psttypes, children, top_item_ids, prefix, 6)

        db.commit() # commit for each source

    db.commit() 
    db.close()


def get_suffix(psttype):
    if psttype == common.PSTTYPE_NOTE:
        return "EM"
    elif psttype == common.PSTTYPE_SCHEDULE:
        return "SC"
    elif psttype == common.PSTTYPE_APPOINTMENT:
        return "AP"
    elif psttype == common.PSTTYPE_CONTACT:
        return "CN"
    elif psttype == common.PSTTYPE_JOURNAL:
        return "JR"
    elif psttype == common.PSTTYPE_STICKYNOTE:
        return "SN"
    elif psttype == common.PSTTYPE_TASK:
        return "TK"
    elif psttype == common.PSTTYPE_OTHER:
        return "OT"
    elif psttype == common.PSTTYPE_REPORT:
        return "RP"
    elif psttype == common.PSTTYPE_ATTACHMENT:
        return "AT"
    elif psttype is None:
        return "EX"
    else:
        print "ERROR: unknown pst type: " + str(psttype)
        sys.exit


def process_items(db, psttypes, children, item_ids, prefix, digits):
    counter = 1

    if digits == -1: #otherwise it's the source or the top item_id
        l = len(item_ids)
        if l < 10: digits = 1
        elif l < 100: digits = 2
        elif l < 1000: digits = 3
        elif l < 1000: digits = 4
        elif l < 10000: digits = 5
        elif l < 100000: digits = 6
        elif l < 1000000: digits = 7       

    for id in item_ids:
        psttype_id = psttypes[id] 
        new_prefix = "{0}{1}".format(prefix, str(counter).zfill(digits))
        public_id = "{0}-{1}".format(new_prefix, get_suffix(psttype_id))

        db.set_public_id(id, public_id) 

        counter += 1 

        if id in children:
            new_item_ids = children[id]
            new_prefix = "{0}_".format(new_prefix)
            process_items(db, psttypes, children, new_item_ids, new_prefix, -1)


if __name__ == '__main__': main()
