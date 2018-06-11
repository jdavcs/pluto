/* ADD FOREIGN KEYS */ 

ALTER TABLE item
	ADD CONSTRAINT fk_item_source
		FOREIGN KEY (source_id) REFERENCES source(id),
	ADD CONSTRAINT fk_item_item 
		FOREIGN KEY (parent_id) REFERENCES item(id),
	ADD CONSTRAINT fk_item_redacttype
		FOREIGN KEY (redacttype_id) REFERENCES redacttype(id),
	ADD CONSTRAINT fk_item_origin
		FOREIGN KEY (origin_id) REFERENCES item(id);

ALTER TABLE pstitem
	ADD CONSTRAINT fk_pstitem_item 
		FOREIGN KEY (item_id) REFERENCES item(id),
	ADD CONSTRAINT fk_pstitem_psttype
		FOREIGN KEY (psttype_id) REFERENCES psttype(id),
	ADD CONSTRAINT fk_pstitem_pstfolder
		FOREIGN KEY (pstfolder_id) REFERENCES pstfolder(id);

ALTER TABLE containeritem
	ADD CONSTRAINT fk_containeritem_item 
		FOREIGN KEY (item_id) REFERENCES item(id),
	ADD CONSTRAINT fk_containeritem_containertype
		FOREIGN KEY (containertype_id) REFERENCES containertype(id);

ALTER TABLE fileitem
	ADD CONSTRAINT fk_fileitem_item 
		FOREIGN KEY (item_id) REFERENCES item(id),
	ADD CONSTRAINT fk_fileitem_mimetype
		FOREIGN KEY (mimetype_id) REFERENCES mimetype(id),
	ADD CONSTRAINT fk_fileitem_mimesubtype
		FOREIGN KEY (mimesubtype_id) REFERENCES mimesubtype(id),
	ADD CONSTRAINT fk_fileitem_mimetypedetector
		FOREIGN KEY (mimetypedetector_id) REFERENCES mimetypedetector(id);

ALTER TABLE property
	ADD CONSTRAINT fk_property_propertytype
		FOREIGN KEY (propertytype_id) REFERENCES propertytype(id);

ALTER TABLE pstfolder
	ADD CONSTRAINT fk_pstfolder_parent
		FOREIGN KEY (parent_id) REFERENCES pstfolder(id),
	ADD CONSTRAINT fk_pstfolder_source
		FOREIGN KEY (source_id) REFERENCES source(id);        
    
ALTER TABLE item_property
	ADD CONSTRAINT fk_item_property_item
		FOREIGN KEY (item_id) REFERENCES item(id),
	ADD CONSTRAINT fk_item_property_property
		FOREIGN KEY (property_id) REFERENCES property(id);

ALTER TABLE item_relationship
	ADD CONSTRAINT fk_item_relationship_item_1
		FOREIGN KEY (item1_id) REFERENCES item(id),
	ADD CONSTRAINT fk_item_relationship_relationship
		FOREIGN KEY (reltype_id) REFERENCES relationshiptype(id),
	ADD CONSTRAINT fk_item_relationship_item_2
		FOREIGN KEY (item2_id) REFERENCES item(id);

ALTER TABLE redaction
	ADD CONSTRAINT fk_redaction_redactrule
		FOREIGN KEY (redactrule_id) REFERENCES redactrule(id);

ALTER TABLE item_redaction
	ADD CONSTRAINT fk_item_redaction_item
		FOREIGN KEY (item_id) REFERENCES item(id),
	ADD CONSTRAINT fk_item_redaction_redaction
		FOREIGN KEY (redaction_id) REFERENCES redaction(id),
	ADD CONSTRAINT fk_item_redaction_property
		FOREIGN KEY (property_id) REFERENCES property(id);

COMMIT;

