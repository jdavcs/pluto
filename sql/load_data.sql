
/* LOAD DEFAULT DATA --------------------------------------------- */
INSERT INTO psttype (id, name) VALUES (1, 'note');
INSERT INTO psttype (id, name) VALUES (2, 'schedule');
INSERT INTO psttype (id, name) VALUES (3, 'appointment');
INSERT INTO psttype (id, name) VALUES (4, 'contact');
INSERT INTO psttype (id, name) VALUES (5, 'journal');
INSERT INTO psttype (id, name) VALUES (6, 'stickynote');
INSERT INTO psttype (id, name) VALUES (7, 'task');
INSERT INTO psttype (id, name) VALUES (8, 'other');
INSERT INTO psttype (id, name) VALUES (9, 'report');
INSERT INTO psttype (id, name) VALUES (10, 'attachment');

INSERT INTO containertype (id, name) VALUES (1, 'pst');
INSERT INTO containertype (id, name) VALUES (2, 'zip');
INSERT INTO containertype (id, name) VALUES (3, 'gzip');
INSERT INTO containertype (id, name) VALUES (4, 'tar');
INSERT INTO containertype (id, name) VALUES (5, 'jar');


INSERT INTO mimetype (id, name) VALUES (1, 'application');
INSERT INTO mimetype (id, name) VALUES (2, 'audio');
INSERT INTO mimetype (id, name) VALUES (3, 'image');
INSERT INTO mimetype (id, name) VALUES (4, 'message');
INSERT INTO mimetype (id, name) VALUES (5, 'multipart');
INSERT INTO mimetype (id, name) VALUES (6, 'text');
INSERT INTO mimetype (id, name) VALUES (7, 'video');
INSERT INTO mimetype (id, name) VALUES (8, 'model');

INSERT INTO mimetypedetector (id, name) VALUES (1, 'unix file utility');
INSERT INTO mimetypedetector (id, name) VALUES (2, 'apache tika');

INSERT INTO relationshiptype (id, name) VALUES (1, 'is duplicate of');     /* for all duplicates */ 
INSERT INTO relationshiptype (id, name) VALUES (2, 'is reply to');     /* for replies */ 

INSERT INTO propertytype (id, name) VALUES (1, 'pstitem-note');
INSERT INTO propertytype (id, name) VALUES (2, 'pstitem-schedule');
INSERT INTO propertytype (id, name) VALUES (3, 'pstitem-appointment');
INSERT INTO propertytype (id, name) VALUES (4, 'pstitem-contact');
INSERT INTO propertytype (id, name) VALUES (5, 'pstitem-journal');
INSERT INTO propertytype (id, name) VALUES (6, 'pstitem-stickynote');
INSERT INTO propertytype (id, name) VALUES (7, 'pstitem-task');
INSERT INTO propertytype (id, name) VALUES (8, 'pstitem-other');
INSERT INTO propertytype (id, name) VALUES (9, 'pstitem-report');
INSERT INTO propertytype (id, name) VALUES (10, 'pstitem-attachment');
INSERT INTO propertytype (id, name) VALUES (11, 'pstitem-all');
INSERT INTO propertytype (id, name) VALUES (12, 'fileitem');


/* all pst items */ 
INSERT INTO property (propertytype_id, name) VALUES (11, 'body');
INSERT INTO property (propertytype_id, name) VALUES (11, 'body_charset');
INSERT INTO property (propertytype_id, name) VALUES (11, 'comment');
INSERT INTO property (propertytype_id, name) VALUES (11, 'create_date');
INSERT INTO property (propertytype_id, name) VALUES (11, 'file_as');
INSERT INTO property (propertytype_id, name) VALUES (11, 'modify_date');
INSERT INTO property (propertytype_id, name) VALUES (11, 'outlook_version');
INSERT INTO property (propertytype_id, name) VALUES (11, 'response_requested');
INSERT INTO property (propertytype_id, name) VALUES (11, 'subject');
INSERT INTO property (propertytype_id, name) VALUES (11, 'Keywords');
INSERT INTO property (propertytype_id, name) VALUES (11, 'flags');

/* pst email item */ 
INSERT INTO property (propertytype_id, name) VALUES (1, 'autoforward');
INSERT INTO property (propertytype_id, name) VALUES (1, 'bcc_address');
INSERT INTO property (propertytype_id, name) VALUES (1, 'cc_address');
INSERT INTO property (propertytype_id, name) VALUES (1, 'conversation_prohibited');
INSERT INTO property (propertytype_id, name) VALUES (1, 'delete_after_submit');
INSERT INTO property (propertytype_id, name) VALUES (1, 'delivery_report');
INSERT INTO property (propertytype_id, name) VALUES (1, 'header');
INSERT INTO property (propertytype_id, name) VALUES (1, 'html_body');
INSERT INTO property (propertytype_id, name) VALUES (1, 'in_reply_to');
INSERT INTO property (propertytype_id, name) VALUES (1, 'message_cc_me');
INSERT INTO property (propertytype_id, name) VALUES (1, 'message_recip_me');
INSERT INTO property (propertytype_id, name) VALUES (1, 'message_to_me');
INSERT INTO property (propertytype_id, name) VALUES (1, 'messageid');
INSERT INTO property (propertytype_id, name) VALUES (1, 'ndr_diag_code');
INSERT INTO property (propertytype_id, name) VALUES (1, 'ndr_reason_code');
INSERT INTO property (propertytype_id, name) VALUES (1, 'ndr_status_code');
INSERT INTO property (propertytype_id, name) VALUES (1, 'original_bcc');
INSERT INTO property (propertytype_id, name) VALUES (1, 'original_cc');
INSERT INTO property (propertytype_id, name) VALUES (1, 'original_to');
INSERT INTO property (propertytype_id, name) VALUES (1, 'outlook_recepient');
INSERT INTO property (propertytype_id, name) VALUES (1, 'outlook_recepient_name');
INSERT INTO property (propertytype_id, name) VALUES (1, 'outlook_recepient2');
INSERT INTO property (propertytype_id, name) VALUES (1, 'outlook_sender');
INSERT INTO property (propertytype_id, name) VALUES (1, 'outlook_sender_name');
INSERT INTO property (propertytype_id, name) VALUES (1, 'outlook_sender2');
INSERT INTO property (propertytype_id, name) VALUES (1, 'processed_subject');
INSERT INTO property (propertytype_id, name) VALUES (1, 'read_receipt');
INSERT INTO property (propertytype_id, name) VALUES (1, 'recip_access');
INSERT INTO property (propertytype_id, name) VALUES (1, 'recip_address');
INSERT INTO property (propertytype_id, name) VALUES (1, 'recip2_access');
INSERT INTO property (propertytype_id, name) VALUES (1, 'recip2_address');
INSERT INTO property (propertytype_id, name) VALUES (1, 'reply_requested');
INSERT INTO property (propertytype_id, name) VALUES (1, 'reply_to');
INSERT INTO property (propertytype_id, name) VALUES (1, 'report_text');
INSERT INTO property (propertytype_id, name) VALUES (1, 'return_path_address');
INSERT INTO property (propertytype_id, name) VALUES (1, 'rtf_body_char_count');
INSERT INTO property (propertytype_id, name) VALUES (1, 'rtf_body_crc');
INSERT INTO property (propertytype_id, name) VALUES (1, 'rtf_body_tag');
INSERT INTO property (propertytype_id, name) VALUES (1, 'rtf_in_sync');
INSERT INTO property (propertytype_id, name) VALUES (1, 'rtf_ws_prefix_count');
INSERT INTO property (propertytype_id, name) VALUES (1, 'rtf_ws_trailing_count');
INSERT INTO property (propertytype_id, name) VALUES (1, 'sender_access');
INSERT INTO property (propertytype_id, name) VALUES (1, 'sender_address');
INSERT INTO property (propertytype_id, name) VALUES (1, 'sender2_access');
INSERT INTO property (propertytype_id, name) VALUES (1, 'sender2_address');
INSERT INTO property (propertytype_id, name) VALUES (1, 'sentto_address');
INSERT INTO property (propertytype_id, name) VALUES (1, 'supplementary_info');
INSERT INTO property (propertytype_id, name) VALUES (1, 'arrival_date');
INSERT INTO property (propertytype_id, name) VALUES (1, 'importance');
INSERT INTO property (propertytype_id, name) VALUES (1, 'original_sensitivity');
INSERT INTO property (propertytype_id, name) VALUES (1, 'priority');
INSERT INTO property (propertytype_id, name) VALUES (1, 'report_time');
INSERT INTO property (propertytype_id, name) VALUES (1, 'sensitivity');
INSERT INTO property (propertytype_id, name) VALUES (1, 'sent_date');

/* pst appointment item */ 
INSERT INTO property (propertytype_id, name) VALUES (3, 'alarm');
INSERT INTO property (propertytype_id, name) VALUES (3, 'alarm_minutes');
INSERT INTO property (propertytype_id, name) VALUES (3, 'all_day');
INSERT INTO property (propertytype_id, name) VALUES (3, 'is_recurring');
INSERT INTO property (propertytype_id, name) VALUES (3, 'location');
INSERT INTO property (propertytype_id, name) VALUES (3, 'recurrence_description');
INSERT INTO property (propertytype_id, name) VALUES (3, 'timezonestring');
INSERT INTO property (propertytype_id, name) VALUES (3, 'end');
INSERT INTO property (propertytype_id, name) VALUES (3, 'label');
INSERT INTO property (propertytype_id, name) VALUES (3, 'recurrence_end');
INSERT INTO property (propertytype_id, name) VALUES (3, 'recurrence_start');
INSERT INTO property (propertytype_id, name) VALUES (3, 'recurrence_type');
INSERT INTO property (propertytype_id, name) VALUES (3, 'reminder');
INSERT INTO property (propertytype_id, name) VALUES (3, 'showas');
INSERT INTO property (propertytype_id, name) VALUES (3, 'start');
                         
/* pst contact item */ 
INSERT INTO property (propertytype_id, name) VALUES (4, 'account_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address1');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address1a');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address1_desc');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address1_transport');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address2');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address2a');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address2_desc');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address2_transport');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address3');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address3a');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address3_desc');
INSERT INTO property (propertytype_id, name) VALUES (4, 'address3_transport');
INSERT INTO property (propertytype_id, name) VALUES (4, 'assistant_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'assistant_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'billing_information');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_address');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_city');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_country');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_fax');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_homepage');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_phone2');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_po_box');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_postal_code');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_state');
INSERT INTO property (propertytype_id, name) VALUES (4, 'business_street');
INSERT INTO property (propertytype_id, name) VALUES (4, 'callback_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'car_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'company_main_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'company_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'computer_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'customer_id');
INSERT INTO property (propertytype_id, name) VALUES (4, 'def_postal_address');
INSERT INTO property (propertytype_id, name) VALUES (4, 'department');
INSERT INTO property (propertytype_id, name) VALUES (4, 'display_name_prefix');
INSERT INTO property (propertytype_id, name) VALUES (4, 'first_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'followup');
INSERT INTO property (propertytype_id, name) VALUES (4, 'free_busy_address');
INSERT INTO property (propertytype_id, name) VALUES (4, 'ftp_site');
INSERT INTO property (propertytype_id, name) VALUES (4, 'fullname');
INSERT INTO property (propertytype_id, name) VALUES (4, 'gov_id');
INSERT INTO property (propertytype_id, name) VALUES (4, 'hobbies');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_address');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_city');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_country');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_fax');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_phone2');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_po_box');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_postal_code');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_state');
INSERT INTO property (propertytype_id, name) VALUES (4, 'home_street');
INSERT INTO property (propertytype_id, name) VALUES (4, 'initials');
INSERT INTO property (propertytype_id, name) VALUES (4, 'isdn_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'job_title');
INSERT INTO property (propertytype_id, name) VALUES (4, 'keyword');
INSERT INTO property (propertytype_id, name) VALUES (4, 'language');
INSERT INTO property (propertytype_id, name) VALUES (4, 'location');
INSERT INTO property (propertytype_id, name) VALUES (4, 'mail_permission');
INSERT INTO property (propertytype_id, name) VALUES (4, 'manager_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'middle_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'mileage');
INSERT INTO property (propertytype_id, name) VALUES (4, 'mobile_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'nickname');
INSERT INTO property (propertytype_id, name) VALUES (4, 'office_loc');
INSERT INTO property (propertytype_id, name) VALUES (4, 'common_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'org_id');
INSERT INTO property (propertytype_id, name) VALUES (4, 'other_address');
INSERT INTO property (propertytype_id, name) VALUES (4, 'other_city');
INSERT INTO property (propertytype_id, name) VALUES (4, 'other_country');
INSERT INTO property (propertytype_id, name) VALUES (4, 'other_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'other_po_box');
INSERT INTO property (propertytype_id, name) VALUES (4, 'other_postal_code');
INSERT INTO property (propertytype_id, name) VALUES (4, 'other_state');
INSERT INTO property (propertytype_id, name) VALUES (4, 'other_street');
INSERT INTO property (propertytype_id, name) VALUES (4, 'pager_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'personal_homepage');
INSERT INTO property (propertytype_id, name) VALUES (4, 'pref_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'primary_fax');
INSERT INTO property (propertytype_id, name) VALUES (4, 'primary_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'profession');
INSERT INTO property (propertytype_id, name) VALUES (4, 'radio_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'rich_text');
INSERT INTO property (propertytype_id, name) VALUES (4, 'spouse_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'suffix');
INSERT INTO property (propertytype_id, name) VALUES (4, 'surname');
INSERT INTO property (propertytype_id, name) VALUES (4, 'telex');
INSERT INTO property (propertytype_id, name) VALUES (4, 'transmittable_display_name');
INSERT INTO property (propertytype_id, name) VALUES (4, 'ttytdd_phone');
INSERT INTO property (propertytype_id, name) VALUES (4, 'work_address_street');
INSERT INTO property (propertytype_id, name) VALUES (4, 'work_address_city');
INSERT INTO property (propertytype_id, name) VALUES (4, 'work_address_state');
INSERT INTO property (propertytype_id, name) VALUES (4, 'work_address_postalcode');
INSERT INTO property (propertytype_id, name) VALUES (4, 'work_address_country');
INSERT INTO property (propertytype_id, name) VALUES (4, 'work_address_postofficebox');
INSERT INTO property (propertytype_id, name) VALUES (4, 'birthday');
INSERT INTO property (propertytype_id, name) VALUES (4, 'gender');
INSERT INTO property (propertytype_id, name) VALUES (4, 'wedding_anniversary');

/* pst journal item */ 
INSERT INTO property (propertytype_id, name) VALUES (5, 'description');
INSERT INTO property (propertytype_id, name) VALUES (5, 'type');

/* pst attachment item */ 
INSERT INTO property (propertytype_id, name) VALUES (10, 'filename1');
INSERT INTO property (propertytype_id, name) VALUES (10, 'filename2');
INSERT INTO property (propertytype_id, name) VALUES (10, 'mimetype');
INSERT INTO property (propertytype_id, name) VALUES (10, 'position');
INSERT INTO property (propertytype_id, name) VALUES (10, 'sequence');
INSERT INTO property (propertytype_id, name) VALUES (10, 'method');

/* file items */ 
INSERT INTO property (propertytype_id, name) VALUES (12, 'extracted-text');

INSERT INTO redacttype (name) VALUES('no redaction needed');
INSERT INTO redacttype (name) VALUES('full item redaction');
INSERT INTO redacttype (name) VALUES('content redaction');

INSERT INTO redactrule (name) VALUES('credit card');
INSERT INTO redactrule (name) VALUES('US passport');
INSERT INTO redactrule (name) VALUES('SSN');


/* COMMIIT DEFAULT DATA ------------------------------------------ */
COMMIT; /* must call this for innodb! */
