/* create data_items table */
 
INSERT INTO data_item
    SELECT
        i.id,
        i.source_id,
        s.name,
        i.parent_id,
        i.tree_level,
        i.public_id,
        i.redacttype_id,
        i.origin_id,
        pi.psttype_id,
        pt.name,
        pi.pstfolder_id,
        pf.name,
        ci.containertype_id,
        ct.name,
        ci.is_extracted,
        fi.mimetype_id,
        mt.name,
        fi.mimesubtype_id,
        mst.name,
        fi.mimetypedetector_id,
        fi.mime_details,
        fi.original_name,
        fi.extension,
        fi.filesize,
        fi.attch_position,
        '' /*instead of hash */
    FROM item i
        LEFT OUTER JOIN pstitem pi ON pi.item_id = i.id
        LEFT OUTER JOIN containeritem ci ON ci.item_id = i.id
        LEFT OUTER JOIN fileitem fi ON fi.item_id = i.id
        LEFT OUTER JOIN psttype pt ON pt.id = pi.psttype_id
        LEFT OUTER JOIN containertype ct ON ct.id = ci.containertype_id
        LEFT OUTER JOIN mimetype mt ON mt.id = fi.mimetype_id
        LEFT OUTER JOIN mimesubtype mst ON mst.id = fi.mimesubtype_id
        LEFT OUTER JOIN pstfolder pf ON pf.id = pi.pstfolder_id
        LEFT OUTER JOIN source s ON s.id = i.source_id;
     

CREATE INDEX in_dataitem__source_id
    ON data_item (source_id);
COMMIT;

CREATE INDEX in_dataitem__redacttype_id
    ON data_item (redacttype_id);
COMMIT;

CREATE INDEX in_dataitem__origin_id
    ON data_item (origin_id);
COMMIT;

CREATE INDEX in_dataitem__psttype_id
    ON data_item (psttype_id);
COMMIT;

CREATE INDEX in_dataitem__file_mimetype_id
    ON data_item (file_mimetype_id);
COMMIT;

CREATE INDEX in_dataitem__file_mimesubtype_id
    ON data_item (file_mimesubtype_id);
COMMIT;

CREATE INDEX in_dataitem__file_name
    ON data_item (file_name);
COMMIT;

CREATE INDEX in_dataitem__file_extension
    ON data_item (file_extension);
COMMIT;

CREATE INDEX in_dataitem__file_size
    ON data_item (file_size);
COMMIT;
