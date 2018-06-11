import sys
import os.path
import _libpst
from shared import common
from pst_attachment_reader import PstAttachmentReader


class PstItemReader(object):

    def __init__(self, db, pst, src_id, property_dic, batch):
        self._db = db
        self._pst = pst
        self._src_id = src_id
        self._property_dic = property_dic
        self._pids = set()  #extracted and stored properties
        self._batch = batch

    def read(self, pst_item, parent_item_id, folder_id, level):
        self._type = self._get_type(pst_item.type)      
        self._item_id = self._db.create_item(self._src_id, parent_item_id, level)
        self._propertytype_id = common.get_propertytype_by_psttype(self._type)

        self._db.create_pstitem(self._item_id, self._type, folder_id)

        if self._item_id % 100 == 0:
            print "reading item_id " + str(self._item_id)

        if pst_item.extra_fields is not None:
            self._read_extra_fields(pst_item.extra_fields)

        if pst_item.flags is not None:
            self._read_field("flags", pst_item.flags, common.PROPERTYTYPE_PSTITEM_ALL)

        self._read_common_fields(pst_item)

        #these pst types have additional fields we know how to extract >> therefore, call these methods.
        if self._type == 1 and pst_item.email is not None:
            self._read_email_fields(pst_item.email)
        elif self._type == 3 and pst_item.appointment is not None:
            self._read_appointment_fields(pst_item.appointment)
        elif self._type == 4 and pst_item.contact is not None:
            self._read_contact_fields(pst_item.contact)
        elif self._type == 5 and pst_item.journal is not None:
            self._read_journal_fields(pst_item.journal)

        #process attachments
        if pst_item.attach is not None:
            reader = PstAttachmentReader(
                self._db, self._pst, self._src_id, self._item_id, level+1, folder_id, self._property_dic, self._batch)
            reader.read(pst_item.attach)

    def _read_extra_fields(self, field):
        self._read_extra_field(field.field_name, field.value)
        if field.next is not None:
            self._read_extra_fields(field.next)

    def _get_type(self, type):
        if type == 1: return common.PSTTYPE_NOTE
        elif type == 2: return common.PSTTYPE_SCHEDULE
        elif type == 8: return common.PSTTYPE_APPOINTMENT
        elif type == 9: return common.PSTTYPE_CONTACT
        elif type == 10: return common.PSTTYPE_JOURNAL
        elif type == 11: return common.PSTTYPE_STICKYNOTE
        elif type == 12: return common.PSTTYPE_TASK
        elif type == 13: return common.PSTTYPE_OTHER
        elif type == 14: return common.PSTTYPE_REPORT
        else:
            print "UNKNOWN TYPE: ", type
            sys.exit() #must halt: modify code to handle this type.

    def _read_common_fields(self, item):
        #override property type for these properties because they are common for all pst items
        ptid = common.PROPERTYTYPE_PSTITEM_ALL 
        
        self._read_field("body", item.body.str, ptid)        
        self._read_field("body_charset", item.body_charset.str, ptid)
        self._read_field("comment", item.comment.str, ptid)
        self._read_field("file_as", item.file_as.str, ptid)
        self._read_field("outlook_version", item.outlook_version.str, ptid)
        self._read_field("subject", item.subject.str, ptid)
        self._read_field("response_requested", item.response_requested, ptid)

        if item.create_date is not None:
            self._read_field("create_date", 
                self._pst.pst_rfc2425_datetime_format(item.create_date), ptid)

        if item.modify_date is not None:
            self._read_field("modify_date", 
                self._pst.pst_rfc2425_datetime_format(item.modify_date), ptid)

    def _read_email_fields(self, item):
        self._read_field("bcc_address", item.bcc_address.str)
        self._read_field("cc_address", item.cc_address.str)
        self._read_field("conversion_prohibited", item.conversion_prohibited)
        self._read_field("delete_after_submit", item.delete_after_submit)
        self._read_field("delivery_report", item.delivery_report)
        self._read_field("header", item.header.str)
        self._read_field("htmlbody", item.htmlbody.str)
        self._read_field("in_reply_to", item.in_reply_to.str)
        self._read_field("message_cc_me", item.message_cc_me)
        self._read_field("message_recip_me", item.message_recip_me)
        self._read_field("message_to_me", item.message_to_me)
        self._read_field("messageid", item.messageid.str)
        self._read_field("ndr_diag_code", item.ndr_diag_code)
        self._read_field("ndr_reason_code", item.ndr_reason_code)
        self._read_field("ndr_status_code", item.ndr_status_code)
        self._read_field("original_bcc", item.original_bcc.str)
        self._read_field("original_cc", item.original_cc.str)
        self._read_field("original_to", item.original_to.str)
        self._read_field("outlook_recipient", item.outlook_recipient.str)
        self._read_field("outlook_recipient_name", item.outlook_recipient_name.str)
        self._read_field("outlook_recipient2", item.outlook_recipient2.str)
        self._read_field("outlook_sender", item.outlook_sender.str)
        self._read_field("outlook_sender_name", item.outlook_sender_name.str)
        self._read_field("outlook_sender2", item.outlook_sender2.str)
        self._read_field("processed_subject", item.processed_subject.str)
        self._read_field("read_receipt", item.read_receipt)
        self._read_field("recip_access", item.recip_access.str)
        self._read_field("recip_address", item.recip_address.str)
        self._read_field("recip2_access", item.recip2_access.str)
        self._read_field("recip2_address", item.recip2_address.str)
        self._read_field("reply_requested", item.reply_requested)
        self._read_field("reply_to", item.reply_to.str)
        self._read_field("report_text", item.report_text.str)
        self._read_field("return_path_address", item.return_path_address.str)
        self._read_field("rtf_body_char_count", item.rtf_body_char_count)
        self._read_field("rtf_body_crc", item.rtf_body_crc)
        self._read_field("rtf_body_tag", item.rtf_body_tag.str)
        self._read_field("rtf_in_sync", item.rtf_in_sync)
        self._read_field("rtf_ws_prefix_count", item.rtf_ws_prefix_count)
        self._read_field("rtf_ws_trailing_count", item.rtf_ws_trailing_count)
        self._read_field("sender_access", item.sender_access.str)
        self._read_field("sender_address", item.sender_address.str)
        self._read_field("sender2_access", item.sender2_access.str)
        self._read_field("sender2_address", item.sender2_address.str)
        self._read_field("sentto_address", item.sentto_address.str)
        self._read_field("supplementary_info", item.supplementary_info.str)

        if item.autoforward == 1:
            autoforward = "1"
        elif item.autoforward == -1:
            autoforward = 0
        else:
            autoforward = ""
        self._read_field("autoforward", autoforward)
        
        if item.importance == 0:
            importance = "low"
        elif item.importance == 1:
            importance = "normal"
        elif item.importance == 2:
            importance = "high"
        self._read_field("importance", importance)
       
        if item.original_sensitivity == 0:
            orig_sen = "none"
        elif item.original_sensitivity == 1:
            orig_sen = "personal"
        elif item.original_sensitivity == 2:
            orig_sen = "private"
        elif item.original_sensitivity == 3:
            orig_sen = "company confidential"
        self._read_field("original_sensitivity", orig_sen)

        priority = ""
        if item.priority == 0:
            priority = "nonurgent"
        elif item.priority == 1:
            priority = "normal"
        elif item.priority == 2:
            priority = "urgent"
        self._read_field("priority", priority)

        sen = ""
        if item.sensitivity == 0:
            sen = "none"
        elif item.sensitivity == 1:
             sen = "personal"
        elif item.sensitivity == 2:
             sen = "private"
        elif item.sensitivity == 3:
             sen = "company confidential"
        self._read_field("sensitivity", sen)       
 
        if item.arrival_date is not None:
            self._read_field("arrival_date", 
                self._pst.pst_rfc2425_datetime_format(item.arrival_date))

        if item.report_time is not None:
            self._read_field("report_time", 
                self._pst.pst_rfc2425_datetime_format(item.report_time))

        if item.sent_date is not None:
            self._read_field("sent_date", 
                self._pst.pst_rfc2425_datetime_format(item.sent_date))

    def _read_appointment_fields(self, item):
        self._read_field("alarm", item.alarm)
        self._read_field("alarm_minutes", item.alarm_minutes)
        self._read_field("all_day", item.all_day)
        self._read_field("is_recurring", item.is_recurring)
        self._read_field("location", item.location.str)
        self._read_field("recurrence_description", item.recurrence_description.str)
        self._read_field("timezonestring", item.timezonestring.str)

        if item.end is not None:
            self._read_field("end", 
                self._pst.pst_rfc2425_datetime_format(item.end))
        
        if item.recurrence_end is not None:
            self._read_field("recurrence_end", 
                self._pst.pst_rfc2425_datetime_format(item.recurrence_end))

        if item.recurrence_start is not None:
            self._read_field("recurrence_start", 
                self._pst.pst_rfc2425_datetime_format(item.recurrence_start))

        if item.reminder is not None:
            self._read_field("reminder", 
                self._pst.pst_rfc2425_datetime_format(item.reminder))

        if item.start is not None:
            self._read_field("start", 
                self._pst.pst_rfc2425_datetime_format(item.start))

        label = ""
        if item.label == 0:
            label = "None"
        elif item.label == 1:
            label = "Important"
        elif item.label == 2:
            label = "Business"
        elif item.label == 3:
            label = "Personal"
        elif item.label == 4:
            label = "Vacation"
        elif item.label == 5:
            label = "Must Attend"
        elif item.label == 6:
            label = "Travel Required"
        elif item.label == 7:
            label = "Needs Preparation"
        elif item.label == 8:
            label = "Birthday"
        elif item.label == 9:
            label = "Anniversary"
        elif item.label == 10:
            label = "Phone Call"
        self._read_field("label", label)       

        recurrence_type = ""
        if item.recurrence_type == 0:
            priority = "none"
        elif item.recurrence_type == 1:
            recurrence_type = "daily"
        elif item.recurrence_type == 2:
            recurrence_type = "weekly"
        elif item.recurrence_type == 3:
            recurrence_type = "monthly"
        elif item.recurrence_type == 4:
            recurrence_type = "yearly"
        self._read_field("recurrence_type", recurrence_type)       

        showas = ""
        if item.showas == 0:
            showas = "free"
        elif item.showas == 1:
            showas = "tentative"
        elif item.showas == 2:
            showas = "busy"
        elif item.showas == 3:
            showas = "out of office"
        self._read_field("showas", showas)      

    def _read_contact_fields(self, item):
        self._read_field("account_name", item.account_name.str)
        self._read_field("address1", item.address1.str)
        self._read_field("address1a", item.address1a.str)
        self._read_field("address1_desc", item.address1_desc.str)
        self._read_field("address1_transport", item.address1_transport.str)
        self._read_field("address2", item.address2.str)
        self._read_field("address2a", item.address2a.str)
        self._read_field("address2_desc", item.address2_desc.str)
        self._read_field("address2_transport", item.address2_transport.str)
        self._read_field("address3", item.address3.str)
        self._read_field("address3a", item.address3a.str)
        self._read_field("address3_desc", item.address3_desc.str)
        self._read_field("address3_transport", item.address3_transport.str)
        self._read_field("assistant_name", item.assistant_name.str)
        self._read_field("assistant_phone", item.assistant_phone.str)
        self._read_field("billing_information", item.billing_information.str)
        self._read_field("business_address", item.business_address.str)
        self._read_field("business_city", item.business_city.str)
        self._read_field("business_country", item.business_country.str)
        self._read_field("business_fax", item.business_fax.str)
        self._read_field("business_homepage", item.business_homepage.str)
        self._read_field("business_phone", item.business_phone.str)
        self._read_field("business_phone2", item.business_phone2.str)
        self._read_field("business_po_box", item.business_po_box.str)
        self._read_field("business_postal_code", item.business_postal_code.str)
        self._read_field("business_state", item.business_state.str)
        self._read_field("business_street", item.business_street.str)
        self._read_field("callback_phone", item.callback_phone.str)
        self._read_field("car_phone", item.car_phone.str)
        self._read_field("company_main_phone", item.company_main_phone.str)
        self._read_field("company_name", item.company_name.str)
        self._read_field("computer_name", item.computer_name.str)
        self._read_field("customer_id", item.customer_id.str)
        self._read_field("def_postal_address", item.def_postal_address.str)
        self._read_field("department", item.department.str)
        self._read_field("display_name_prefix", item.display_name_prefix.str)
        self._read_field("first_name", item.first_name.str)
        self._read_field("followup", item.followup.str)
        self._read_field("free_busy_address", item.free_busy_address.str)
        self._read_field("ftp_site", item.ftp_site.str)
        self._read_field("fullname", item.fullname.str)
        self._read_field("gov_id", item.gov_id.str)
        self._read_field("hobbies", item.hobbies.str)
        self._read_field("home_address", item.home_address.str)
        self._read_field("home_city", item.home_city.str)
        self._read_field("home_country", item.home_country.str)
        self._read_field("home_fax", item.home_fax.str)
        self._read_field("home_phone", item.home_phone.str)
        self._read_field("home_phone2", item.home_phone2.str)
        self._read_field("home_po_box", item.home_po_box.str)
        self._read_field("home_postal_code", item.home_postal_code.str)
        self._read_field("home_state", item.home_state.str)
        self._read_field("home_street", item.home_street.str)
        self._read_field("initials", item.initials.str)
        self._read_field("isdn_phone", item.isdn_phone.str)
        self._read_field("job_title", item.job_title.str)
        self._read_field("keyword", item.keyword.str)
        self._read_field("language", item.language.str)
        self._read_field("location", item.location.str)
        self._read_field("mail_permission", item.mail_permission)
        self._read_field("manager_name", item.manager_name.str)
        self._read_field("middle_name", item.middle_name.str)
        self._read_field("mileage", item.mileage.str)
        self._read_field("mobile_phone", item.mobile_phone.str)
        self._read_field("nickname", item.nickname.str)
        self._read_field("office_loc", item.office_loc.str)
        self._read_field("common_name", item.common_name.str)
        self._read_field("org_id", item.org_id.str)
        self._read_field("other_address", item.other_address.str)
        self._read_field("other_city", item.other_city.str)
        self._read_field("other_country", item.other_country.str)
        self._read_field("other_phone", item.other_phone.str)
        self._read_field("other_po_box", item.other_po_box.str)
        self._read_field("other_postal_code", item.other_postal_code.str)
        self._read_field("other_state", item.other_state.str)
        self._read_field("other_street", item.other_street.str)
        self._read_field("pager_phone", item.pager_phone.str)
        self._read_field("personal_homepage", item.personal_homepage.str)
        self._read_field("pref_name", item.pref_name.str)
        self._read_field("primary_fax", item.primary_fax.str)
        self._read_field("primary_phone", item.primary_phone.str)
        self._read_field("profession", item.profession.str)
        self._read_field("radio_phone", item.radio_phone.str)
        self._read_field("rich_text", item.rich_text)
        self._read_field("spouse_name", item.spouse_name.str)
        self._read_field("suffix", item.suffix.str)
        self._read_field("surname", item.surname.str)
        self._read_field("telex", item.telex.str)
        self._read_field("transmittable_display_name", item.transmittable_display_name.str)
        self._read_field("ttytdd_phone", item.ttytdd_phone.str)
        self._read_field("work_address_street", item.work_address_street.str)
        self._read_field("work_address_city", item.work_address_city.str)
        self._read_field("work_address_state", item.work_address_state.str)
        self._read_field("work_address_postalcode", item.work_address_postalcode.str)
        self._read_field("work_address_country", item.work_address_country.str)
        self._read_field("work_address_postofficebox", item.work_address_postofficebox.str)
        
        if item.birthday is not None:
            self._read_field("birthday", 
                self._pst.pst_rfc2425_datetime_format(item.birthday))

        if item.wedding_anniversary is not None:
            self._read_field("wedding_anniversary", 
                self._pst.pst_rfc2425_datetime_format(item.wedding_anniversary))

        if item.gender == 0:
            gender = "unspecified"
        elif item.gender == 1:
            gender = "female"
        elif item.gender == 2:
            gender = "male"    
        self._read_field("gender", gender)

    def _read_journal_fields(self, item):
        self._read_field("description", item.description.str)
        self._read_field("type", item.type.str)

        if item.end is not None:
            self._read_field("end", 
                self._pst.pst_rfc2425_datetime_format(item.end))

        if item.start is not None:
            self._read_field("start", 
                self._pst.pst_rfc2425_datetime_format(item.start))

    def _read_extra_field(self, name, value):
        if value != "": 
            value = str(value).strip()
            propertytype_id = self._propertytype_id
            key = "{0}_{1}".format(propertytype_id, name)
            if key in self._property_dic:
                property_id = self._property_dic[key]
            else:
                property_id = self._db.create_property(propertytype_id, name)
                self._property_dic[key] = property_id

            if not property_id in self._pids: #this property has not been extracted for this item yet
                self._pids.add(property_id)
                self._db.create_item_property(self._item_id, property_id, value, self._batch)
            else: #this property has been extracted for this item: must concatenate
                value = " {0} {1}".format(common.DELIMITER, value)
                self._db.concat_item_property(self._item_id, property_id, value)
            
    def _read_field(self, name, value, override_pt_id=None):
        if value != "": #only process non-empty values
            # this allows to override property types for individual fields; 
            #   for example, it is used for common pst fields which belong 
            #   to all pst types (body, subject, etc...)
            value = str(value).strip()
            if override_pt_id is None:
                propertytype_id = self._propertytype_id
            else:
                propertytype_id = override_pt_id

            key = "{0}_{1}".format(propertytype_id, name)
            if key in self._property_dic:
                property_id = self._property_dic[key]
            else:
                property_id = self._db.create_property(propertytype_id, name)
                self._property_dic[key] = property_id

            if not property_id in self._pids:
                self._pids.add(property_id)
            
            self._db.create_item_property(self._item_id, property_id, value, self._batch)
