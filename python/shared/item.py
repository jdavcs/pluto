from shared import database
from shared import property
from shared import psttype
from shared import common

PST_EXCEPTION       = "Item is not a PST item"
FILE_EXCEPTION      = "Item is not a file"
CONTAINER_EXCEPTION = "Item is not a container"
EMAIL_EXCEPTION     = "Item is not an email"


class Item(object):
    # ------------- all item properties ---------------- #
    def id(self):                  
        return self._item_id

    def source_id(self):                
        return self._source_id

    def source_name(self):              
        return self._source_name

    def parent_id(self):                
        return self._parent_id

    def tree_level(self):               
        return self._tree_level

    def public_id(self):                
        return self._public_id

    def redacttype_id(self):            
        return self._redacttype_id

    def origin_id(self):                
        return self._origin_id

    # ------------- all item methods ---------------- #
    def is_email(self):
        return self._psttype_id == psttype.NOTE_ID
        
    def is_pstitem(self):
        return self._psttype_id is not None
    
    def is_file(self):
        return self._file_size is not None        

    def is_container(self):
        return self._conttype_id is not None

    def is_duplicate(self):
        return self._duplicate_of is not None

    def duplicate_of(self):
        return self._duplicate_of
    
    def has_duplicates(self):
        return len(self._duplicates) > 0

    def duplicates(self):
        return self._duplicates

    def has_children(self):
        return len(self._children) > 0
    
    def children(self):
        return self._children

    def metadata(self):
        return self._metadata_dict

    # ------------- pst item properties---------------- #
    def psttype_id(self):            
        if self.is_pstitem():
            return self._psttype_id
        else:
            raise Exception(PST_EXCEPTION)        

    def psttype_name(self):
        if self.is_pstitem():
            return self._psttype_name
        else:
            raise Exception(PST_EXCEPTION)        

    def pstfolder_id(self):
        if self.is_pstitem():
            return self._pstfolder_id
        else:
            raise Exception(PST_EXCEPTION)        

    def pstfolder_name(self):
        if self.is_pstitem():
            return self._pstfolder_name
        else:
            raise Exception(PST_EXCEPTION)        

    # ------------- pst item common methods---------------- #
    def pst_subject(self):
        if self.is_pstitem(): 
            return self._pst_subject
        else:               
            raise Exception(PST_EXCEPTION)
    
    def pst_body(self):
        if self.is_pstitem(): 
            return self._pst_body
        else:               
            raise Exception(PST_EXCEPTION)
    
    # ------------- container item properties---------------- #
    def containertype_id(self):
        if self.is_container():
            return self._conttype_id
        else:
            raise Exception(CONTAINER_EXCEPTION)

    def containertype_name(self):
        if self.is_container():
            return self._conttype_name
        else:
            raise Exception(CONTAINER_EXCEPTION)

    def container_is_extracted(self):
        if self.is_container():
            return self._cont_isextracted
        else:
            raise Exception(CONTAINER_EXCEPTION)

    # ------------- file item properties---------------- #
    def file_mimetype_id(self):
        if self.is_file():
            return self._file_mimetype_id
        else:
            raise Exception(FILE_EXCEPTION)

    def file_mimetype_name(self):
        if self.is_file():
            return self._file_mimetype_name
        else:
            raise Exception(FILE_EXCEPTION)

    def file_mimesubtype_id(self):
        if self.is_file():
            return self._file_mimesubtype_id
        else:
            raise Exception(FILE_EXCEPTION)

    def file_mimesubtype_name(self):
        if self.is_file():
            return self._file_mimesubtype_name
        else:
            raise Exception(FILE_EXCEPTION)

    def file_mimedetector_id(self):
        if self.is_file():
            return self._file_mimedetector_id
        else:
            raise Exception(FILE_EXCEPTION)

    def file_mimedetails(self):
        if self.is_file():
            return self._file_mimedetails
        else:
            raise Exception(FILE_EXCEPTION)

    def file_name(self):
        if self.is_file():
            return self._file_name
        else:
            raise Exception(FILE_EXCEPTION)

    def file_extension(self):
        if self.is_file():
            return self._file_extension
        else:
            raise Exception(FILE_EXCEPTION)

    def file_size(self):
        if self.is_file():
            return self._file_size
        else:
            raise Exception(FILE_EXCEPTION)

    def file_attch_position(self):
        if self.is_file():
            if self.is_pstitem(): #only pst attachments have this
                return self._file_attch_position
            else:
                return -1
        else:
            raise Exception(FILE_EXCEPTION)
    
    # ------------- file item methods ---------------- #
    def extracted_text(self):
        if self.is_file():
            return self._extracted_text
        else:
            raise Exception(FILE_EXCEPTION)

    def extracted_chars(self):
        if self.is_file():
            return len(self._extracted_text)
        else:
            raise Exception(FILE_EXCEPTION) 
    
    # ------------- email item methods ------------------- #
    def is_reply(self):
        if self.is_email(): 
            return self._reply_to is not None
        else:               
            raise Exception(EMAIL_EXCEPTION)

    def reply_to(self):
        if self.is_email(): 
            return self._reply_to
        else:               
            raise Exception(EMAIL_EXCEPTION)

    def has_replies(self):
        if self.is_email(): 
            return len(self._replies) > 0
        else:               
            raise Exception(EMAIL_EXCEPTION)
    
    def replies(self):
        if self.is_email(): 
            return self._replies
        else:               
            raise Exception(EMAIL_EXCEPTION)
    
    def email_to(self):
        if self.is_email(): 
            return self._email_sentto_address
        else:               
            raise Exception(EMAIL_EXCEPTION)

    def email_cc(self):
        if self.is_email(): 
            return self._email_cc
        else:               
            raise Exception(EMAIL_EXCEPTION)

    def email_bcc(self):
        if self.is_email(): 
            return self._email_bcc
        else:               
            raise Exception(EMAIL_EXCEPTION)

    def email_date(self):
        if self.is_email(): 
            return self._email_date
        else:               
            raise Exception(EMAIL_EXCEPTION)

    def is_email_header_generated(self):
        if self.is_email(): 
            return self._is_email_header_generated
        else:               
            raise Exception(EMAIL_EXCEPTION)

    def email_header(self):
        if self.is_email(): 
            return self._email_header
        else:               
            raise Exception(EMAIL_EXCEPTION)

# --------------------------- private -------------------------- #
    def __init__(self, item_id):
        db = database.DbTool()
        db.open()
        self._load_item(item_id, db)
        self._load_properties(item_id, db)
        self._load_relationships(item_id, db)
        self._load_children(item_id, db)
        db.close()

        if self.is_file():
            self._load_file_data()
        if self.is_pstitem():
            self._load_common_pst_data()
        if self.is_email():
            self._load_email_data()

    def _load_item(self, item_id, db):
        di = db.get_dataitem(item_id)
        self._item_id                 = di[0]
        self._source_id               = di[1]
        self._source_name             = di[2]
        self._parent_id               = di[3]
        self._tree_level              = di[4]
        self._public_id               = di[5]
        self._redacttype_id           = di[6]
        self._origin_id               = di[7]
        self._psttype_id              = di[8]
        self._psttype_name            = di[9]
        self._pstfolder_id            = di[10]
        self._pstfolder_name          = di[11]
        self._conttype_id             = di[12]
        self._conttype_name           = di[13]
        self._cont_isextracted        = di[14]
        self._file_mimetype_id        = di[15]
        self._file_mimetype_name      = di[16]
        self._file_mimesubtype_id     = di[17]
        self._file_mimesubtype_name   = di[18]
        self._file_mimedetector_id    = di[19]
        self._file_mimedetails        = di[20]
        self._file_name               = di[21]
        self._file_extension          = di[22]
        self._file_size               = di[23]
        self._file_attch_position     = di[24]

    def _load_properties(self, item_id, db):
        self._metadata_dict = {}
        rows = db.get_itemproperties_by_item(item_id)
        for r in rows:
            prop_id    = r[0]
            prop_value = r[1]
            prop_name  = r[2]

            if prop_value is not None:
                prop_value = prop_value.strip() #strip it here

            self._metadata_dict[prop_id] = prop_value 

    def _load_relationships(self, item_id, db):
        self._duplicates = set()
        self._replies    = set()
        self._duplicate_of = None
        self._reply_to     = None

        rows = db.get_item_relationships_by_item1(item_id)
        for r in rows:
            reltype_id = r[0]
            item2_id   = r[1]
            
            if reltype_id == common.IS_DUPLICATE_RELTYPE_ID:
                self._duplicate_of = item2_id
            elif reltype_id == common.IS_REPLYTO_RELTYPE_ID:
                self._reply_to = item2_id

        rows = db.get_item_relationships_by_item2(item_id)
        for r in rows:
            item1_id   = r[0]
            reltype_id = r[1]
            
            if reltype_id == common.IS_DUPLICATE_RELTYPE_ID:
                self._duplicates.add(item1_id)
            elif reltype_id == common.IS_REPLYTO_RELTYPE_ID:
                self._replies.add(item1_id)

    def _load_children(self, item_id, db):
        self._children = set()
        rows = db.get_item_children(item_id)
        for r in rows:
            self._children.add(r[0])

    def _load_file_data(self):
        self._extracted_text = ""
        if property.EXTRACTED_TEXT_ID in self._metadata_dict:
            self._extracted_text = self._metadata_dict[property.EXTRACTED_TEXT_ID] 
    
    def _load_common_pst_data(self):
        self._pst_subject = ""
        self._pst_body = ""
        
        if property.PST_SUBJECT_ID in self._metadata_dict:
            self._pst_subject = self._metadata_dict[property.PST_SUBJECT_ID] 
        if property.PST_BODY_ID in self._metadata_dict:
            self._pst_body = self._metadata_dict[property.PST_BODY_ID] 

    def _load_email_data(self):
        self._email_sender_name = ''
        self._email_sender_address = ''
        self._email_sentto_address = '' 
        self._email_cc = '' 
        self._email_bcc = ''
        self._email_date = ''
        self._email_messageid = '' 
        self._email_importance = ''
        self._email_inreplyto = ''
        self._email_header = ''
        self._is_email_header_generated = False

        if property.PST_OUTLOOK_SENDER_NAME_ID in self._metadata_dict:
            self._email_sender_name = self._metadata_dict[property.PST_OUTLOOK_SENDER_NAME_ID] 
        if property.PST_SENDER_ADDRESS_ID in self._metadata_dict:
            self._email_sender_address = self._metadata_dict[property.PST_SENDER_ADDRESS_ID] 
        if property.PST_SENTTO_ADDRESS_ID in self._metadata_dict:
            self._email_sentto_address = self._metadata_dict[property.PST_SENTTO_ADDRESS_ID] 
        if property.PST_CC_ADDRESS_ID in self._metadata_dict:
            self._email_cc = self._metadata_dict[property.PST_CC_ADDRESS_ID] 
        if property.PST_BCC_ADDRESS_ID in self._metadata_dict:
            self._email_bcc = self._metadata_dict[property.PST_BCC_ADDRESS_ID] 
        if property.PST_DATE_ID in self._metadata_dict:
            self._email_date = self._metadata_dict[property.PST_DATE_ID] 
        if property.PST_MESSAGEID_ID in self._metadata_dict:
            self._email_messageid = self._metadata_dict[property.PST_MESSAGEID_ID] 
        if property.PST_IMPORTANCE_ID in self._metadata_dict:
            self._email_importance = self._metadata_dict[property.PST_IMPORTANCE_ID] 
        if property.PST_IN_REPLY_TO_ID in self._metadata_dict:
            self._email_inreplyto = self._metadata_dict[property.PST_IN_REPLY_TO_ID] 

        if property.PST_HEADER_ID in self._metadata_dict and self._metadata_dict[property.PST_HEADER_ID] != "":
            self._email_header = self._metadata_dict[property.PST_HEADER_ID] 
        else:
            self._email_header = self._generate_header()
            self._is_email_header_generated = True

    # -----------------------------------------------------------------------
    #    Format to build:
    #    From: "outlook_sender_name"  <sender_address>   [or sender2_address]
    #    To: sentto_address [simicolon-separated: emails or names
    #    Cc: cc_address
    #    Bcc: bcc_address
    #    Subject: subject
    #    Date: sent_date
    #    Message-ID: Message-ID
    #    Importance: importance
    #    In-Reply-To: <inreplyto??>
    # -----------------------------------------------------------------------
    def _generate_header(self):
        sb = []

        if len(self._email_sender_name) > 0 or len(self._email_sender_address) > 0:
            sb.append('\nFrom: ')

            if len(self._email_sender_name) > 0:

                delim = ''
                if len(self._email_sender_address) > 0 and '@' in self._email_sender_address: #check for a valid email!
                    delim = '"'

                sb.append('{1}{0}{1}'.format(self._email_sender_name, delim))

            if len(self._email_sender_address) > 0 and '@' in self._email_sender_address: #check for a valid email!
                sb.append(' <{0}>'.format(self._email_sender_address))

        if len(self._email_sentto_address) > 0:
            sb.append('\nTo: {0}'.format(self._email_sentto_address))
        
        if len(self._email_cc) > 0:
            sb.append('\nCc: {0}'.format(self._email_cc))

        if len(self._email_bcc) > 0:
            sb.append('\nBcc: {0}'.format(self._email_bcc))

        if len(self._pst_subject) > 0:
            sb.append('\nSubject: {0}'.format(self._pst_subject))

        if len(self._email_date) > 0:
            sb.append('\nDate: {0}'.format(self._email_date))

        if len(self._email_messageid) > 0:
            sb.append('\nMessage-ID: {0}'.format(self._email_messageid))
        
        if len(self._email_importance) > 0:
            sb.append('\nImportance: {0}'.format(self._email_importance))
        
        if len(self._email_inreplyto) > 0:
            sb.append('\nIn-Reply-To: {0}'.format(self._email_inreplyto))

        return ''.join(sb)


if __name__ == '__main__': main()
