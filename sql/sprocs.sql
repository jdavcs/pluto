-- drop all sprocs


DROP PROCEDURE IF EXISTS data_dedup_hash__create;
DROP PROCEDURE IF EXISTS data_dedup__create_nonemailpst;
DROP PROCEDURE IF EXISTS data_dedup__get;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS data_item__get_md5sums;
DROP PROCEDURE IF EXISTS data_item__read;
DROP PROCEDURE IF EXISTS data_item__update_md5sum;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS fileitem__get;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS item__get_origin_pstfolders;
DROP PROCEDURE IF EXISTS item__get_nonorigin_pstfolders;
DROP PROCEDURE IF EXISTS item__get_children;
DROP PROCEDURE IF EXISTS item__get_publicids;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS item_label__create;
DROP PROCEDURE IF EXISTS item_label__delete_by_item;
DROP PROCEDURE IF EXISTS item_label__get_by_item;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS item_property__get_by_item;
DROP PROCEDURE IF EXISTS item_property__get_by_property;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS item_relationship__create;
DROP PROCEDURE IF EXISTS item_relationship__get_by_item1;
DROP PROCEDURE IF EXISTS item_relationship__get_by_item2;
DROP PROCEDURE IF EXISTS item_relationship__get_by_reltype;
DROP PROCEDURE IF EXISTS item_relationship__get_item1_by_reltype;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS label__create;
DROP PROCEDURE IF EXISTS label__update;
DROP PROCEDURE IF EXISTS label__delete;
DROP PROCEDURE IF EXISTS label__get;
DROP PROCEDURE IF EXISTS label__get_count;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS mimetype__get;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS mimesubtype__get;
DROP PROCEDURE IF EXISTS mimesubtype__get_by_subset;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS property__get;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS pstfolder__get_by_source;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS pstitem__get;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS psttype__get;
DROP PROCEDURE IF EXISTS psttype__get_by_subset;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS redaction__get;
DROP PROCEDURE IF EXISTS redaction__get_by_query;
DROP PROCEDURE IF EXISTS redaction__count_by_query;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS redactrule__get;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS source__get;
DROP PROCEDURE IF EXISTS source__get_by_view;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS subset__create;
DROP PROCEDURE IF EXISTS subset__read;
DROP PROCEDURE IF EXISTS subset__update;
DROP PROCEDURE IF EXISTS subset__delete;
DROP PROCEDURE IF EXISTS subset__get;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS subset_mimesubtype__create;
DROP PROCEDURE IF EXISTS subset_mimesubtype__delete_by_subset;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS subset_originpsttype__create;
DROP PROCEDURE IF EXISTS subset_originpsttype__delete_by_subset;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS v_distro__get;
-- ---------------------------------------------------------------------
DROP PROCEDURE IF EXISTS data__get_item;
DROP PROCEDURE IF EXISTS data__get_email;
DROP PROCEDURE IF EXISTS data__get_allitems;
DROP PROCEDURE IF EXISTS data__count_allitems;
DROP PROCEDURE IF EXISTS data__get_emails;
DROP PROCEDURE IF EXISTS data__count_emails;
DROP PROCEDURE IF EXISTS data__get_attachments;
DROP PROCEDURE IF EXISTS data__count_attachments;
DROP PROCEDURE IF EXISTS data__get_images;
DROP PROCEDURE IF EXISTS data__count_images;
-- ---------------------------------------------------------------------


-- set delimiter
DELIMITER //

-- create sprocs

-- ---------------------------------------------------------------------
CREATE PROCEDURE data_dedup_hash__create(
    p_item_id INT,
    p_hash_D VARCHAR(32),
    p_hash_F VARCHAR(32),
    p_hash_FD VARCHAR(32),
    p_hash_B VARCHAR(32),
    p_hash_BD VARCHAR(32),
    p_hash_BF VARCHAR(32),
    p_hash_BFD VARCHAR(32),
    p_hash_M VARCHAR(32),
    p_hash_MD VARCHAR(32),
    p_hash_MF VARCHAR(32),
    p_hash_MFD VARCHAR(32),
    p_hash_MB VARCHAR(32),
    p_hash_MBD VARCHAR(32),
    p_hash_MBF VARCHAR(32),
    p_hash_MBFD VARCHAR(32))
    INSERT INTO data_dedup_hash (
        item_id, 
        hash_D, 
        hash_F, 
        hash_FD, 
        hash_B, 
        hash_BD, 
        hash_BF,
        hash_BFD,
        hash_M, 
        hash_MD, 
        hash_MF, 
        hash_MFD,
        hash_MB, 
        hash_MBD,
        hash_MBF,
        hash_MBFD)
    VALUES (
        p_item_id,
        p_hash_D, 
        p_hash_F, 
        p_hash_FD, 
        p_hash_B, 
        p_hash_BD, 
        p_hash_BF,
        p_hash_BFD,
        p_hash_M, 
        p_hash_MD, 
        p_hash_MF, 
        p_hash_MFD,
        p_hash_MB, 
        p_hash_MBD,
        p_hash_MBF,
        p_hash_MBFD);
//

CREATE PROCEDURE data_dedup__create_nonemailpst(
    p_item_id INT,
    p_md5sum VARCHAR(250))
    INSERT INTO data_dedup (item_id, pst_md5sum) VALUES (p_item_id, p_md5sum);
//

CREATE PROCEDURE data_dedup__get()
    SELECT item_id, file_md5sum, pst_md5sum, email_messageid FROM data_dedup ORDER BY item_id;
//

-- ---------------------------------------------------------------------
CREATE PROCEDURE data_item__get_md5sums()
    SELECT item_id, file_md5sum FROM data_item WHERE file_md5sum IS NOT NULL ORDER BY item_id;
//

CREATE PROCEDURE data_item__read(
    p_item_id INT) 
    SELECT * FROM data_item WHERE item_id = p_item_id;
//

CREATE PROCEDURE data_item__update_md5sum(
    p_item_id INT,
    p_md5sum VARCHAR(32))
    UPDATE data_item 
    SET file_md5sum = p_md5sum
    WHERE item_id = p_item_id
//

-- ---------------------------------------------------------------------
CREATE PROCEDURE fileitem__get()
    SELECT i.id, i.source_id, fi.extension
    FROM fileitem fi INNER JOIN item i ON i.id = fi.item_id;
//

-- ---------------------------------------------------------------------
CREATE PROCEDURE item__get_origin_pstfolders()
    SELECT 
        i.id,
        i.public_id,
        p.id
    FROM item i 
    INNER JOIN pstitem pi ON i.origin_id IS NULL AND pi.item_id = i.id 
    INNER JOIN pstfolder p ON p.id = pi.pstfolder_id;
//

CREATE PROCEDURE item__get_nonorigin_pstfolders()
    SELECT 
        i.id,
        i.public_id,
        p.id
    FROM item i 
    INNER JOIN pstitem pi ON pi.item_id = i.origin_id
    INNER JOIN pstfolder p ON p.id = pi.pstfolder_id;
//

CREATE PROCEDURE item__get_children(
    p_item_id INT)
    SELECT id FROM item WHERE parent_id = p_item_id;
//

CREATE PROCEDURE item__get_publicids()
    SELECT 
        id,
        public_id
    FROM item;
//

-- ---------------------------------------------------------------------
CREATE PROCEDURE item_label__create(
    p_item_id INT, 
    p_label_id INT)
    INSERT INTO item_label (item_id, label_id) 
    VALUES(p_item_id, p_label_id);
//

CREATE PROCEDURE item_label__delete_by_item(
    p_item_id INT)
    DELETE FROM item_label 
    WHERE item_id = p_item_id;    
//

CREATE PROCEDURE item_label__get_by_item(
    p_item_id INT)
    SELECT
        il.item_id,
        l.id,
        l.name
    FROM label l
    LEFT OUTER JOIN item_label il ON l.id = il.label_id AND il.item_id = p_item_id
    ORDER BY l.name;
//


-- ---------------------------------------------------------------------
CREATE PROCEDURE item_property__get_by_item(
    p_item_id INT)
    SELECT
        ip.property_id, 
        ip.value, 
        p.name
    FROM item_property ip 
    INNER JOIN property p ON p.id = ip.property_id AND ip.item_id = p_item_id
    ORDER BY ip.property_id;
//

CREATE PROCEDURE item_property__get_by_property(
    p_property_id INT)
    SELECT
        item_id, 
        value 
    FROM item_property WHERE property_id = p_property_id
    ORDER BY property_id;
//


-- --------------------------------------------------------------------- #
CREATE PROCEDURE item_relationship__create(
    p_item1_id INT,
    p_reltype_id INT,
    p_item2_id INT,
    p_value VARCHAR(25))
    INSERT INTO item_relationship (item1_id, reltype_id, item2_id, value)
        VALUES (p_item1_id, p_reltype_id, p_item2_id, p_value);
//

CREATE PROCEDURE item_relationship__get_by_item1(
    p_item_id INT)
    SELECT
        reltype_id, 
        item2_id, 
        value 
    FROM item_relationship WHERE item1_id = p_item_id;
//

CREATE PROCEDURE item_relationship__get_by_item2(
    p_item_id INT)
    SELECT
        item1_id, 
        reltype_id, 
        value
    FROM item_relationship WHERE item2_id = p_item_id;
//

CREATE PROCEDURE item_relationship__get_by_reltype(
    p_reltype_id INT)
    SELECT
        item1_id, 
        item2_id,
        value
    FROM item_relationship WHERE reltype_id = p_reltype_id;
//

CREATE PROCEDURE item_relationship__get_item1_by_reltype(
    p_reltype_id INT)
    SELECT item1_id FROM item_relationship WHERE reltype_id = p_reltype_id;
//

-- ---------------------------------------------------------------------
CREATE PROCEDURE label__create(
    p_name VARCHAR(100))
    BEGIN
        INSERT INTO label(name) VALUES(p_name);
        SELECT LAST_INSERT_ID();
    END 
//

CREATE PROCEDURE label__update(
    p_id INT, 
    p_name VARCHAR(100))
    UPDATE label SET name = p_name WHERE id = p_id;
//

CREATE PROCEDURE label__delete(
    p_id INT)
    BEGIN
        DELETE FROM item_label WHERE label_id = p_id;
        DELETE FROM label WHERE id = p_id;
    END
//

CREATE PROCEDURE label__get()
    SELECT id, name FROM label ORDER BY name;
//

CREATE PROCEDURE label__get_count()
    SELECT l.id, l.name, count(il.label_id) 
    FROM label l 
    LEFT OUTER JOIN item_label il ON il.label_id = l.id 
    GROUP BY l.id ORDER BY l.name;
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE mimetype__get()
    SELECT id, name FROM mimetype ORDER BY name;
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE mimesubtype__get()
    SELECT id, name FROM mimesubtype ORDER BY name;
//

CREATE PROCEDURE mimesubtype__get_by_subset(
    p_subset_id INT)
    SELECT
        m.id,
        m.name,
        sm.subset_id
    FROM mimesubtype m
    LEFT OUTER JOIN subset_mimesubtype sm ON m.id = sm.mimesubtype_id AND sm.subset_id = p_subset_id
    ORDER BY m.name;
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE property__get()
    SELECT id, propertytype_id, name FROM property ORDER BY name;
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE pstfolder__get_by_source(
    p_source_id INT)
    SELECT 
        id, 
        parent_id,
        name
        FROM pstfolder WHERE source_id = p_source_id ORDER BY parent_id, name;
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE pstitem__get()
    SELECT item_id, psttype_id FROM pstitem ORDER BY item_id;
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE psttype__get()
    SELECT id, name FROM psttype ORDER BY name;
//


CREATE PROCEDURE psttype__get_by_subset(
    p_subset_id INT)
    SELECT
        t.id,
        t.name,
        st.subset_id
    FROM psttype t
    LEFT OUTER JOIN subset_originpsttype st ON t.id = st.psttype_id AND st.subset_id = p_subset_id
    ORDER BY t.name;
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE redaction__get()
    SELECT id, redactrule_id, original, generated_val FROM redaction
//

CREATE PROCEDURE redaction__get_by_query(
    p_query VARCHAR(1000))
    BEGIN        
        SET @query = p_query;
        SET @s = CONCAT('
            SELECT 
                r.id, 
                rr.id, 
                rr.name, 
                r.original, 
                r.generated_val, 
                COUNT(ir.item_id)
            FROM redaction r 
            INNER JOIN redactrule rr ON rr.id = r.redactrule_id  
            INNER JOIN item_redaction ir ON ir.redaction_id = r.id ', @query);
        PREPARE stmt FROM @s;       
        EXECUTE stmt;
    END
//

CREATE PROCEDURE redaction__count_by_query(
    p_query VARCHAR(1000))
    BEGIN        
        SET @query = p_query;
        SET @s = CONCAT('SELECT count(*) 
            FROM redaction r 
            INNER JOIN redactrule rr ON rr.id = r.redactrule_id ', @query);
        PREPARE stmt from @s;       
        EXECUTE stmt;
    END
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE redactrule__get()
    SELECT id, name FROM redactrule ORDER BY name;
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE source__get()
    SELECT id, name FROM source ORDER BY name;
//

CREATE PROCEDURE source__get_by_view(
    p_viewname VARCHAR(20))
    BEGIN
        SET @viewname = p_viewname;
        SET @s = CONCAT('
            SELECT i.source_id, s.name, s.filesize, count(*) FROM ', @viewname, ' v INNER JOIN item i ON i.id = v.item_id INNER JOIN source s ON s.id = i.source_id GROUP BY i.source_id'); 
    PREPARE stmt FROM @s;
    EXECUTE stmt;
    END
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE subset__create(
    p_name VARCHAR(100),
    p_extensions VARCHAR(1000))
    BEGIN
        INSERT INTO subset (name, count, extensions) 
        VALUES(p_name, 0, p_extensions);
        SELECT LAST_INSERT_ID();  
    END  
//

CREATE PROCEDURE subset__read(
    p_id INT)
    SELECT
        s.id,
        s.name,
        s.count,
        s.extensions
    FROM subset s
    WHERE s.id = p_id;
//

CREATE PROCEDURE subset__update(
    p_id INT, 
    p_name VARCHAR(100), 
    p_count INT,
    p_extensions VARCHAR(1000))
    UPDATE subset SET 
        name = p_name,
        extensions = p_extensions,
        count = p_count
    WHERE id = p_id;
//

CREATE PROCEDURE subset__delete(
    p_id INT)
    BEGIN
        DELETE FROM subset_originpsttype WHERE subset_id = p_id;
        DELETE FROM subset_mimesubtype WHERE subset_id = p_id;
        DELETE FROM subset WHERE id = p_id;
    END
//

CREATE PROCEDURE subset__get()
    SELECT id, name, count FROM subset ORDER BY name;
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE subset_mimesubtype__create(
    p_subset_id INT, 
    p_mimesubtype_id INT)
    INSERT INTO subset_mimesubtype (subset_id, mimesubtype_id) 
    VALUES(p_subset_id, p_mimesubtype_id);
//

CREATE PROCEDURE subset_mimesubtype__delete_by_subset(
    p_subset_id INT)
    DELETE FROM subset_mimesubtype WHERE subset_id = p_subset_id;    
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE subset_originpsttype__create(
    p_subset_id INT, 
    p_psttype_id INT)
    INSERT INTO subset_originpsttype (subset_id, psttype_id) 
    VALUES(p_subset_id, p_psttype_id);
//

CREATE PROCEDURE subset_originpsttype__delete_by_subset(
    p_subset_id INT)
    DELETE FROM subset_originpsttype WHERE subset_id = p_subset_id;    
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE v_distro__get(
    p_viewname VARCHAR(20))
    BEGIN
        SET @viewname = p_viewname;
        SET @s = CONCAT('SELECT v.item_id, i.source_id, i.public_id FROM ', @viewname, ' v inner join item i on i.id = v.item_id ORDER BY i.source_id, i.public_id' ); 
    PREPARE stmt FROM @s;
    EXECUTE stmt;
    END
//


-- ----------------------------------------------------------------------
CREATE PROCEDURE data__get_item(item_id INT)
    SELECT
        i.item_id,
        i.source_id,
        i.source_name,
        i.parent_id,
        i.tree_level,
        i.public_id,
        i.redacttype_id,
        i.origin_id,
        i.psttype_id,
        i.psttype_name,
        i.pstfolder_id,
        i.pstfolder_name,
        i.conttype_id,
        i.conttype_name,
        i.cont_isextracted,
        i.file_mimetype_id,
        i.file_mimetype_name,
        i.file_mimesubtype_id,
        i.file_mimesubtype_name,
        i.file_mimedetector_id,
        i.file_mimedetails,
        i.file_name,
        i.file_extension,
        i.file_size,
        i.file_attch_position
    FROM data_item i
    WHERE i.item_id = item_id;
//

CREATE PROCEDURE data__get_email(item_id INT)
    SELECT
        i.item_id,
        i.email_to,
        i.email_cc,
        i.email_bcc,
        i.email_from,
        i.email_date,
        i.email_subject,
        i.email_header,
        i.email_body
    FROM data_email_items i
    WHERE i.item_id = item_id;
//

CREATE PROCEDURE data__get_allitems(query VARCHAR(1000))
    BEGIN        
        SET @query = query;
        SET @s = CONCAT('
            SELECT 
                i.item_id, 
                i.source_id,
                i.source_name,
                i.public_id,
                i.psttype_id,
                i.psttype_name
            FROM data_all_items di
            INNER JOIN data_item i ON i.item_id = di.item_id ', @query);
        PREPARE stmt from @s;       
        EXECUTE stmt;
    END
//

CREATE PROCEDURE data__count_allitems(query VARCHAR(1000))
    BEGIN        
        SET @query = query;
        SET @s = CONCAT('SELECT count(*) FROM data_all_items di
            INNER JOIN data_item i ON i.item_id = di.item_id ', @query);
        PREPARE stmt from @s;       
        EXECUTE stmt;
    END
//

CREATE PROCEDURE data__get_emails(query VARCHAR(1000))
    BEGIN        
        SET @query = query;
        SET @s = CONCAT('
            SELECT 
                i.item_id, 
                i.source_id, 
                i.source_name,
                i.public_id,
                di.email_from,
                di.email_to,
                di.email_date,
                di.email_subject
            FROM data_email_items di
            INNER JOIN data_item i ON i.item_id = di.item_id  ', @query);
        PREPARE stmt from @s;       
        EXECUTE stmt;
    END
//

CREATE PROCEDURE data__count_emails(query VARCHAR(1000))
    BEGIN        
        SET @query = query;
        SET @s = CONCAT('SELECT count(*) FROM data_email_items di
            INNER JOIN data_item i ON i.item_id = di.item_id ', @query);
        PREPARE stmt from @s;       
        EXECUTE stmt;
    END
//

CREATE PROCEDURE data__get_attachments(query VARCHAR(1000))
    BEGIN        
        SET @query = query;
        SET @s = CONCAT('
            SELECT 
                i.item_id, 
                i.source_id, 
                i.source_name,
                i.public_id,
                i.file_size,
                i.file_name,
                i.file_extension,
                i.file_mimetype_name,
                i.file_mimesubtype_name
            FROM data_nonemail_items di
            INNER JOIN data_item i ON i.item_id = di.item_id ', @query);
        PREPARE stmt from @s;       
        EXECUTE stmt;
    END
//

CREATE PROCEDURE data__count_attachments(query VARCHAR(1000))
    BEGIN        
        SET @query = query;
        SET @s = CONCAT('SELECT count(*) FROM data_nonemail_items di
            INNER JOIN data_item i ON i.item_id = di.item_id ', @query);
        PREPARE stmt from @s;       
        EXECUTE stmt;
    END
//

CREATE PROCEDURE data__get_images(query VARCHAR(1000))
    BEGIN
        SET @query = query;
        SET @s = CONCAT('
            SELECT 
                i.item_id, 
                i.source_id, 
                i.public_id, 
                i.redacttype_id, 
                i.file_mimesubtype_name, 
                i.file_extension, 
                i.file_size
            FROM data_item i WHERE i.file_mimetype_id = 3 ', @query);
        PREPARE stmt from @s;       
        EXECUTE stmt;
    END
//

CREATE PROCEDURE data__count_images(query VARCHAR(1000))
    BEGIN        
        SET @query = query;
        SET @s = CONCAT('SELECT count(*) FROM data_nonemail_items di
            INNER JOIN data_item i ON i.item_id = di.item_id ', @query);
        PREPARE stmt from @s;       
        EXECUTE stmt;
    END
//

-- ----------------------------------------------------------------------

-- reset delimiter
DELIMITER ; 
