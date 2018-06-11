import os.path
import sys
import time
import hashlib
from shared import common
from shared import database


def run():
    
    db = database.DbTool()
    db.open()

    sql = "SELECT item_id, '', email_from, email_date, email_body FROM data_email_items where item_id not in (select item_id from data_dedup_hash)"    
    rows = db.get_records(sql)
    count = 0
    total = len(rows)
    for r in rows:
        item_id = r[0]
        m       = str(r[1]) #messageid
        f       = str(r[2]) #from (outlook_sender_name and outlook_sender_address)
        d       = str(r[3]) #date (sent_date)
        b       = str(r[4]) #body

        if m is None: m = ''
        if f is None: f = ''
        if d is None: d = ''
        if b is None: b = ''

        if count % 1000 == 0:
            print "Processing pstitem {0} of {1} [item_id {2}]".format(count, total, item_id)
            db.commit()
        count += 1

        #0000 = mbfd
        text_0001 = d
        text_0010 = f
        text_0011 = f + '\n' + d
        text_0100 = b
        text_0101 = b + '\n' + d
        text_0110 = b + '\n' + f
        text_0111 = b + '\n' + f + '\n' + d
        text_1000 = m
        text_1001 = m + '\n' + d
        text_1010 = m + '\n' + f
        text_1011 = m + '\n' + f + '\n' + d
        text_1100 = m + '\n' + b
        text_1101 = m + '\n' + b + '\n' + d
        text_1110 = m + '\n' + b + '\n' + f
        text_1111 = m + '\n' + b + '\n' + f + '\n' + d

        hash_0001 = hashlib.md5(text_0001).hexdigest()
        hash_0010 = hashlib.md5(text_0010).hexdigest()
        hash_0011 = hashlib.md5(text_0011).hexdigest()
        hash_0100 = hashlib.md5(text_0100).hexdigest()
        hash_0101 = hashlib.md5(text_0101).hexdigest()
        hash_0110 = hashlib.md5(text_0110).hexdigest()
        hash_0111 = hashlib.md5(text_0111).hexdigest()
        hash_1000 = hashlib.md5(text_1000).hexdigest()
        hash_1001 = hashlib.md5(text_1001).hexdigest()
        hash_1010 = hashlib.md5(text_1010).hexdigest()
        hash_1011 = hashlib.md5(text_1011).hexdigest()
        hash_1100 = hashlib.md5(text_1100).hexdigest()
        hash_1101 = hashlib.md5(text_1101).hexdigest()
        hash_1110 = hashlib.md5(text_1110).hexdigest()
        hash_1111 = hashlib.md5(text_1111).hexdigest()
       
        db.create_data_dedup_hash(item_id, hash_0001, hash_0010, hash_0011, hash_0100, hash_0101, hash_0110, hash_0111, hash_1000, hash_1001, hash_1010, hash_1011, hash_1100, hash_1101, hash_1110, hash_1111)

    db.commit()
    db.close()
