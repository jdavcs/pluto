import os.path
import sys
import time
from shared import common
from shared import database


def main():
    db = database.DbTool()
    db.open()

    item_origins = {} #stores origin_id for each item_id. Items with level=0 have themselves as origins

    items = db.get_items_ordered_by_level() #must be ordered by level!
    for i in items:
        item_id = i[0]
        parent_id = i[1]
        level = i[2]

        if parent_id is None:
            item_origins[item_id] = item_id #we need this so we can retrieve this origin later
        else:
            origin_id = item_origins[parent_id] #retrieve origin for parent
            item_origins[item_id] = origin_id #assign same origin to item

    count = 1
    total = len(item_origins)
    for key in item_origins:
        if (count % 1000 == 0):
            print "Processing item {0} of {1} [{2}]".format(count, total, item_id)
        count += 1

        if key != item_origins[key]:        #ignore top-levels
            db.set_origin_id(key, item_origins[key])

    db.commit() 
    db.close()


if __name__ == '__main__': main()
