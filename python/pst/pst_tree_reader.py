import sys
import os.path
import _libpst
from shared import common
from shared import database
from pst_item_reader import PstItemReader


class PstTreeReader(object):

    def __init__(self, db, source_id, parent_item_id, level, path_in, path_out, store_folders, batch):
        self._db = db
        self._source_id = source_id
        self._parent_item_id = parent_item_id
        self._level = level
        self._path_out = path_out
        self._pst = _libpst.pst(path_in, 'ASCII')
        self._store_folders = store_folders
        self._load_properties()
        self._counter = 0
        self._batch = batch

    def _load_properties(self):  
        self._property_dic = {}
        plist = self._db.get_properties()
        for p in plist:
            id = p[0]
            type_id = p[1]
            name = p[2]
            key ="{0}_{1}".format(type_id, name) # not refactoring for better perfrmance: PSTItemReader uses this a lot!
            self._property_dic[key] = id

    def read(self):
        # create root folder
        root_folder_id = None
        if self._store_folders:
            root_folder_id = self._db.create_pstfolder(None, self._source_id, common.PST_ROOT_FOLDER_NAME)

        # launch libpst extraction
        pst_tree = self._pst.pst_getTopOfFolders()
        self._read_tree(pst_tree, root_folder_id)

    def _read_tree(self, pst_tree, parent_folder_id):
        self._counter += 1
        if self._counter % 100 == 0:
            self._db.commit() #commit every 100 items

        while (pst_tree is not None):
            pst_item = self._pst.pst_parse_item(pst_tree, None) #TODO check this method signature: why none?
            if pst_item.folder is not None: 
                folder_id = None
                if self._store_folders:
                    folder_id = self._db.create_pstfolder(parent_folder_id, self._source_id, pst_item.file_as.str)
                if pst_tree.child is not None: 
                    self._read_tree(pst_tree.child, folder_id)
            else:               
                reader = PstItemReader(self._db, self._pst, self._source_id, self._property_dic, self._batch)
                reader.read(pst_item, self._parent_item_id, parent_folder_id, self._level)

            pst_tree = pst_tree.next
