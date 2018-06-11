CREATE FULLTEXT INDEX in_data_all_items__item_text
    ON data_all_items (item_text);

CREATE FULLTEXT INDEX in_data_all_items__item_metadata
    ON data_all_items (item_metadata);

CREATE FULLTEXT INDEX in_data_nonemail_items__item_text
    ON data_nonemail_items (item_text);

CREATE FULLTEXT INDEX in_data_nonemail_items__item_metadata
    ON data_nonemail_items (item_metadata);

CREATE FULLTEXT INDEX in_data_email_items__email_to
    ON data_email_items (email_to);

CREATE FULLTEXT INDEX in_data_email_items__email_from
    ON data_email_items (email_from);

CREATE FULLTEXT INDEX in_data_email_items__email_cc
    ON data_email_items (email_cc);

CREATE FULLTEXT INDEX in_data_email_items__email_bcc
    ON data_email_items (email_bcc);

CREATE FULLTEXT INDEX in_data_email_items__email_subject
    ON data_email_items (email_subject);

CREATE FULLTEXT INDEX in_data_email_items__email_header
    ON data_email_items (email_header);

CREATE FULLTEXT INDEX in_data_email_items__email_body
    ON data_email_items (email_body);

CREATE FULLTEXT INDEX in_data_email_items__email_metadata
    ON data_email_items (email_metadata);
