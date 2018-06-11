from shared import database

PST_BODY_ID                 = 1 
PST_SUBJECT_ID              = 9
PST_HEADER_ID               = 18
PST_OUTLOOK_SENDER_NAME_ID  = 35
PST_SENDER_ADDRESS_ID       = 54
PST_SENTTO_ADDRESS_ID       = 57
PST_CC_ADDRESS_ID           = 14
PST_BCC_ADDRESS_ID          = 13
PST_SUBJECT_ID              = 9
PST_DATE_ID                 = 65
PST_MESSAGEID_ID            = 24
PST_IMPORTANCE_ID           = 60
PST_IN_REPLY_TO_ID          = 20
EXTRACTED_TEXT_ID           = 188


class PropertyRepository(object):
    
    def get_id(self, name):
        if name in self._id_by_name_dict:
            return self._id_by_name_dict[name]
        else:
            raise Exception("Unknown property name: " + str(name))

    def get_name(self, id):
        if id in self._name_by_id_dict:
            return self._name_by_id_dict[id]
        else:
            raise Exception("Unknown property id: " + str(id))

# --------------------- private ---------------------- #
    def __init__(self):
        self._id_by_name_dict = {}
        self._name_by_id_dict = {}
        self._load()

    def _load(self):
        db = database.DbTool()
        db.open()

        rows = db.get_properties()
        for r in rows:
            prop_id   = r[0]
            type_id   = r[1]
            prop_name = r[2]
            self._id_by_name_dict[prop_name] = prop_id
            self._name_by_id_dict[prop_id] = prop_name

        db.close()
