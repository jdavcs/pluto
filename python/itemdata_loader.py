import os.path
import sys
import time
from shared import common
from shared import database


def main():
    db = database.DbTool()
    db.open()

    delim = ' ||| '

    #init property_ids for properties we'll need
    pid_body = 1 
    pid_header = 18 
    pid_outlook_sender_name = 35
    pid_sender_address = 54
    pid_sentto_address = 57
    pid_cc_address = 14
    pid_bcc_address = 13
    pid_date = 65
    pid_subject = 9
    pid_message_id = 24
    pid_importance = 60 
    pid_in_reply_to = 20
    pid_extr_text = 188 
    
    #load email item ids
    emails = set()
    pstitems = db.get_pstitems()
    for pi in pstitems:
        item_id = pi[0]
        psttype_id = pi[1]
        if psttype_id == common.PSTTYPE_NOTE:
            emails.add(item_id)

    #get all items
    items = db.get_items()
    is_email = False
    count = 1
    total = len(items)
    for i in items:
        item_id = i[0]

        if (count % 100 == 0):
            print "Processing item {0} of {1} [{2}]".format(count, total, item_id)
            db.commit()  #commit every 100 items
        count += 1

        is_email = item_id in emails #check if item is an email

        #init empty dictionary
        prop_dict = {} #key = property_id, value = item_property value

        #init empty named properties
        email_from = ""
        email_to = ""
        email_cc = ""
        email_bcc = ""
        email_date = ""
        email_subject = ""
        email_header = ""
        
        pst_body = ""
        extr_text = ""
        metadata = [] #all properties excluding body and extr_text       
        
        #get all properties for each item and load into dictionary (we don't care for prop_name at ip[0])
        ips = db.get_itemproperties_by_item(item_id);
        for ip in ips:
            prop_value = ip[1]
            prop_id = ip[0]
            prop_dict[prop_id] = prop_value

        #build the values: load extr text if not email, otherwise - load email values. Load body and meta data for all
        if not is_email: 
            if pid_extr_text in prop_dict: 
                extr_text = prop_dict[pid_extr_text]
        else:
            if pid_outlook_sender_name in prop_dict: 
                email_from = prop_dict[pid_outlook_sender_name]
            if pid_sender_address in prop_dict: 
                email_from = email_from + ", " + prop_dict[pid_sender_address]
    
            if pid_sentto_address in prop_dict: 
                email_to = prop_dict[pid_sentto_address]

            if pid_cc_address in prop_dict: 
                email_cc = prop_dict[pid_cc_address]
        
            if pid_bcc_address in prop_dict: 
                email_bcc = prop_dict[pid_bcc_address]
                
            if pid_date in prop_dict: 
                email_date = make_date(prop_dict[pid_date]) #convert to date

            if pid_subject in prop_dict: 
                email_subject = prop_dict[pid_subject]
        
            if pid_header in prop_dict: 
                email_header = prop_dict[pid_header]

            if email_header == "":
                email_header = build_header(prop_dict)
            
        #load metadata            
        for pid in prop_dict:
            if pid != pid_body and pid != pid_extr_text:
                if prop_dict[pid] is not None:
                    metadata.append(prop_dict[pid])

        #load body (loads for pst and nonpst items - not a problem)
        if pid_body in prop_dict: 
            pst_body = prop_dict[pid_body]


        #load into db for this item
        text = email_header + delim + pst_body + delim + extr_text

        meta = ""
        if len(metadata) > 0:
            meta = delim.join(metadata)

        db.create_item_all_data(item_id, text, meta)

        if not is_email:
            db.create_item_nonemail_data(item_id, text, meta)
        else:
            db.create_item_email_data(
                item_id, email_from, email_to, email_cc, email_bcc, email_date, email_subject, email_header, pst_body, meta)

        #MUST RESET THESE!!!
        text = "" 
        meta = ""

    db.commit() 
    db.close()


#quick fix
def make_date(date):
    return date.replace('T', ' ')[:-1]


def build_header(metadata_dict):
#    From: "outlook_sender_name"  <sender_address>   [or sender2_address]
#    To: sentto_address [simicolon-separated: emails or names. if name - then email is in system?: later on figure out the mapping] 
#    Cc: cc_address
#    Bcc: bcc_address
#    Subject: subject
#    Date: sent_date
#    Message-ID: Message-ID
#    Importance: importance
#    In-Reply-To: <inreplyto??>

    pid_outlook_sender_name = 35
    pid_sender_address = 54
    pid_sentto_address = 57
    pid_cc_address = 14
    pid_bcc_address = 13
    pid_subject = 9
    pid_date = 65
    pid_message_id = 24
    pid_importance = 60 
    pid_in_reply_to = 20

    outlook_sender_name = ''
    sender_address = ''
    sentto_address = ''
    cc_address = ''
    bcc_address = ''
    subject = ''
    date = ''
    message_id = ''
    importance = '' 
    in_reply_to = ''

    if pid_outlook_sender_name in metadata_dict: 
        outlook_sender_name = metadata_dict[pid_outlook_sender_name]
    if pid_sender_address in metadata_dict: 
        sender_address = metadata_dict[pid_sender_address]
    if pid_sentto_address in metadata_dict: 
        sentto_address = metadata_dict[pid_sentto_address]
    if pid_cc_address in metadata_dict:  
        cc_address = metadata_dict[pid_cc_address]
    if pid_bcc_address in metadata_dict:  
        bcc_address = metadata_dict[pid_bcc_address]
    if pid_subject in metadata_dict:  
        subject = metadata_dict[pid_subject]
    if pid_date in metadata_dict:  
        date = metadata_dict[pid_date]
    if pid_message_id in metadata_dict:  
        message_id = metadata_dict[pid_message_id]
    if pid_importance in metadata_dict:  
        importance = metadata_dict[pid_importance]
    if pid_in_reply_to in metadata_dict:  
        in_reply_to = metadata_dict[pid_in_reply_to]


    #build header
    sb = []

    if len(outlook_sender_name) > 0 or len(sender_address) > 0:
        sb.append('\nFrom: ')
        if len(outlook_sender_name) > 0:

            delim = ''
            if len(sender_address) > 0 and '@' in sender_address: #check for a valid email!
                delim = '"'

            sb.append('{1}{0}{1}'.format(outlook_sender_name, delim))

        if len(sender_address) > 0 and '@' in sender_address: #check for a valid email!
            sb.append(' <{0}>'.format(sender_address))

    if len(sentto_address) > 0:
        sb.append('\nTo: {0}'.format(sentto_address))
    
    if len(cc_address) > 0:
        sb.append('\nCc: {0}'.format(cc_address))

    if len(bcc_address) > 0:
        sb.append('\nBcc: {0}'.format(bcc_address))

    if len(subject) > 0:
        sb.append('\nSubject: {0}'.format(subject))

    if len(date) > 0:
        sb.append('\nDate: {0}'.format(date))

    if len(message_id) > 0:
        sb.append('\nMessage-ID: {0}'.format(message_id))
    
    if len(importance) > 0:
        sb.append('\nImportance: {0}'.format(importance))
    
    if len(in_reply_to) > 0:
        sb.append('\nIn-Reply-To: {0}'.format(in_reply_to))

    return ''.join(sb)


if __name__ == '__main__': main()
