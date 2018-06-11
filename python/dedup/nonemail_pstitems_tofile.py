import os.path
import sys
import time
from shared import common
from shared import database


def run():
    timer_start = time.time()

    md5 = {}
    
    root_path = common.get_path_pstitems_text()

    db = database.DbTool()
    db.open()

    pstitems = db.get_pstitems()
    
    count = 1
    total = len(pstitems)

    for pi in pstitems:
        item_id = pi[0]
        psttype = pi[1]

        if count % 100 == 0:
            print "[nepi_tofile] Processing pstitem {0} of {1} [item_id {2}]".format(count, total, item_id)
        count += 1
        
        if psttype != common.PSTTYPE_NOTE and psttype != common.PSTTYPE_ATTACHMENT: #process emails and attachments separately 
            f_path = os.path.join(root_path, str(item_id))
            sb = []

            ips = db.get_itemproperties_by_item(item_id)
            for ip in ips:
                name = str(ip[0])
                value = str(ip[1])

                sb.append(name)
                sb.append(": ")
                sb.append(value)
                sb.append("\n")
    
            text = '' #create empty files if no text
            if len(sb) > 0:
                text = "".join(sb)

            f = open(f_path, 'w')
            f.write(text)
            f.close()

    db.close()
   
    print common.display_elapsed(timer_start, "STEP COMPLETED: generate text files from non-email pstitems")

