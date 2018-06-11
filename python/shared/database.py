import os.path
import sys
import MySQLdb
import config 
from shared import common as module_common 


class DbTool(object):

    def open(self):
        cnf = config.ConfigReader()
        self._connect = MySQLdb.connect(
            host=cnf.get('DB_HOST'), user=cnf.get('DB_USER'), 
            passwd=cnf.get('DB_PASSWORD'), db=cnf.get('DB_NAME'))
        self._cursor = self._connect.cursor() 

    def close(self):
        self._cursor.close()
        self._connect.close()

    def commit(self):
        self._connect.commit()

#--------------get records-------------------#        
    
    def get_origin_pstfolders(self):
        return self._sp_fetch_all("item__get_origin_pstfolders")
    
    def get_nonorigin_pstfolders(self):
        return self._sp_fetch_all("item__get_nonorigin_pstfolders")
    
    def get_items_by_source(self, source_id):
        return self._sp_fetch_all("item__get_by_source", (source_id,))
    
    def get_pstfolders_by_source(self, source_id):
        return self._sp_fetch_all("pstfolder__get_by_source", (source_id,))

    def get_dataitem(self, item_id):
        return self._sp_fetch_one("data_item__read", (item_id,))
    
    def get_items_for_distro(self, view_name):
        return self._sp_fetch_all("v_distro__get", (view_name,))

    def get_item_children(self, item_id):
        return self._sp_fetch_all("item__get_children", (item_id,))

    def get_item_duplicates(self): 
        reltype_id = module_common.IS_DUPLICATE_RELTYPE_ID
        return self._sp_fetch_all("item_relationship__get_item1_by_reltype", (reltype_id,))
    
    def get_publicids(self):
        return self._sp_fetch_all("item__get_publicids")

    def get_itemproperties_by_item(self, item_id):
        return self._sp_fetch_all("item_property__get_by_item", (item_id,))

    def get_itemproperties_by_property(self, property_id):
        return self._sp_fetch_all("item_property__get_by_property", (property_id,))
    
    def get_properties(self):
        return self._sp_fetch_all("property__get")

    def get_redactions(self): 
        return self._sp_fetch_all("redaction__get")

    def get_sources_for_distro(self, view_name):
        return self._sp_fetch_all("source__get_by_view", (view_name,))

    def get_fileitems(self):
        return self._sp_fetch_all("fileitem__get")

    def get_pstitems(self):
        return self._sp_fetch_all("pstitem__get")

    def get_dedup_data(self):
        return self._sp_fetch_all("data_dedup__get")

    def get_item_relationships_by_reltype(self, reltype_id): 
        return self._sp_fetch_all("item_relationship__get_by_reltype", (reltype_id,))
    
    def get_item_relationships_by_item1(self, item_id): 
        return self._sp_fetch_all("item_relationship__get_by_item1", (item_id,))

    def get_item_relationships_by_item2(self, item_id): 
        return self._sp_fetch_all("item_relationship__get_by_item2", (item_id,))

    def create_item_relationship(self, item1_id, reltype_id, item2_id, value):
        return self._sp_execute("item_relationship__create", (item1_id, reltype_id, item2_id, value))

    def create_data_dedup_nonemailpst(self, item_id, md5sum):
        return self._sp_execute("data_dedup__create_nonemailpst", (item_id, md5sum))

    def create_data_dedup_hash(self, item_id, hash1, hash2, hash3, hash4, hash5, hash6, hash7, hash8, hash9, hash10, hash11, hash12, hash13, hash14, hash15):
        return self._sp_execute("data_dedup_hash__create", (item_id, hash1, hash2, hash3, hash4, hash5, hash6, hash7, hash8, hash9, hash10, hash11, hash12, hash13, hash14, hash15))

    # be very careful with this
    def get_records(self, sql):
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_md5sums(self):
        return self._sp_fetch_all("data_item__get_md5sums")

    def update_file_md5sum(self, item_id, md5sum):
        return self._sp_execute("data_item__update_md5sum", (item_id, md5sum))

    def get_publicids(self): 
        sql = """SELECT id, public_id FROM item"""
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    # be very careful with this
    def exec_sql(self, sql, params):
        self._cursor.execute(sql, params)
        return 0

#---------------------------create records-----------------------------#
    def create_source(self, name, filesize):        
        sql = """INSERT INTO source (name, filesize) VALUES (%s, %s);"""
        return self._exec_lastrowid(sql, (name, filesize)) 

    def create_pstfolder(self, parent_id, source_id, name):
        sql = """INSERT INTO pstfolder (parent_id, source_id, name) VALUES (%s, %s, %s)""" 
        return self._exec_lastrowid(sql, (parent_id, source_id, name))

    def create_item(self, source_id, parent_id, level):        
        sql = """INSERT INTO item (source_id, parent_id, tree_level)
                 VALUES (%s, %s, %s)"""
        return self._exec_lastrowid(sql, (source_id, parent_id, level))

    def create_pstitem(self, item_id, psttype_id, pstfolder_id):        
        sql = """INSERT INTO pstitem (item_id, psttype_id, pstfolder_id)
                 VALUES (%s, %s, %s)"""
        return self._exec_lastrowid(sql, (item_id, psttype_id, pstfolder_id))

    def create_containeritem(self, item_id, containertype_id):        
        sql = """INSERT INTO containeritem (item_id, containertype_id)
                 VALUES (%s, %s)"""
        return self._exec_lastrowid(sql, (item_id, containertype_id))

    def create_fileitem(self, item_id, original_name, extension, filesize, attch_position):        
        sql = """INSERT INTO fileitem (item_id, original_name, extension, filesize, attch_position)
                 VALUES (%s, %s, %s, %s, %s)"""
        return self._exec_lastrowid(sql, (item_id, original_name, extension, filesize, attch_position))

    def create_property(self, propertytype_id, name):
        sql = """INSERT INTO property (propertytype_id, name) 
                 VALUES (%s, %s)"""
        return self._exec_lastrowid(sql, (propertytype_id, name))

    def create_item_property(self, item_id, property_id, value, batch):
        sql = """INSERT INTO item_property (item_id, property_id, value, batch) VALUES (%s, %s, %s, %s)"""
        try:
            return self._exec_lastrowid(sql, (item_id, property_id, value, batch))
        except:
            self.commit() #commit to database for debugging
            print "ERROR: {0}".format(sys.exc_info()[0])
            print "item_id: {0}".format(item_id)
            print "property_id: {0}".format(property_id)
            print "value: {0}".format(value)
            raise

    def update_item_property(self, item_id, property_id, value, batch):
        sql = """UPDATE item_property SET value = %s, batch = %s WHERE item_id = %s AND property_id = %s;"""
        self._cursor.execute(sql, (value, batch, item_id, property_id))

    def update_data_all_items(self, item_id, text):
        sql = """UPDATE data_all_items SET item_text = %s WHERE item_id = %s;"""
        self._cursor.execute(sql, (text, item_id))

    def update_data_nonemail_items(self, item_id, text):
        sql = """UPDATE data_nonemail_items SET item_text = %s WHERE item_id = %s;"""
        self._cursor.execute(sql, (text, item_id))

    def concat_item_property(self, item_id, property_id, value):
        sql = """UPDATE item_property SET value = concat(value, %s) WHERE item_id = %s AND property_id = %s"""
        return self._exec_lastrowid(sql, (value, item_id, property_id))

    def create_mimesubtype(self, name):
        sql = """INSERT INTO mimesubtype (name) VALUES (%s)"""
        return self._exec_lastrowid(sql, (name,))

    def create_item_relationship(self, item1_id, reltype_id, item2_id, value):
        sql = """INSERT INTO item_relationship (item1_id, reltype_id, item2_id, value) VALUES (%s, %s, %s, %s)"""
        return self._exec_lastrowid(sql, (item1_id, reltype_id, item2_id, value))

    def create_redaction(self, rule_id, original, generated):
        sql = """INSERT INTO redaction (redactrule_id, original, generated) VALUES (%s, %s, %s)"""
        return self._exec_lastrowid(sql, (rule_id, original, generated))
    
    def create_item_redaction(self, item_id, redaction_id, property_id):
        sql = """INSERT INTO item_redaction (item_id, redaction_id, property_id) VALUES (%s, %s, %s)"""
        return self._exec_lastrowid(sql, (item_id, redaction_id, property_id))

    def create_item_all_data(self, item_id, text, meta):
        sql = """INSERT INTO data_all_items (item_id, item_text, item_metadata) VALUES (%s, %s, %s)"""
        return self._exec_lastrowid(sql, (item_id, text, meta))

    def create_item_nonemail_data(self, item_id, text, meta):
        sql = """INSERT INTO data_nonemail_items (item_id, item_text, item_metadata) VALUES (%s, %s, %s)"""
        return self._exec_lastrowid(sql, (item_id, text, meta))

    def create_item_email_data(self, item_id, email_from, email_to, email_cc, email_bcc, email_date, email_subject, email_header, pst_body, meta):
        sql = """INSERT INTO data_email_items (item_id, email_from, email_to, email_cc, email_bcc, email_date, email_subject, email_header, email_body, email_metadata) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        return self._exec_lastrowid(sql, (item_id, email_from, email_to, email_cc, email_bcc, email_date, email_subject, email_header, pst_body, meta))

#---------------------------update/delete records-----------------------------#
    def set_origin_id(self, item_id, origin_id):
        sql = """UPDATE item SET origin_id = %s WHERE id = %s"""
        self._cursor.execute(sql, (origin_id, item_id))
        return 0

    def update_fileitem(self, item_id, mimetype_id, mimesubtype_id, mime_details, mimetypedetector_id):
        sql = """UPDATE fileitem SET mimetype_id = %s, mimesubtype_id = %s, \
                 mime_details = %s, mimetypedetector_id = %s WHERE item_id = %s"""
        self._cursor.execute(sql, (mimetype_id, mimesubtype_id, mime_details, mimetypedetector_id, item_id))
        return 0

    def update_container(self, item_id, is_extracted):
        sql = """UPDATE containeritem SET is_extracted = %s WHERE item_id = %s"""
        self._cursor.execute(sql, (is_extracted, item_id))
        return 0

    def set_public_id(self, item_id, public_id):
        sql = """UPDATE item SET public_id = %s WHERE id = %s"""
        self._cursor.execute(sql, (public_id, item_id))
        return 0

    def set_item_redacttype(self, item_id, redacttype_id):
        sql = """UPDATE item SET redacttype_id = %s WHERE id = %s"""
        self._cursor.execute(sql, (redacttype_id, item_id))
        return 0

#---------------------------get records-----------------------------#
    def get_itemproperties_by_item_detailed(self, item_id):
        sql = """SELECT p.name, ip.value, ip.property_id FROM item_property ip INNER JOIN property p ON p.id = ip.property_id AND ip.item_id = %s """
        self._cursor.execute(sql, (item_id,))
        return self._cursor.fetchall()
    
    def get_items_ordered_by_level(self): 
        sql = """SELECT id, parent_id, tree_level FROM item ORDER BY tree_level ASC"""
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    
    #except1 and except2 are property ids for body and extracted text
    def get_metadata_by_item(self, item_id, except1, except2):
        sql = """SELECT p.name, ip.value, ip.property_id FROM item_property ip INNER JOIN property p ON p.id = ip.property_id AND ip.item_id = %s \
                WHERE ip.property_id <> %s AND ip.property_id <> %s"""
        self._cursor.execute(sql, (item_id, except1, except2))
        return self._cursor.fetchall()
    
    def get_items_by_parent(self, item_id): 
        sql = """SELECT id FROM item WHERE parent_id = %s"""
        self._cursor.execute(sql, (item_id,))
        return self._cursor.fetchall()
    
    def get_itemproperty(self, item_id, property_id):
        sql = """SELECT value FROM item_property WHERE item_id = %s AND property_id = %s"""
        self._cursor.execute(sql, (item_id, property_id))
        return self._cursor.fetchone()
    
    def get_vitems_by_source(self, source_id): 
        sql = """SELECT * FROM v_item WHERE source_id = %s"""
        self._cursor.execute(sql, (source_id,))
        return self._cursor.fetchall()

    def get_items(self): 
        sql = """SELECT id FROM item"""
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_fileitem_names(self):
        sql = """SELECT i.source_id, i.id, f.extension FROM fileitem f INNER JOIN item i ON i.id = f.item_id"""
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    
    def get_fileitem_ids(self):
        sql = """SELECT item_id FROM fileitem"""
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_property(self, propertytype_id, name):
        sql = """SELECT id FROM property WHERE propertytype_id = %s AND name = %s"""
        self._cursor.execute(sql, (propertytype_id, name))
        return self._cursor.fetchone()
    
    def get_mimetypes(self):
        sql = """SELECT id, name FROM mimetype ORDER BY id"""                     
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_mimesubtypes(self):
        sql = """SELECT id, name FROM mimesubtype ORDER BY id"""                     
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_parent_items(self):
        sql = """SELECT parent_id FROM item GROUP BY parent_id ORDER BY parent_id"""                     
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_items_ordered_1(self):
        sql = """SELECT i.id, i.source_id, i.parent_id, i.tree_level, f.extension, p.psttype_id \
                 FROM item i \
                 LEFT OUTER JOIN fileitem f ON f.item_id = i.id \
                 LEFT OUTER JOIN pstitem p ON p.item_id = i.id \
                 ORDER BY i.source_id, i.parent_id, f.attch_position"""
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_source_list(self):
        sql = """SELECT id FROM source ORDER BY id"""                     
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_containers(self):
        sql = """SELECT i.id, i.source_id, i.tree_level, c.containertype_id, f.extension \
                 FROM item i INNER JOIN containeritem c ON c.item_id = i.id \
                 INNER JOIN fileitem f ON f.item_id = i.id \
                 ORDER BY c.containertype_id"""      
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_new_containers(self):
        sql = """SELECT i.id, i.source_id, i.tree_level, c.containertype_id, f.extension \
                 FROM item i INNER JOIN containeritem c ON c.item_id = i.id \
                 INNER JOIN fileitem f ON f.item_id = i.id \
                 AND c.is_extracted IS NULL \
                 ORDER BY c.containertype_id"""      
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_property_id(self, propertytype_id, name):
        sql = """SELECT id FROM property WHERE name LIKE %s AND propertytype_id = %s"""
        row = self._exec_fetchone(sql, (name, propertytype_id))
        if row is not None: 
            return row[0]
        else:
            return -1

    def get_mimetype_id(self, name):
        sql = """SELECT id FROM mimetype WHERE name LIKE %s"""
        row = self._exec_fetchone(sql, (name,))
        if row is not None: 
            return row[0]
        else:
            return -1

    def get_mimesubtype_id(self, name):
        sql = """SELECT id FROM mimesubtype WHERE name LIKE %s"""
        row = self._exec_fetchone(sql, (name,))
        if row is not None: 
            return row[0]
        else:
            return -1

    def get_extracted_items(self):
        sql = """SELECT i.id, i.source_id, f.extension FROM item i \
                 INNER JOIN fileitem f ON f.item_id = i.id \
                 AND i.tree_level > 1"""                     
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def get_pstitems_by_parent(self, parent_id):
        sql = """SELECT i.id, p.psttype_id FROM pstitem p INNER JOIN item i ON \
                 i.id = p.item_id AND i.parent_id = %s ORDER BY i.id"""  
        self._cursor.execute(sql, (parent_id,))
        return self._cursor.fetchall()

    def get_fileitems_by_parent(self, parent_id):
        sql = """SELECT i.id, f.extension FROM fileitem f INNER JOIN item i ON \
                 i.id = f.item_id AND i.parent_id = %s ORDER BY i.id"""  
        self._cursor.execute(sql, (parent_id,))
        return self._cursor.fetchall()

    def get_containeritems_by_parent(self, parent_id):
        sql = """SELECT i.id, i.source_id, i.tree_level, c.containertype_id, f.extension \
                 FROM item i INNER JOIN containeritem c ON c.item_id = i.id \
                 INNER JOIN fileitem f ON f.item_id = i.id AND i.parent_id = %s \
                 ORDER BY c.containertype_id"""      
        self._cursor.execute(sql, (parent_id,))
        return self._cursor.fetchall()

    def get_fileitems_by_mimetype(self, mimetype_id):
        if mimetype_id is not None:
            sql = """SELECT i.source_id, i.id, f.extension FROM fileitem f INNER JOIN item i ON \
                     i.id = f.item_id AND f.mimetype_id = %s"""  
            self._cursor.execute(sql, (mimetype_id,))
            return self._cursor.fetchall()
        else:
            sql = """SELECT i.source_id, i.id, f.extension FROM fileitem f INNER JOIN item i ON \
                     i.id = f.item_id AND f.mimetype_id IS NULL"""  
            self._cursor.execute(sql)
            return self._cursor.fetchall()

    def get_fileitems_by_mimetype_and_level(self, mimetype_id, level):
        if mimetype_id is not None:
            sql = """SELECT i.source_id, i.id, f.extension FROM fileitem f INNER JOIN item i ON \
                     i.id = f.item_id AND f.mimetype_id = %s AND i.tree_level = %s"""  
            self._cursor.execute(sql, (mimetype_id, level))
            return self._cursor.fetchall()
        else:
            sql = """SELECT i.source_id, i.id, f.extension FROM fileitem f INNER JOIN item i ON \
                     i.id = f.item_id AND f.mimetype_id IS NULL AND i.tree_level = %s"""  
            self._cursor.execute(sql, (level,))
            return self._cursor.fetchall()
   
    def get_items_by_source(self, source_id):
        sql = """SELECT i.id, i.parent_id, p.psttype_id FROM item i \
                 LEFT OUTER JOIN pstitem p ON p.item_id = i.id \
                 LEFT OUTER JOIN fileitem f ON f.item_id = i.id \
                 WHERE i.source_id = %s \
                 ORDER BY i.parent_id, f.attch_position, f.original_name"""   
        self._cursor.execute(sql, (source_id,))
        return self._cursor.fetchall()

#---------------------------helpers-----------------------------#
    def _exec_lastrowid(self, sql, params):
        self._cursor.execute(sql, params)
        return self._cursor.lastrowid

    def _exec_fetchone(self, sql, params):
        self._cursor.execute(sql, params)
        return self._cursor.fetchone()

  # ----------------- private -----------------#
    def _sp_fetch_one(self, sp, params = None):
        self._call_sp(sp, params)
        return self._finalize_sp(self._cursor.fetchone())
    
    def _sp_fetch_all(self, sp, params = None):
        self._call_sp(sp, params)
        return self._finalize_sp(self._cursor.fetchall())

    def _sp_execute(self, sp, params = None):
        self._call_sp(sp, params)

    def _call_sp(self, sp, params):
        if params is not None:
            self._cursor.callproc(sp, params)
        else:
            self._cursor.callproc(sp)

    def _finalize_sp(self, result):
        self._cursor.nextset() #mysqldb/python requirement
        return result
