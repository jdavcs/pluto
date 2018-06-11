import os.path
import sys
import time
from shared import common
from shared import database
from shared import mimetype_detector
from containers import container_extractor

BATCH = 2


def main():
    timer_start = time.time()
    
    db = database.DbTool()
    db.open()

    _extract_containers(db)

    db.commit() 
    db.close()

    print common.display_elapsed(timer_start, "extract containers")


def _extract_containers(db):
    mdetect = mimetype_detector.MimetypeDetector(db)

    iteration = 0
    while True:
        iteration += 1
        clist = db.get_new_containers()        

        if iteration > 20:            
            print "BREAKING LOOP: reached 20 levels of nesting!"
            break # safeguard

        if len(clist) == 0:
            break
        else:
            total = len(clist)
            counter = 1
            for citem in clist:
                print "processing container {0} of {1} at interation {2}".format(counter, total, iteration)
                counter += 1           
                container_extractor.extract(db, citem, BATCH)

            level = iteration + 1

            #later refactor this: it's the same loop as in the mime-detection driver program!
            flist = db.get_fileitems_by_mimetype_and_level(None, level)
            f_total = len(flist)
            f_counter = 1
            for f in flist:
                if f_counter % 10 == 0:
                    print "detecting MIME-type for file {0} of {1} at interation {2}".format(f_counter, f_total, iteration)
                f_counter += 1           

                source_id = f[0]
                item_id = f[1]
                extension = f[2]
               
                f_path = common.get_path_files_processed_item(source_id, item_id, extension)
                
                mdata = mdetect.get_mimetype_data(f_path)
                mdetect.process_item(item_id, f_path, mdata)

            db.commit() #commit for each iteration


if __name__ == '__main__': main()
