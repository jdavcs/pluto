import os.path
import random
import re
import sys
import time
from shared import common
from shared import database


class RedactCC(object):

    VISA = 1
    MC   = 2
    AMEX = 3
    DIN  = 4
    DISC = 5
    JCB  = 6

    def __init__(self):
        self._dict_redact = {} #dictionary: original_string >> generated_string
        self._dict_redactid = {} #dictionary: generated_string >> redaction_id
        self._redactitems = set() #set of items with redacted content
        self._db = database.DbTool()
        random.seed(835291) 
        self._init_regex()

    def _init_regex(self):
        #sequence of digits
        pattern1 = r'\b(?:\d[ -]??){13,16}\b' #matches one dash/space at most = reduces false positives
        
        pattern_cc1 = r'^4[0-9]{12}(?:[0-9]{3})?$' #visa
        pattern_cc2 = r'^5[1-5][0-9]{14}$' #mc
        pattern_cc3 = r'^3[47][0-9]{13}$' #amex
        pattern_cc4 = r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$' #diners
        pattern_cc5 = r'^6(?:011|5[0-9]{2})[0-9]{12}$' #discover
        pattern_cc6 = r'^(?:2131|1800|35\d{3})\d{11}$' #jcb

        self._regex_digits = re.compile(pattern1) #checks digits
    
        self._regex_cc1 = re.compile(pattern_cc1) 
        self._regex_cc2 = re.compile(pattern_cc2) 
        self._regex_cc3 = re.compile(pattern_cc3) 
        self._regex_cc4 = re.compile(pattern_cc4) 
        self._regex_cc5 = re.compile(pattern_cc5) 
        self._regex_cc6 = re.compile(pattern_cc6) 

    def run(self):
        timer_start = time.time()
        self._db.open()
        self._redact()
        self._db.commit() #final commit just in case
        self._db.close()
        print common.display_elapsed(timer_start, "cc redaction")

    def _redact(self):
        items = self._db.get_items()
        total = len(items)
        counter = 1

        for i in items:
            item_id = i[0]

            if (counter % 10000 == 0):
                print "Processing item {0} of {1}: {2}".format(counter, total, item_id)
            counter += 1

            self._scan_item(item_id)

    def _scan_item(self, item_id):
        item_properties = self._db.get_itemproperties_by_item(item_id)
        for ip in item_properties:
            property_id = ip[0]
            value = str(ip[1])
            name = ip[2]           

            if property_id == 24 or property_id == 470: #ignore messageId and edit-time 
                continue

            #check for sequence of digits
            if self._regex_digits.search(value):
                self._scan_property(item_id, property_id, value)

    def _scan_property(self, item_id, property_id, value):
        matches = self._regex_digits.findall(value)
        for m in matches:
            digits_raw = ''.join(m)

            #get rid of dashes and spaces
            digits = digits_raw.replace(' ', '')
            digits = digits.replace('-', '')

            #check for correct format
            cctype = ""
            if self._regex_cc1.match(digits):
                cctype = RedactCC.VISA
            elif self._regex_cc2.match(digits):
                cctype = RedactCC.MC
            if self._regex_cc3.match(digits):
                cctype = RedactCC.AMEX
            if self._regex_cc4.match(digits):
                cctype = RedactCC.DIN
            if self._regex_cc5.match(digits):
                cctype = RedactCC.DISC
            if self._regex_cc6.match(digits):
                cctype = RedactCC.JCB

            if cctype != "":
                #check luhn algorithm
                if self._luhn(digits):
                    self._redact_string(item_id, property_id, digits, cctype)

    def _redact_string(self, item_id, property_id, str_old, cctype):
        if str_old in self._dict_redact:
            str_new = self._dict_redact[str_old]
            redaction_id = self._dict_redactid[str_new]
        else:
            str_new = self._generate_str(str_old, cctype, 1)
            self._dict_redact[str_old] = str_new
            
            redaction_id = self._db.create_redaction(common.REDACTRULE_CC, str_old, str_new)
            self._dict_redactid[str_new] = redaction_id

        self._db.create_item_redaction(item_id, redaction_id, property_id)
        self._db.set_item_redacttype(item_id, common.REDACTTYPE_CONTENT)

    def _luhn(self, digits):
        r = [int(ch) for ch in str(digits)][::-1]
        return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0

    def _generate_str(self, str_old, cctype, iteration):
        #sanity check: look like we are in a permanent loop!
        if iteration > 100:
            print "HOUSTON: WE HAVE A random number generation PROBLEM!"
            sys.exit()

        if cctype == RedactCC.VISA:            
            if len(str_old) == 16:
                str_new = "4" + str(random.randint(0, 999999999999999)).zfill(15)
            else:
                str_new = "4" + str(random.randint(0, 999999999999)).zfill(12)
        elif cctype == RedactCC.MC:
            str_new = "53" + str(random.randint(0, 99999999999999)).zfill(14)
        elif cctype == RedactCC.AMEX:
            str_new = "34" + str(random.randint(0, 9999999999999)).zfill(13)
        elif cctype == RedactCC.DIN:
            str_new = "302" + str(random.randint(0, 99999999999)).zfill(11)
        elif cctype == RedactCC.DISC:
            str_new = "6011" + str(random.randint(0, 999999999999)).zfill(12)
        elif cctype == RedactCC.JCB:
            if len(str_old) == 16:
                str_new = "2131" + str(random.randint(0, 99999999999)).zfill(11)
            else:
                str_new = "35" + str(random.randint(0, 99999999999999)).zfill(14)

        if str_new in self._dict_redactid: #str-new must be unique > repeat!
            iteration += 1
            return self._generate_str(str_old, cctype, iteration)
        else:
            return str_new
