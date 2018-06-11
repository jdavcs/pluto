CREATE INDEX in_mimesubtype_name
    ON mimesubtype(name);

CREATE INDEX in_containeritem_isextracted
    ON containeritem(is_extracted);

CREATE INDEX in_fileitem_mimedetails
    ON fileitem(mime_details(10));

CREATE INDEX in_fileitem_extension
    ON fileitem(extension(5));

CREATE INDEX in_fileitem_filesize
    ON fileitem(filesize);

CREATE INDEX in_fileitem_mime
    ON fileitem(mimetype_id, mimesubtype_id);

CREATE INDEX in_property_name
    ON property(name);

CREATE INDEX in_pstfolder_name
    ON pstfolder(name);

CREATE INDEX in_itemrelationship_ri1
    ON item_relationship(reltype_id, item1_id);

CREATE INDEX in_itemrelationship_ri2
    ON item_relationship(reltype_id, item2_id);

COMMIT;
