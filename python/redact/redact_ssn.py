import os.path
import random
import re
import sys
import time
from shared import common
from shared import database


class RedactSSN(object):

    def __init__(self):
        self._dict_redact = {} #dictionary: original_string >> generated_string
        self._dict_redactid = {} #dictionary: generated_string >> redaction_id
        self._redactitems = set() #set of items with redacted content
        self._db = database.DbTool()
        random.seed(145567) #just a safeguard

    def run(self):
        timer_start = time.time()
    
        self._db.open()
        self._redact()
        self._db.commit() #final commit just in case
        self._db.close()

        print common.display_elapsed(timer_start, "ssn redaction")

    def _redact(self):
        ssn_1 = r'\b(?!000|666)(?:[0-6][0-9]{2}|7(?:[0-6][0-9]|7[0-2]))-(?!00)[0-9]{2}-(?!0000)[0-9]{4}\b' #ssn with dashes
        ssn_2 = r'\b(?!000|666)(?:[0-6][0-9]{2}|7(?:[0-6][0-9]|7[0-2]))(?!00)[0-9]{2}(?!0000)[0-9]{4}\b' #ssn without dashes
        ssn_c = r'(\bssn\b)|(\bss#\b)|(\bsocial security\b)' #relevant context

        p_ssn1 = re.compile(ssn_1)
        p_ssn2 = re.compile(ssn_2)
        p_ssnc = re.compile(ssn_c, re.IGNORECASE)
    
        items = self._db.get_items()
    
        total = len(items)
        counter = 1

        for i in items:
            item_id = i[0]

            if (counter % 10000 == 0):
                print "Processing item {0} of {1}: {2}".format(counter, total, item_id)
            counter += 1

            self._scan_item(item_id, p_ssn1, p_ssn2, p_ssnc)

    def _scan_item(self, item_id, p_ssn1, p_ssn2, p_ssnc):
        has_ssn = False
    
        item_properties = self._db.get_itemproperties_by_item(item_id)
        for ip in item_properties:
            property_id = ip[0]
            value = str(ip[1])
            name = ip[2]           

            #check pattern with dashes
            if p_ssn1.search(value):
                has_ssn = True
                self._scan_text(value, p_ssn1, item_id, property_id)

            #check pattern without dashes
            if p_ssn2.search(value): #found potential matches for ssn: must check each line
                lines = value.splitlines()
                for line in lines: 
                    if p_ssnc.search(line) and p_ssn2.search(line): #context and ssn occur in the same line!
                        has_ssn = True
                        self._scan_text(line, p_ssn2, item_id, property_id)

        if has_ssn:
            self._db.set_item_redacttype(item_id, common.REDACTTYPE_CONTENT)

    def _scan_text(self, text, pattern, item_id, property_id):
        matches = pattern.findall(text)
        for m in matches:
            str_old = ''.join(m)
            str_new = self._redact_string(str_old, item_id, property_id)

    def _redact_string(self, str_old, item_id, property_id):
        if str_old in self._dict_redact:
            str_new = self._dict_redact[str_old]
            redaction_id = self._dict_redactid[str_new]
        else:
            str_new = self._generate_str(str_old, 1)
            self._dict_redact[str_old] = str_new
            
            redaction_id = self._db.create_redaction(common.REDACTRULE_SSN, str_old, str_new)
            self._dict_redactid[str_new] = redaction_id

        self._db.create_item_redaction(item_id, redaction_id, property_id)

    def _generate_str(self, str_old, iteration):
        #santity check: look like we are in a permanent loop!
        if iteration > 100:
            print "HOUSTON: WE HAVE A random number generation PROBLEM!"
            sys.exit()

        str1 = str(random.randint(1, 665)).zfill(3)
        str2 = str(random.randint(1, 99)).zfill(2)
        str3 = str(random.randint(1, 9999)).zfill(4)

        if '-' in str_old: #generate ssn with dashes
            str_new = "{0}-{1}-{2}".format(str1, str2, str3)
        else: #generate without daches
            str_new = "{0}{1}{2}".format(str1, str2, str3)

        if str_new in self._dict_redactid: #str-new must be unique > repeat!
            iteration += 1
            return self._generate_str(str_old, iteration)
        else:
            return str_new
