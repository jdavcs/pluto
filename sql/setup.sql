
/* DO NOT AUTO-COMMIT -------------------------------------------- */ 
SET AUTOCOMMIT=0;


/* DROP TABLES --------------------------------------------------- */
SET foreign_key_checks = 0;

DROP TABLE IF EXISTS containeritem;
DROP TABLE IF EXISTS containertype;
DROP TABLE IF EXISTS data_all_items;
DROP TABLE IF EXISTS data_dedup;
DROP TABLE IF EXISTS data_dedup_hash;
DROP TABLE IF EXISTS data_email_items;
DROP TABLE IF EXISTS data_item;
DROP TABLE IF EXISTS data_nonemail_items;
DROP TABLE IF EXISTS fileitem;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS item_label;
DROP TABLE IF EXISTS item_property;
DROP TABLE IF EXISTS item_redaction;
DROP TABLE IF EXISTS item_relationship;
DROP TABLE IF EXISTS label;
DROP TABLE IF EXISTS mimesubtype;
DROP TABLE IF EXISTS mimetype;
DROP TABLE IF EXISTS mimetypedetector;
DROP TABLE IF EXISTS property;
DROP TABLE IF EXISTS propertytype;
DROP TABLE IF EXISTS pstfolder;
DROP TABLE IF EXISTS pstitem;
DROP TABLE IF EXISTS psttype;
DROP TABLE IF EXISTS redaction;
DROP TABLE IF EXISTS redactrule;
DROP TABLE IF EXISTS redacttype;
DROP TABLE IF EXISTS relationshiptype;
DROP TABLE IF EXISTS source;
DROP TABLE IF EXISTS subset;
DROP TABLE IF EXISTS subset_mimesubtype;
DROP TABLE IF EXISTS subset_originpsttype;

SET foreign_key_checks = 1;

/* COMMIT CLEAN UP ----------------------------------------------- */
COMMIT;


/* CREATE TABLES ------------------------------------------------- */

/* -------------- lookup tables -------------------*/
CREATE TABLE IF NOT EXISTS psttype (
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(20) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS containertype (
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(20) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS mimetype (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(20) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS mimesubtype (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS mimetypedetector (
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS relationshiptype (
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS propertytype (
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS redacttype (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(25) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS redactrule (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(25) NOT NULL UNIQUE)
    ENGINE = InnoDB;

/* -------------- item data tables -------------------*/
CREATE TABLE IF NOT EXISTS item (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    source_id INT NOT NULL,
    parent_id INT, /* container if extracted, pstitem if attached, null if top-level */
    tree_level INT,
    public_id VARCHAR(50) UNIQUE,
    redacttype_id INT,
    origin_id INT)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS pstitem (
    item_id INT NOT NULL PRIMARY KEY,
    psttype_id  INT NOT NULL,
    pstfolder_id INT)  
    ENGINE = InnoDB;
    
CREATE TABLE IF NOT EXISTS containeritem (
    item_id INT NOT NULL PRIMARY KEY,
    containertype_id  INT NOT NULL,
    is_extracted TINYINT(1))
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS fileitem (
    item_id INT NOT NULL PRIMARY KEY,
    mimetype_id INT,
    mimesubtype_id INT,
    mimetypedetector_id INT,
    mime_details VARCHAR(2000),
    original_name VARCHAR(500), 
    extension VARCHAR(500),
    filesize INT,
    attch_position INT)
    ENGINE = InnoDB;


/* -------------- other data tables  -------------------*/
CREATE TABLE IF NOT EXISTS label (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE)
    ENGINE = MyISAM;

CREATE TABLE IF NOT EXISTS source (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
    filesize INT)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS property (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    propertytype_id INT,
	name VARCHAR(50) NOT NULL)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS pstfolder (    
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    parent_id INT,
    source_id INT NOT NULL,
    name VARCHAR(50))
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS redaction (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    redactrule_id INT NOT NULL,
    original VARCHAR(25) NOT NULL UNIQUE,
    generated_val VARCHAR(25) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS subset (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    count INT NOT NULL,
    extensions VARCHAR(1000))
    ENGINE = MyISAM;

/* -------------- link tables -------------------*/
CREATE TABLE IF NOT EXISTS item_label (
	item_id INT NOT NULL,
    label_id INT NOT NULL,
	PRIMARY KEY (item_id, label_id))
    ENGINE = MyISAM;

CREATE TABLE IF NOT EXISTS item_property (
	item_id INT NOT NULL,
	property_id INT NOT NULL,
	value LONGTEXT,
    batch INT,
	PRIMARY KEY (item_id, property_id))
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS item_relationship (
	item1_id INT NOT NULL,
	reltype_id INT NOT NULL,
	item2_id INT NOT NULL,
    value VARCHAR(25), /* for now; expand if needed */
	PRIMARY KEY (item1_id, reltype_id, item2_id))
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS item_redaction (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	item_id INT NOT NULL,
    redaction_id INT NOT NULL,
	property_id INT NOT NULL)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS subset_mimesubtype (
    subset_id INT NOT NULL,
	mimesubtype_id INT NOT NULL,
	PRIMARY KEY (subset_id, mimesubtype_id))
    ENGINE = MyISAM;

CREATE TABLE IF NOT EXISTS subset_originpsttype (
    subset_id INT NOT NULL,
	psttype_id INT NOT NULL,
	PRIMARY KEY (subset_id, psttype_id))
    ENGINE = MyISAM;

/* -------------- tables for dedup -------------------*/
CREATE TABLE IF NOT EXISTS data_dedup (
	item_id INT NOT NULL PRIMARY KEY,
    file_md5sum VARCHAR(32),
    pst_md5sum VARCHAR(32),
    email_messageid VARCHAR(100))
    ENGINE = InnoDB;

-- M = messageid; B = body; F = from, D = sent date
CREATE TABLE IF NOT EXISTS data_dedup_hash (
	item_id INT NOT NULL PRIMARY KEY,
    hash_D    VARCHAR(32),
    hash_F    VARCHAR(32),
    hash_FD   VARCHAR(32),
    hash_B    VARCHAR(32),
    hash_BD   VARCHAR(32),
    hash_BF   VARCHAR(32),
    hash_BFD  VARCHAR(32),
    hash_M    VARCHAR(32),
    hash_MD   VARCHAR(32),
    hash_MF   VARCHAR(32),
    hash_MFD  VARCHAR(32),
    hash_MB   VARCHAR(32),
    hash_MBD  VARCHAR(32),
    hash_MBF  VARCHAR(32),
    hash_MBFD VARCHAR(32))
    ENGINE = InnoDB;

/* -------------- denormalized tables (mostly for search) --------*/
CREATE TABLE IF NOT EXISTS data_item (
    item_id INT NOT NULL PRIMARY KEY,
    source_id INT NOT NULL,
	source_name VARCHAR(50) NOT NULL,
    parent_id INT,
    tree_level INT,
    public_id VARCHAR(50) UNIQUE,
    redacttype_id INT,
    origin_id INT,
    psttype_id INT,
    psttype_name VARCHAR(20),
    pstfolder_id INT,
    pstfolder_name VARCHAR(50),
    conttype_id INT,
    conttype_name VARCHAR(20),
    cont_isextracted TINYINT(1),
    file_mimetype_id INT,
    file_mimetype_name VARCHAR(20),
    file_mimesubtype_id INT,
    file_mimesubtype_name VARCHAR(50),
    file_mimedetector_id INT,
    file_mimedetails VARCHAR(500),
    file_name VARCHAR(500),
    file_extension VARCHAR(500),
    file_size INT,
    file_attch_position INT,
    file_md5sum VARCHAR(32))
    ENGINE = MyISAM;


/* search all items */
CREATE TABLE IF NOT EXISTS data_all_items (
    item_id INT NOT NULL PRIMARY KEY,
    item_text LONGTEXT, /* header + body for pstitems, extracted_text for files */
    item_metadata LONGTEXT) /* properties minus body and extracted text */
    ENGINE = MyISAM;
    
/* search emails by specific fields; Items with psttype_id = 1 */
CREATE TABLE IF NOT EXISTS data_email_items (
    item_id INT NOT NULL PRIMARY KEY,
    email_to TEXT,  
    email_cc TEXT,
    email_bcc TEXT,
    email_from VARCHAR(2000), /* 200 was too short for additional test data from Enron collection */
    email_date DATETIME,
    email_subject VARCHAR(1000),
    email_header LONGTEXT,
    email_body LONGTEXT,
    email_metadata LONGTEXT) /* minus body */
    ENGINE = MyISAM;

/* search non-emails: complements email table; used for performance;
Items with psttype_id != 1 */
CREATE TABLE IF NOT EXISTS data_nonemail_items (
    item_id INT NOT NULL PRIMARY KEY, 
    item_text LONGTEXT, /* body for pst items, extracted_text for files */
    item_metadata LONGTEXT) /* minus body and extracted text */
    ENGINE = MyISAM;


/* COMMIT DEFAULT DATA ------------------------------------------ */
COMMIT; /* must call this for innodb! */
