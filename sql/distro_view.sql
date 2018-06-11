use pluto2;

CREATE VIEW v_distro (
        item_id,
        source_id,
        source_name,
        parent_id,
        tree_level,
        public_id,
        redacttype_id,
        origin_id,
        psttype_id,
        psttype_name,
        pstfolder_id,
        pstfolder_name,
        conttype_id,
        conttype_name,
        cont_isextracted,
        file_mimetype_id,
        file_mimetype_name,
        file_mimesubtype_id,
        file_mimesubtype_name,
        file_mimedetector_id,
        file_mimedetails,
        file_name,
        file_extension,
        file_size,
        file_attch_position)
    AS 
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
        fi.attch_position
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
