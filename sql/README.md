# /src/sql

## Change log
Update 9/2/17:
Renamed field name: "generated" to "generated_val" in sproc.sql and setup.sql
("generated" is a reserved word in MySQL as of v. 5.7.6)


## What's inside

### add_fk.sql
Adds foreign keys to maintain data integrity.

### add_fulltext_indexes.sql
Creates fulltext indexes on extracted item text and relevant metadata fields.

### add_indexes.sql
Creates indexes for faster processing.

### load_data.sql
Loads default data used for extraction:
- PST item types (note, schedule, contact...)
- container types (pst, zip, gzip...)
- MIME types (application, audio, image...)
- MIME type detector (UNIX file utility, Apache Tika)
- PST item property types (pstitem-note, pstitem-schedule...)
- PST item properties/all items (body, comment, subject...) 
- PST item properties/email items (autoforward, bcc_address...)
- PST item properties/appointment items (alarm, is_recurring...)
- PST item properties/contact items (address1, business_address...)
- PST item properties/journal items (description, type)
- PST item properties/attachment items (filename1, mimetype...)
- file item properties (extracted-text)
- redaction types (no redaction needed, full item redaction, content redaction)
- redaction rules (credit card, US passport, SSN)

### load_dataitems.sql
Populates data_item table (denormalized table for retrieval).

### setup.sql
Creates all tables, drops existing tables. Here's the structure of all tables:

```sql
mysql> describe containeritem;
+------------------+------------+------+-----+---------+-------+
| Field            | Type       | Null | Key | Default | Extra |
+------------------+------------+------+-----+---------+-------+
| item_id          | int(11)    | NO   | PRI | NULL    |       |
| containertype_id | int(11)    | NO   | MUL | NULL    |       |
| is_extracted     | tinyint(1) | YES  | MUL | NULL    |       |
+------------------+------------+------+-----+---------+-------+

mysql> describe containertype;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int(11)     | NO   | PRI | NULL    |       |
| name  | varchar(20) | NO   | UNI | NULL    |       |
+-------+-------------+------+-----+---------+-------+

mysql> describe data_all_items;
+---------------+----------+------+-----+---------+-------+
| Field         | Type     | Null | Key | Default | Extra |
+---------------+----------+------+-----+---------+-------+
| item_id       | int(11)  | NO   | PRI | NULL    |       |
| item_text     | longtext | YES  | MUL | NULL    |       |
| item_metadata | longtext | YES  | MUL | NULL    |       |
+---------------+----------+------+-----+---------+-------+

mysql> describe data_dedup;
+-----------------+--------------+------+-----+---------+-------+
| Field           | Type         | Null | Key | Default | Extra |
+-----------------+--------------+------+-----+---------+-------+
| item_id         | int(11)      | NO   | PRI | NULL    |       |
| file_md5sum     | varchar(32)  | YES  |     | NULL    |       |
| pst_md5sum      | varchar(32)  | YES  |     | NULL    |       |
| email_messageid | varchar(100) | YES  |     | NULL    |       |
+-----------------+--------------+------+-----+---------+-------+

mysql> describe data_dedup_hash;
+-----------+-------------+------+-----+---------+-------+
| Field     | Type        | Null | Key | Default | Extra |
+-----------+-------------+------+-----+---------+-------+
| item_id   | int(11)     | NO   | PRI | NULL    |       |
| hash_D    | varchar(32) | YES  |     | NULL    |       |
| hash_F    | varchar(32) | YES  |     | NULL    |       |
| hash_FD   | varchar(32) | YES  |     | NULL    |       |
| hash_B    | varchar(32) | YES  |     | NULL    |       |
| hash_BD   | varchar(32) | YES  |     | NULL    |       |
| hash_BF   | varchar(32) | YES  |     | NULL    |       |
| hash_BFD  | varchar(32) | YES  |     | NULL    |       |
| hash_M    | varchar(32) | YES  |     | NULL    |       |
| hash_MD   | varchar(32) | YES  |     | NULL    |       |
| hash_MF   | varchar(32) | YES  |     | NULL    |       |
| hash_MFD  | varchar(32) | YES  |     | NULL    |       |
| hash_MB   | varchar(32) | YES  |     | NULL    |       |
| hash_MBD  | varchar(32) | YES  |     | NULL    |       |
| hash_MBF  | varchar(32) | YES  |     | NULL    |       |
| hash_MBFD | varchar(32) | YES  |     | NULL    |       |
+-----------+-------------+------+-----+---------+-------+

mysql> describe data_email_items;
+----------------+---------------+------+-----+---------+-------+
| Field          | Type          | Null | Key | Default | Extra |
+----------------+---------------+------+-----+---------+-------+
| item_id        | int(11)       | NO   | PRI | NULL    |       |
| email_to       | text          | YES  | MUL | NULL    |       |
| email_cc       | text          | YES  | MUL | NULL    |       |
| email_bcc      | text          | YES  | MUL | NULL    |       |
| email_from     | varchar(2000) | YES  | MUL | NULL    |       |
| email_date     | datetime      | YES  |     | NULL    |       |
| email_subject  | varchar(1000) | YES  | MUL | NULL    |       |
| email_header   | longtext      | YES  | MUL | NULL    |       |
| email_body     | longtext      | YES  | MUL | NULL    |       |
| email_metadata | longtext      | YES  | MUL | NULL    |       |
+----------------+---------------+------+-----+---------+-------+

mysql> describe data_item;
+-----------------------+---------------+------+-----+---------+-------+
| Field                 | Type          | Null | Key | Default | Extra |
+-----------------------+---------------+------+-----+---------+-------+
| item_id               | int(11)       | NO   | PRI | NULL    |       |
| source_id             | int(11)       | NO   | MUL | NULL    |       |
| source_name           | varchar(50)   | NO   |     | NULL    |       |
| parent_id             | int(11)       | YES  |     | NULL    |       |
| tree_level            | int(11)       | YES  |     | NULL    |       |
| public_id             | varchar(50)   | YES  | UNI | NULL    |       |
| redacttype_id         | int(11)       | YES  | MUL | NULL    |       |
| origin_id             | int(11)       | YES  | MUL | NULL    |       |
| psttype_id            | int(11)       | YES  | MUL | NULL    |       |
| psttype_name          | varchar(20)   | YES  |     | NULL    |       |
| pstfolder_id          | int(11)       | YES  |     | NULL    |       |
| pstfolder_name        | varchar(50)   | YES  |     | NULL    |       |
| conttype_id           | int(11)       | YES  |     | NULL    |       |
| conttype_name         | varchar(20)   | YES  |     | NULL    |       |
| cont_isextracted      | tinyint(1)    | YES  |     | NULL    |       |
| file_mimetype_id      | int(11)       | YES  | MUL | NULL    |       |
| file_mimetype_name    | varchar(20)   | YES  |     | NULL    |       |
| file_mimesubtype_id   | int(11)       | YES  | MUL | NULL    |       |
| file_mimesubtype_name | varchar(50)   | YES  |     | NULL    |       |
| file_mimedetector_id  | int(11)       | YES  |     | NULL    |       |
| file_mimedetails      | varchar(2000) | YES  |     | NULL    |       |
| file_name             | varchar(500)  | YES  | MUL | NULL    |       |
| file_extension        | varchar(500)  | YES  | MUL | NULL    |       |
| file_size             | int(11)       | YES  | MUL | NULL    |       |
| file_attch_position   | int(11)       | YES  |     | NULL    |       |
| file_md5sum           | varchar(32)   | YES  |     | NULL    |       |
+-----------------------+---------------+------+-----+---------+-------+

mysql> describe data_nonemail_items;
+---------------+----------+------+-----+---------+-------+
| Field         | Type     | Null | Key | Default | Extra |
+---------------+----------+------+-----+---------+-------+
| item_id       | int(11)  | NO   | PRI | NULL    |       |
| item_text     | longtext | YES  | MUL | NULL    |       |
| item_metadata | longtext | YES  | MUL | NULL    |       |
+---------------+----------+------+-----+---------+-------+

mysql> describe fileitem;
+---------------------+--------------+------+-----+---------+-------+
| Field               | Type         | Null | Key | Default | Extra |
+---------------------+--------------+------+-----+---------+-------+
| item_id             | int(11)      | NO   | PRI | NULL    |       |
| mimetype_id         | int(11)      | YES  | MUL | NULL    |       |
| mimesubtype_id      | int(11)      | YES  | MUL | NULL    |       |
| mimetypedetector_id | int(11)      | YES  | MUL | NULL    |       |
| mime_details        | varchar(500) | YES  | MUL | NULL    |       |
| original_name       | varchar(500) | YES  |     | NULL    |       |
| extension           | varchar(500) | YES  | MUL | NULL    |       |
| filesize            | int(11)      | YES  | MUL | NULL    |       |
| attch_position      | int(11)      | YES  |     | NULL    |       |
+---------------------+--------------+------+-----+---------+-------+

mysql> describe item;
+---------------+-------------+------+-----+---------+----------------+
| Field         | Type        | Null | Key | Default | Extra          |
+---------------+-------------+------+-----+---------+----------------+
| id            | int(11)     | NO   | PRI | NULL    | auto_increment |
| source_id     | int(11)     | NO   | MUL | NULL    |                |
| parent_id     | int(11)     | YES  | MUL | NULL    |                |
| tree_level    | int(11)     | YES  |     | NULL    |                |
| public_id     | varchar(50) | YES  | UNI | NULL    |                |
| redacttype_id | int(11)     | YES  | MUL | NULL    |                |
| origin_id     | int(11)     | YES  | MUL | NULL    |                |
+---------------+-------------+------+-----+---------+----------------+

mysql> describe item_label;
+----------+---------+------+-----+---------+-------+
| Field    | Type    | Null | Key | Default | Extra |
+----------+---------+------+-----+---------+-------+
| item_id  | int(11) | NO   | PRI | NULL    |       |
| label_id | int(11) | NO   | PRI | NULL    |       |
+----------+---------+------+-----+---------+-------+

mysql> describe item_property;
+-------------+----------+------+-----+---------+-------+
| Field       | Type     | Null | Key | Default | Extra |
+-------------+----------+------+-----+---------+-------+
| item_id     | int(11)  | NO   | PRI | NULL    |       |
| property_id | int(11)  | NO   | PRI | NULL    |       |
| value       | longtext | YES  |     | NULL    |       |
| batch       | int(11)  | YES  |     | NULL    |       |
+-------------+----------+------+-----+---------+-------+

mysql> describe item_redaction;
+--------------+---------+------+-----+---------+----------------+
| Field        | Type    | Null | Key | Default | Extra          |
+--------------+---------+------+-----+---------+----------------+
| id           | int(11) | NO   | PRI | NULL    | auto_increment |
| item_id      | int(11) | NO   | MUL | NULL    |                |
| redaction_id | int(11) | NO   | MUL | NULL    |                |
| property_id  | int(11) | NO   | MUL | NULL    |                |
+--------------+---------+------+-----+---------+----------------+

mysql> describe item_relationship;
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| item1_id   | int(11)     | NO   | PRI | NULL    |       |
| reltype_id | int(11)     | NO   | PRI | NULL    |       |
| item2_id   | int(11)     | NO   | PRI | NULL    |       |
| value      | varchar(25) | YES  |     | NULL    |       |
+------------+-------------+------+-----+---------+-------+

mysql> describe label;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int(11)      | NO   | PRI | NULL    | auto_increment |
| name  | varchar(100) | NO   | UNI | NULL    |                |
+-------+--------------+------+-----+---------+----------------+

mysql> describe mimesubtype;
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| name  | varchar(50) | NO   | UNI | NULL    |                |
+-------+-------------+------+-----+---------+----------------+

mysql> describe mimetype;
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| name  | varchar(20) | NO   | UNI | NULL    |                |
+-------+-------------+------+-----+---------+----------------+

mysql> describe mimetypedetector;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int(11)     | NO   | PRI | NULL    |       |
| name  | varchar(50) | NO   | UNI | NULL    |       |
+-------+-------------+------+-----+---------+-------+

mysql> describe property;
+-----------------+-------------+------+-----+---------+----------------+
| Field           | Type        | Null | Key | Default | Extra          |
+-----------------+-------------+------+-----+---------+----------------+
| id              | int(11)     | NO   | PRI | NULL    | auto_increment |
| propertytype_id | int(11)     | YES  | MUL | NULL    |                |
| name            | varchar(50) | NO   | MUL | NULL    |                |
+-----------------+-------------+------+-----+---------+----------------+

mysql> describe propertytype;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int(11)     | NO   | PRI | NULL    |       |
| name  | varchar(50) | NO   | UNI | NULL    |       |
+-------+-------------+------+-----+---------+-------+

mysql> describe pstfolder;
+-----------+-------------+------+-----+---------+----------------+
| Field     | Type        | Null | Key | Default | Extra          |
+-----------+-------------+------+-----+---------+----------------+
| id        | int(11)     | NO   | PRI | NULL    | auto_increment |
| parent_id | int(11)     | YES  | MUL | NULL    |                |
| source_id | int(11)     | NO   | MUL | NULL    |                |
| name      | varchar(50) | YES  | MUL | NULL    |                |
+-----------+-------------+------+-----+---------+----------------+

mysql> describe pstitem;
+--------------+---------+------+-----+---------+-------+
| Field        | Type    | Null | Key | Default | Extra |
+--------------+---------+------+-----+---------+-------+
| item_id      | int(11) | NO   | PRI | NULL    |       |
| psttype_id   | int(11) | NO   | MUL | NULL    |       |
| pstfolder_id | int(11) | YES  | MUL | NULL    |       |
+--------------+---------+------+-----+---------+-------+

mysql> describe psttype;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int(11)     | NO   | PRI | NULL    |       |
| name  | varchar(20) | NO   | UNI | NULL    |       |
+-------+-------------+------+-----+---------+-------+

mysql> describe redaction;
+---------------+-------------+------+-----+---------+----------------+
| Field         | Type        | Null | Key | Default | Extra          |
+---------------+-------------+------+-----+---------+----------------+
| id            | int(11)     | NO   | PRI | NULL    | auto_increment |
| redactrule_id | int(11)     | NO   | MUL | NULL    |                |
| original      | varchar(25) | NO   | UNI | NULL    |                |
| generated_val | varchar(25) | NO   | UNI | NULL    |                |
+---------------+-------------+------+-----+---------+----------------+

mysql> describe redactrule;
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| name  | varchar(25) | NO   | UNI | NULL    |                |
+-------+-------------+------+-----+---------+----------------+

mysql> describe redacttype;
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| name  | varchar(25) | NO   | UNI | NULL    |                |
+-------+-------------+------+-----+---------+----------------+

mysql> describe relationshiptype;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int(11)     | NO   | PRI | NULL    |       |
| name  | varchar(50) | NO   | UNI | NULL    |       |
+-------+-------------+------+-----+---------+-------+

mysql> describe source;
+----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| id       | int(11)     | NO   | PRI | NULL    | auto_increment |
| name     | varchar(50) | NO   | UNI | NULL    |                |
| filesize | int(11)     | YES  |     | NULL    |                |
+----------+-------------+------+-----+---------+----------------+

mysql> describe subset;
+------------+---------------+------+-----+---------+----------------+
| Field      | Type          | Null | Key | Default | Extra          |
+------------+---------------+------+-----+---------+----------------+
| id         | int(11)       | NO   | PRI | NULL    | auto_increment |
| name       | varchar(100)  | NO   | UNI | NULL    |                |
| count      | int(11)       | NO   |     | NULL    |                |
| extensions | varchar(1000) | YES  |     | NULL    |                |
+------------+---------------+------+-----+---------+----------------+

mysql> describe subset_mimesubtype;
+----------------+---------+------+-----+---------+-------+
| Field          | Type    | Null | Key | Default | Extra |
+----------------+---------+------+-----+---------+-------+
| subset_id      | int(11) | NO   | PRI | NULL    |       |
| mimesubtype_id | int(11) | NO   | PRI | NULL    |       |
+----------------+---------+------+-----+---------+-------+

mysql> describe subset_originpsttype;
+------------+---------+------+-----+---------+-------+
| Field      | Type    | Null | Key | Default | Extra |
+------------+---------+------+-----+---------+-------+
| subset_id  | int(11) | NO   | PRI | NULL    |       |
| psttype_id | int(11) | NO   | PRI | NULL    |       |
+------------+---------+------+-----+---------+-------+
```

### sprocs.sql
Creates all stored procedures, drops existing. There may be seemingly redundant procedures; that was
done for better performance (i.e., there may be 2 different procedures calling the same table by the
same criteria, but retrieving a different number of fields: with several million records in the
result set that makes a noticeable difference in performance.
