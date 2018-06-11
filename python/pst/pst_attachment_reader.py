import sys
import os.path
import _libpst
from shared import common


class PstAttachmentReader(object):

    def __init__(self, db, pst, src_id, parent_item_id, tree_level, folder_id, property_dic, batch):
        self._db = db
        self._pst = pst
        self._src_id = src_id
        self._parent_item_id = parent_item_id
        self._level = tree_level
        self._folder_id = folder_id
        self._path_out = common.get_path_files_processed_source(src_id)
        self._property_dic = property_dic
        self._batch = batch

    def read(self, attch_item):
        if attch_item.method != 0:

            item_id = self._db.create_item(self._src_id, self._parent_item_id, self._level)
            self._db.create_pstitem(item_id, common.PSTTYPE_ATTACHMENT, self._folder_id)
       
            self._read_field(item_id, "filename1", attch_item.filename1.str)
            self._read_field(item_id, "filename2", attch_item.filename2.str)
            self._read_field(item_id, "mimetype", attch_item.mimetype.str)
            self._read_field(item_id, "position", attch_item.position)
            self._read_field(item_id, "sequence", attch_item.sequence)

            #process filename: use pst attch property "filename2": this is the original filename
            original_name, extension = os.path.splitext(attch_item.filename2.str)

            extension = extension.lower() #lowercase extensions for convenience

            filename = "{0}{1}".format(item_id, extension)
        
            f_path = os.path.join(self._path_out, filename)
            file = open(f_path, 'w')        

            #Update: added str() to guard against rare cases when trying to write not a string
            #Cause: empty attachment file
            file.write(str(self._pst.pst_attach_to_mem(attch_item)))

            file.flush()    
            file.close()               

            filesize = os.path.getsize(f_path)
            attch_position = attch_item.position

            self._db.create_fileitem(item_id, original_name, extension, filesize, attch_position)

        if attch_item.next is not None:
            self.read(attch_item.next)

    def _read_field(self, item_id, name, value):
        if value != "":
            value = str(value).strip() 
            key = "{0}_{1}".format(common.PROPERTYTYPE_PSTITEM_ATTACHMENT, name)
            if key in self._property_dic:
                property_id = self._property_dic[key]
            else:
                property_id = self._db.create_property(common.PROPERTYTYPE_PSTITEM_ATTACHMENT, name)
                self._property_dic[key] = property_id

            self._db.create_item_property(item_id, property_id, value, self._batch)
