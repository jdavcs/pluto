import os.path
import re
import sys
import time
import array
from shared import config
from shared import item as mod_item
from shared import common as mod_comm
from shared import database as mod_db
from shared import property as mod_prop

DISTRO_VIEW = "v_distro"


def get_type_by_publicid(public_id):
    if 'EM' in public_id:
        return 'email'
    elif 'SC' in public_id:
        return 'schedule'
    elif 'AP' in public_id:
        return 'appoitnment'
    elif 'CN' in public_id:
        return 'contact'
    elif 'JR' in public_id:
        return 'journal'
    elif 'SN' in public_id:
        return 'stickynote'
    elif 'TK' in public_id:
        return 'task'
    elif 'OT' in public_id:
        return 'other'
    elif 'RP' in public_id:
        return 'report'
    elif 'AT' in public_id:
        return 'attachment'
    elif 'EX' in public_id:
        return 'extracted file'
    else:
        print "ERROR: unknown type: " + str(public_id)
        sys.exit


class DistroBuilder():

    def run(self):
        self._write_collection_xml_files()
        self._write_text_files()
                
# --------------------------- private: initialize and load -------------------------- #
    def __init__(self, distro_path):                
        self._make_dirs(distro_path)
        self._property = mod_prop.PropertyRepository()
        self._items          = set()  #IDs of all items from view
        self._sources        = None   #tuple from db.get_sources_for_distro  
        self._source_folders = {}     #key = source_id; value = tuple from db.get_pstfolders_by_source
        self._publicids      = {}     #key = item_id; value = public_id
        self._redactions     = {}     #key = original string; value = generated string
        self._folderitems    = {}     #key = folder_id; value = list of item_publicids
        self._source_items   = {}     #key = source_id; value = list of item_ids 
        self._load()

    def _load(self):
        db = mod_db.DbTool()
        db.open()
        self._load_items(db)
        self._load_publicids(db)
        self._load_sources(db)
        self._load_source_folders(db)
        self._load_redactions(db)
        self._load_pstfolders(db)
        self._sort_folderitems()
        db.close()

    def _load_items(self, db):
        print "Loading items"
        rows = db.get_items_for_distro(DISTRO_VIEW)
        for r in rows:
            item_id   = r[0]
            src_id    = r[1]
            public_id = r[2]

            self._items.add(item_id)
            
            if src_id not in self._source_items:
                self._source_items[src_id] = []
            self._source_items[src_id].append(item_id)

    def _load_publicids(self, db):
        print "Loading public IDs"
        rows = db.get_publicids()
        for r in rows:
            item_id = r[0]
            public_id = r[1]
            self._publicids[item_id] = public_id

    def _load_sources(self, db):
        print "Loading sources"
        self._sources = db.get_sources_for_distro(DISTRO_VIEW)        

    def _load_source_folders(self, db):
        print "Loading source pst folders"
        for s in self._sources:
            src_id = s[0]
            self._source_folders[src_id] = db.get_pstfolders_by_source(src_id)

    def _load_redactions(self, db):
        print "Loading redactions"
        rows = db.get_redactions()
        for r in rows:
            str_old = r[2]
            str_new = r[3]
            self._redactions[str_old] = str_new

    def _load_pstfolders(self, db):
        print "Fetching pst folders of origin items"
        rows = db.get_origin_pstfolders() #gets pstfolders of origins
        print "Loading pst folders of {0} origin items".format(len(rows))
        for r in rows:
            item_id   = r[0]
            public_id = r[1]
            folder_id = r[2]
            if item_id in self._items:
                self._load_dictionaries(folder_id, public_id)

        print "Fetching pst folders of non-origin items"
        rows = db.get_nonorigin_pstfolders() #gets pst folders of non-origins
        print "Loading pst folders of {0} non-origin items".format(len(rows))
        for r in rows:
            item_id   = r[0]
            public_id = r[1]
            folder_id = r[2]
            if item_id in self._items:
                self._load_dictionaries(folder_id, public_id)

    def _load_dictionaries(self, folder_id, public_id):
        d1 = self._folderitems
        if folder_id not in d1:
            d1[folder_id] = []
        d1[folder_id].append(public_id)
    
    def _sort_folderitems(self): #sort by public ids!
        for key in self._folderitems:
            list = self._folderitems[key]
            list.sort()

# --------------------------- private: main functionality -------------------------- #
    def _make_dirs(self, distro_path):
        self.path = distro_path
        if not os.path.exists(distro_path):
            os.mkdir(distro_path)

        self.path_text = os.path.join(distro_path, 'text')
        self.path_cust = os.path.join(distro_path, 'custodians')

        if not os.path.exists(self.path_text):
            os.mkdir(self.path_text)
       
        if not os.path.exists(self.path_cust):
            os.mkdir(self.path_cust)

    def _write_collection_xml_files(self):
        print "Writing collection xml file"

        collection_name = config.ConfigReader().get('COLLECTION_NAME')

        sb = []
        sb.append('<?xml version="1.0" ?>')
        sb.append('\n<collection xmlns:xi="http://www.w3.org/2001/XInclude">')
        sb.append('\n\t<name>{0}</name>'.format(collection_name))
        sb.append('\n\t<timestamp>{0}</timestamp>'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        sb.append('\n\t<custodians>')
        
        for s in self._sources:
            src_id    = s[0]
            src_name  = s[1]
            src_size  = s[2]                    
            itemcount = s[3]

            src_id_str = mod_comm.get_source_dir(src_id)
            src_name = mod_comm.xml_filter_encoding(src_name) #just a safeguard
            src_size = mod_comm.format_size(src_size)

            sb.append('\n\t\t<!-- custodian id="{0}" items="{1}" source_file_name="{2}" source_file_size="{3}" -->'.format(src_id, itemcount, src_name, src_size))
            sb.append('\n\t\t<xi:include href="custodians/{0}.xml" />'.format(src_id_str))  
            
            self._write_custodian_xml_file(src_id, src_id_str, src_name, src_size, itemcount)
        
        sb.append('\n\t</custodians>')
        sb.append('\n</collection>')
        sb.append('\n\n')

        filepath = os.path.join(self.path, 'collection.xml')
        self._write_file(filepath, sb)

    def _write_custodian_xml_file(self, src_id, src_id_str, src_name, src_size, itemcount):
            print "Writing custodian xml file for {0}".format(src_id)
        
            sb = []
            sb.append('<?xml version="1.0" ?>')
            sb.append('\n<custodian id="{0}" items="{1}"> '.format(src_id, itemcount))
            sb.append('\n\t<source_file size="{0}">{1}</source_file>'.format(src_size, src_name))

            sb.append('\n\t<pst-folders>')
            self._build_pstfolders_section(sb, src_id)
            sb.append('\n\t</pst-folders>')
            
            sb.append('\n\t<items>')
            for item_id in self._source_items[src_id]:
                self._build_item_tag(sb, item_id)
            sb.append('\n\t</items>')
            
            sb.append('\n</custodian>')
            sb.append('\n\n')
 
            filename = src_id_str + '.xml'
            filepath = os.path.join(self.path_cust, filename)
            self._write_file(filepath, sb)

    def _build_pstfolders_section(self, sb, src_id):
        children = {}   # key = id; value = [children]
        names    = {}   # key = id; value = name

        root_id = None
        for r in self._source_folders[src_id]:
            id        = r[0]
            parent_id = r[1]
            name      = r[2]

            names[id] = name

            if parent_id is None: #there should be only one per source
                root_id = id
            else:
                if parent_id not in children:
                    children[parent_id] = []
                children[parent_id].append(id)

        self._build_pstfolder_node(sb, src_id, root_id, children, names, 2)

    def _build_pstfolder_node(self, sb, src_id, id, children, names, level):
        tabs = mod_comm.get_tabs(level, '\t')
        foldername = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(names[id]), '\t\t')       

        itemcount = 0
        if id in self._folderitems:
            itemcount = len(self._folderitems[id])

        subfoldercount = 0
        if id in children:
            subfoldercount = len(children[id])
        
        sb.append('\n{0}<pst_folder id="{1}" items="{2}" subfolders="{3}">'.format(tabs, str(id), itemcount, subfoldercount))
        sb.append('\n\t{0}<name>{1}</name>'.format(tabs, foldername))

        if subfoldercount > 0:
            for child_id in children[id]:
                self._build_pstfolder_node(sb, src_id, child_id, children, names, level + 2)

        sb.append('\n{0}</pst_folder>'.format(tabs))
   
    def _build_item_tag(self, sb, item_id):
        item = mod_item.Item(item_id)
        type = get_type_by_publicid(item.public_id())

        sb.append('\n\t\t<item id="{0}" type="{1}"'.format(item.public_id(), type))

        if item.redacttype_id() == mod_comm.REDACTTYPE_FULL:
            sb.append(' redacted="true">')
        else:
            if item.has_duplicates():
                sb.append(' duplicates="{0}"'.format(len(item.duplicates())))
            sb.append('>')

            self._build_files_tag(sb, item)

            self._build_relationship_tag(sb, item)

            if item.is_pstitem():
                self._build_pstdata_tag(sb, item)

            if item.is_container():
                self._build_containerdata_tag(sb, item)

            if item.is_file():
                self._build_filedata_tag(sb, item)

            if len(item.metadata()) > 0:
                self._build_metadata_tag(sb, item)
           
        sb.append('\n\t\t</item>')

    def _build_files_tag(self, sb, item):

        dirname = mod_comm.get_source_dir(item.source_id())

        if item.is_email() or (item.is_file() and item.extracted_chars() > 0):
            sb.append('\n\t\t\t<files>')
            sb.append('\n\t\t\t\t<file type="text" name="{0}.txt" path="../../text/{1}/{0}.txt" />'.format(item.public_id(), dirname))
            sb.append('\n\t\t\t</files>')

    def _build_relationship_tag(self, sb, item):
        if self._has_relationships(item):
            sb.append('\n\t\t\t<relationships>')

            if item.is_duplicate():
                duplicate_of_public_id = self._publicids[item.duplicate_of()] 
                sb.append('\n\t\t\t\t<duplicate_of id="{0}" />'.format(duplicate_of_public_id))

            if item.parent_id() is not None:
                parent_publicid = self._publicids[item.parent_id()] 
                if item.is_pstitem() and item.psttype_id() == mod_comm.PSTTYPE_ATTACHMENT:
                    sb.append('\n\t\t\t\t<attached_to id="{0}" />'.format(parent_publicid))
                else:
                    sb.append('\n\t\t\t\t<extracted_from id="{0}" />'.format(parent_publicid))

            if item.is_email() and item.is_reply():
                reply_to_publicid = self._publicids[item.reply_to()]
                sb.append('\n\t\t\t\t<reply_to id="{0}" />'.format(reply_to_publicid))

            sb.append('\n\t\t\t</relationships>')

    def _has_relationships(self, item):        
        return item.parent_id() is not None or item.is_duplicate() or (item.is_email() and item.is_reply())

    def _build_pstdata_tag(self, sb, item):
        pstfolder_name = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.pstfolder_name()), '\t\t')       
        sb.append('\n\t\t\t<pst-data type="{0}" '.format(item.psttype_name()))

        if item.psttype_id() != mod_comm.PSTTYPE_ATTACHMENT: #attachments cannot have attachments, any other pstitem can.
            sb.append('attachments="{0}"'.format(len(item.children())))

        sb.append('>')

        sb.append('\n\t\t\t\t<pst-folder id="{0}">{1}</pst-folder>'.format(item.pstfolder_id(), pstfolder_name))

        if item.is_email():
            to      = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.email_to()), '\t\t\t')
            cc      = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.email_cc()), '\t\t\t')
            bcc     = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.email_bcc()), '\t\t\t')
            date    = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.email_date()), '\t\t\t')
            subject = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.pst_subject()), '\t\t\t')

            if item.redacttype_id() == mod_comm.REDACTTYPE_CONTENT:
                to      = self._redact_text(to)
                cc      = self._redact_text(cc)
                bcc     = self._redact_text(bcc)
                date    = self._redact_text(date)
                subject = self._redact_text(subject)

            sb.append('\n\t\t\t\t<email-data ')

            if item.has_replies():
                sb.append('replies="{0}" '.format(len(item.replies())))

            if item.is_email_header_generated():
                sb.append('header-generated="true" ')

            sb.append('>')

            if to != '':
                sb.append('\n\t\t\t\t\t<email-to>{0}</email-to>'.format(to))
            if cc != '':
                sb.append('\n\t\t\t\t\t<email-cc>{0}</email-cc>'.format(cc))
            if bcc != '':
                sb.append('\n\t\t\t\t\t<email-bcc>{0}</email-bcc>'.format(bcc))
            if date != '':
                sb.append('\n\t\t\t\t\t<email-date>{0}</email-date>'.format(date))
            if subject != '':
                sb.append('\n\t\t\t\t\t<email-subject>{0}</email-subject>'.format(subject))

            sb.append('\n\t\t\t\t</email-data>')
        sb.append('\n\t\t\t</pst-data>')

    def _build_containerdata_tag(self, sb, item):
        if item.container_is_extracted(): 
            is_extracted = 'true'
        else: 
            is_extracted = 'false'

        sb.append('\n\t\t\t<container-data type="{0}" is_extracted="{1}" extracted="{2}" />'.format(
            item.containertype_name(), is_extracted, len(item.children())))

    def _build_filedata_tag(self, sb, item):
        name        = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.file_name()), '\t\t')
        extension   = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.file_extension()), '\t\t')
        mimetype    = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.file_mimetype_name()), '\t\t')
        mimesubtype = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(item.file_mimesubtype_name()), '\t\t')

        sb.append('\n\t\t\t<file-data size="{0}" extracted-chars="{1}">'.format(
            item.file_size(), item.extracted_chars()))

        if name != '':
            sb.append('\n\t\t\t\t<name>{0}</name>'.format(name))

        if extension != '':
            sb.append('\n\t\t\t\t<extension>{0}</extension>'.format(extension))
            
        if mimetype != '':
            sb.append('\n\t\t\t\t<mime-type>{0}</mime-type>'.format(mimetype))

        if mimesubtype != '':
            sb.append('\n\t\t\t\t<mime-subtype>{0}</mime-subtype>'.format(mimesubtype))
        
        sb.append('\n\t\t\t</file-data>')

    def _build_metadata_tag(self, sb, item):
        sb.append('\n\t\t\t<metadata>')

        for key in item.metadata():
            prop_id    = key
            prop_value = item.metadata()[key] 
            prop_name  = self._property.get_name(prop_id)

            criteria1 = item.is_email() and prop_id != mod_prop.PST_BODY_ID and prop_id != mod_prop.PST_HEADER_ID
            criteria2 = not item.is_email() and prop_id != mod_prop.EXTRACTED_TEXT_ID

            if criteria1 or criteria2:
                name = mod_comm.xml_filter_element_name(mod_comm.xml_filter_encoding(prop_name))       
                value = mod_comm.xml_filter_cdata(mod_comm.xml_filter_encoding(prop_value), '\t\t\t\t')

                if item.redacttype_id() == mod_comm.REDACTTYPE_CONTENT:
                    value = self._redact_text(value)
            
                if len(value) > 0:
                    sb.append('\n\t\t\t\t<field name="{0}">{1}</field>'.format(name, value))

        sb.append('\n\t\t\t</metadata>')

    def _redact_text(self, text):
        if len(text) > 0:
            for key in self._redactions:
                if key in text:
                    text = text.replace(key, self._redactions[key])
        return text
    
    def _write_text_files(self):
        count = 0
        total = len(self._items)
        for id in self._items:
            item = mod_item.Item(id)
            if count % 100 == 0:
                print 'Processing item {0} of {1} [id# {2}]'.format(count, total, item.id())
            count += 1
            self._write_textfile(item)

    def _write_textfile(self, item):
        #write only non-duplicate and non-fully redacted items
        if not item.is_duplicate() and item.redacttype_id() != mod_comm.REDACTTYPE_FULL:
            sb = []

            if item.is_email(): #which are emails,
                sb.append(item.email_header())
                if len(sb) > 0:
                    sb.append('\n\n')
                sb.append(item.pst_body())

            elif item.is_file() and item.extracted_chars() > 0: #or are files with extracted text.
                sb.append(item.extracted_text())

            text = ''.join(sb) #must convert to string before redacting

            if item.redacttype_id() == mod_comm.REDACTTYPE_CONTENT:
                text = self._redact_text(text)

            #write only nonempty files
            if len(text) > 0:
                sb2 = []
                sb2.append(text)
                sb2.append('\n\n')
                self._write_item_file(item, sb2, 'txt', self.path_text)

    def _write_item_file(self, item, sb, extension, path):
        dirname = mod_comm.get_source_dir(item.source_id())
        dirpath = os.path.join(path, dirname)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        filename = "{0}.{1}".format(item.public_id(), extension)
        filepath = os.path.join(dirpath, filename)
        self._write_file(filepath, sb)

    def _write_file(self, path, sb):
        file = open(path, 'w')
        file.writelines(sb)
        file.close()
