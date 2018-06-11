import os.path
import sys
import time
from shared import common
from shared import database
from shared import mimetype_detector


def main():
    timer_start = time.time()
    
    db = database.DbTool()
    db.open()

    _detect_mimetypes(db)

    db.commit() #final commit (cleanup)
    db.close()

    print common.display_elapsed(timer_start, "detect MIME-types")


def _detect_mimetypes(db):
    mdetect = mimetype_detector.MimetypeDetector(db)

    flist = db.get_fileitems_by_mimetype(None) #get only not identified files
    total = len(flist)
    counter = 1

    for f in flist:
        if counter % 10 == 0:
            print "Processing file {0} of {1}".format(counter, total)   
        counter += 1

        source_id = f[0]
        item_id = f[1]
        extension = f[2]

        f_path = common.get_path_files_processed_item(source_id, item_id, extension)

        mdata = mdetect.get_mimetype_data(f_path)
        mdetect.process_item(item_id, f_path, mdata)

        if counter % 1000 == 0:
            db.commit() #commit for every 1000 files

    db.commit() # final commit


if __name__ == '__main__': main()
