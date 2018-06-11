import os.path
import subprocess
import config
import time
import math
import re

#for all ITEMTYPE: values must be the same as in database

#containers:
CONTAINERTYPE_PST = 1
CONTAINERTYPE_ZIP = 2
CONTAINERTYPE_GZIP = 3
CONTAINERTYPE_TAR = 4
CONTAINERTYPE_JAR = 5

#psttype codes: 
PSTTYPE_NOTE = 1
PSTTYPE_SCHEDULE = 2
PSTTYPE_APPOINTMENT = 3
PSTTYPE_CONTACT = 4
PSTTYPE_JOURNAL = 5
PSTTYPE_STICKYNOTE = 6
PSTTYPE_TASK = 7
PSTTYPE_OTHER = 8
PSTTYPE_REPORT = 9
PSTTYPE_ATTACHMENT = 10

#propertytype codes:
PROPERTYTYPE_PSTITEM_NOTE = 1
PROPERTYTYPE_PSTITEM_SCHEDULE = 2
PROPERTYTYPE_PSTITEM_APPOINTMENT = 3
PROPERTYTYPE_PSTITEM_CONTACT = 4
PROPERTYTYPE_PSTITEM_JOURNAL = 5
PROPERTYTYPE_PSTITEM_STICKYNOTE = 6
PROPERTYTYPE_PSTITEM_TASK = 7
PROPERTYTYPE_PSTITEM_OTHER = 8
PROPERTYTYPE_PSTITEM_REPORT = 9
PROPERTYTYPE_PSTITEM_ATTACHMENT = 10
PROPERTYTYPE_PSTITEM_ALL = 11
PROPERTYTYPE_FILEITEM = 12

CONFIG_FILE_NAME = 'config.properties'

MIME_PATTERN_PST = 'Microsoft Outlook email folder'

EXT_PST = ".pst"

IS_DUPLICATE_RELTYPE_ID = 1
IS_REPLYTO_RELTYPE_ID = 2

DELIMITER = " [[pluto-delim]] "

REDACTTYPE_NONE = 1
REDACTTYPE_FULL = 2
REDACTTYPE_CONTENT= 3

REDACTRULE_CC = 1
REDACTRULE_SSN = 3

PST_ROOT_FOLDER_NAME='PST_ROOT_FOLDER'


def get_source_dir(source_id):
    return str(source_id).zfill(3)


def get_path_files_processed():
    cnf = config.ConfigReader()
    return "{0}{1}".format(cnf.get('OUTPUT_ROOT'), cnf.get('PROCESSED_FILES_RELPATH'))


def get_path_files_processed_source(src_id):
    cnf = config.ConfigReader()
    return "{0}{1}{2}/".format(cnf.get('OUTPUT_ROOT'), cnf.get('PROCESSED_FILES_RELPATH'), src_id)


def get_path_files_processed_item(src_id, item_id, extension):
    cnf = config.ConfigReader()
    return "{0}{1}{2}/{3}{4}".format(cnf.get('OUTPUT_ROOT'), cnf.get('PROCESSED_FILES_RELPATH'), src_id, item_id, extension)


def get_path_files_original():
    cnf = config.ConfigReader()
    return "{0}{1}".format(cnf.get('OUTPUT_ROOT'), cnf.get('ORIGINAL_FILES_RELPATH'))


def get_path_files_original_container(container_id):
    cnf = config.ConfigReader()
    return "{0}{1}{2}/".format(cnf.get('OUTPUT_ROOT'), cnf.get('ORIGINAL_FILES_RELPATH'), container_id)


def get_path_pstitems_text():
    cnf = config.ConfigReader()
    return "{0}{1}".format(cnf.get('OUTPUT_ROOT'), cnf.get('PSTITEMS_TEXT_RELPATH'))


def get_path_files_text():
    cnf = config.ConfigReader()
    return "{0}{1}".format(cnf.get('OUTPUT_ROOT'), cnf.get('FILES_TEXT_RELPATH'))


def get_path_tikalogs():
    cnf = config.ConfigReader()
    return "{0}{1}".format(cnf.get('OUTPUT_ROOT'),cnf.get('TIKA_LOG_RELPATH'))


def get_propertytype_by_psttype(psttype_id):
    if psttype_id == PSTTYPE_NOTE:
        return PROPERTYTYPE_PSTITEM_NOTE
    elif psttype_id == PSTTYPE_SCHEDULE:
        return PROPERTYTYPE_PSTITEM_SCHEDULE
    elif psttype_id == PSTTYPE_APPOINTMENT:
        return PROPERTYTYPE_PSTITEM_APPOINTMENT
    elif psttype_id == PSTTYPE_CONTACT:
        return PROPERTYTYPE_PSTITEM_CONTACT
    elif psttype_id == PSTTYPE_JOURNAL:
        return PROPERTYTYPE_PSTITEM_JOURNAL
    elif psttype_id == PSTTYPE_STICKYNOTE:
        return PROPERTYTYPE_PSTITEM_STICKYNOTE
    elif psttype_id == PSTTYPE_TASK:
        return PROPERTYTYPE_PSTITEM_TASK
    elif psttype_id == PSTTYPE_OTHER:
        return PROPERTYTYPE_PSTITEM_OTHER
    elif psttype_id == PSTTYPE_REPORT:
        return PROPERTYTYPE_PSTITEM_REPORT
    elif psttype_id == PSTTYPE_ATTACHMENT:
        return PROPERTYTYPE_PSTITEM_ATTACHMENT
    else:
        print "ERROR: wrong psttype_id: " + str(psttype_id)
        sys.exit()


def get_containertype(mimetype, submimetype, mimedetails):
    if mimetype != "application":
        return -1

    if submimetype == "zip" or submimetype == "x-zip-compressed":
        return CONTAINERTYPE_ZIP
    elif submimetype == "x-gzip" or submimetype == "x-tar-gz" or submimetype == "x-tgz":
        return CONTAINERTYPE_GZIP
    elif submimetype == "tar" or submimetype == "x-tar" or submimetype == "x-gtar":
        return CONTAINERTYPE_TAR
    elif submimetype == "java-archive" or submimetype == "x-java-archive":
        return CONTAINERTYPE_JAR
    elif MIME_PATTERN_PST in mimedetails:
        return CONTAINERTYPE_PST
    else:
        return -1


def exec_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, bufsize=-1, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.communicate()


def display_elapsed(time_start, operation):
    s = time.time() - time_start
    if s < 60:
        s = math.ceil(s)
        return "{0}: {1} seconds".format(operation, s)
    elif s < 3600:
        m = math.floor(s/60)
        s = s - m * 60
        s = math.ceil(s)
        return "{0}: {1} minutes {2} seconds".format(operation, m, s)
    else:
        m = math.floor(s/60)
        s = s - m * 60
        s = math.ceil(s)
        h = math.floor(m/60)
        m = m - h * 60
        return "{0}: {1} hours {2} minutes {3} seconds".format(operation, h, m, s)


def format_size(bytes):
    types = ('', 'KB', 'MB', 'GB', 'TB')
    pos = 0
    while bytes >= 1024:
        bytes /= 1024.0
        pos += 1
    
    bytes = round(bytes, 1)
    if bytes % 1 == 0:
        bytes = int(bytes)
    
    return str(bytes) + types[pos]


def xml_filter_encoding(text): #encode
    if text is not None:
        illegal_xml_re = re.compile(
                u'[\x00-\x08\x0b-\x1f\x7f-\x84\x86-\x9f\ud800-\udfff\ufdd0-\ufddf\ufffe-\uffff]')
        text = illegal_xml_re.sub('', text)
        text = unicode(text, errors = 'ignore')
        text = text.decode()
        return text
    else:
        return ''


def xml_filter_element_name(text): #replace all non-alphanumerics with underscores
    filtered = []
    for c in text:
        if c.isalnum(): 
            filtered.append(c)
        else: 
            filtered.append('_')
    return ''.join(filtered)


def xml_filter_cdata(text, closing_indent):
    if "\n" in text or "<" in text or ">" in text or "&" in text or "'" in text or "\"" in text:
        if "]]>" in text: 
            text = text.replace("]]>", "[ ] ] > ]")
        if '\n' in text:
            return '<![CDATA[\n\n{0}\n\n{1}]]>'.format(text, closing_indent)
        else:
            return '<![CDATA[{0}]]>'.format(text)
    else:
        return text


def get_tabs(level, tab):
    sb = []
    while level > 0:
        sb.append(tab)
        level -= 1
    return ''.join(sb)
