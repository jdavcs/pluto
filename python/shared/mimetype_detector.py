import sys
import os.path
import common 
import config 
import database


#returns tuple: (mimetype, mimesubtype, details, detector_id): same as detect()
class MimetypeDetector(object):

    def __init__(self, db):
        self._db = db

        self._cnf = config.ConfigReader()

        self._mt_dic = {}
        mtlist = db.get_mimetypes()
        for mt in mtlist:
            id = mt[0]
            name = mt[1]
            self._mt_dic[name] = id

        self._mst_dic = {}
        mstlist = db.get_mimesubtypes()
        for mst in mstlist:
            id = mst[0]
            name = mst[1]
            self._mst_dic[name] = id

        self._unknown_types = []

    #returns tuple: (mimetype, mimesubtype, details, detector_id)
    def get_mimetype_data(self, path):
        mimetype = ""
        mimesubtype = ""
        details = ""
        detector = self._cnf.get('MIMETYPE_DETECTOR_UNIX')

        details = common.exec_cmd("file -b -e cdf '{0}'".format(path))[0].strip()
        
        mime_str = common.exec_cmd("file -b --mime-type '{0}'".format(path))[0].strip()

        if len(mime_str) > 0 and mime_str.find("/") > 0: 
            type = mime_str.split("/", 1)
            mimetype = type[0].strip()
            mimesubtype = type [1].strip()

        return mimetype, mimesubtype, details, detector

    def get_mimetype(self, name):
        if name in self._mt_dic:
            return self._mt_dic[name]
        else:
            print "ERROR: unknown top-level mime-type: " + name
            sys.exit()

    def get_mimesubtype(self, name):
        if name in self._mst_dic:
            return self._mst_dic[name]
        else:
            #create new mime=subtype in db + add to dict!!!
            id = self._db.create_mimesubtype(name)
            self._mst_dic[name] = id
            print "Found new MIME-subtype: {0}".format(name)
            return id

    def process_item(self, item_id, path, mdata):
        mimetype = mdata[0]
        mimesubtype = mdata[1]
        details = mdata[2]
        detector_id = mdata[3]
        
        mimetype_id = None
        mimesubtype_id = None

        #if no mimetype was detected - we don't need to look for mimesubtype or check if it's a container
        if len(mimetype) > 0:
            mimetype_id = self.get_mimetype(mimetype)
            mimesubtype_id = self.get_mimesubtype(mimesubtype)

            containertype_id = common.get_containertype(mimetype, mimesubtype, details)       
            if containertype_id > -1:
                self._db.create_containeritem(item_id, containertype_id)
        else:
            self._unknown_types.append(path)

        #Finally, update in any case (details and detector will be present)
        self._db.update_fileitem(item_id, mimetype_id, mimesubtype_id, details, detector_id)
