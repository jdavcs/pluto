<?php
namespace Model;

class Repository extends BaseModel
{
    private $db;

    function __construct()
    {
        parent::__construct();

        $this->db = new \Db();
        $this->db->open();
    }

    function __destruct()
    {
        $this->db->close();
        parent::__destruct();
    }

    function execute_sql($sql)
    {
        return $this->db->execute($sql, false);
    }
    
    function get_scalar_sql($sql) 
    {
        return $this->db->get_scalar($sql, false); 
    }

/* -------------------------CREATE------------------------------ */

    function create_subset($name, $extensions) 
    {
        $p = array();
        $p[] = $name;
        $p[] = $extensions;
        return $this->db->get_scalar("subset__create", true, $p);
    }
    
    function create_label($name) {
        return $this->db->get_scalar("label__create", true, $name); 
    }

/* -------------------------DELETE------------------------------ */

    function delete_subset($id) {
        return $this->db->execute("subset__delete", true, $id); }

/* -------------------------LINKS---------------------------- */
    function link_subset_originpsttype($subset_id, $psttype_ids)
    {
        $this->db->execute("subset_originpsttype__delete_by_subset", true, $subset_id); 
        foreach($psttype_ids as $id)
        {
            $p = array();
            $p[] = $subset_id;
            $p[] = $id;
            $this->db->execute("subset_originpsttype__create", true, $p); 
        }      
    }        

    function link_subset_mimesubtype($subset_id, $mst_ids)
    {
        $this->db->execute("subset_mimesubtype__delete_by_subset", true, $subset_id); 
        foreach($mst_ids as $id)
        {
            $p = array();
            $p[] = $subset_id;
            $p[] = $id;
            $this->db->execute("subset_mimesubtype__create", true, $p); 
        }      
    }        

/* -------------------------GET RECORDSETS---------------------- */

    function get_subsets() {
        return $this->db->get_records("subset__get", true); }         

    function get_redactrules() {
        return $this->db->get_records("redactrule__get", true); }         

    function get_redactions($query) {
        return $this->db->get_records("redaction__get_by_query", true, $query); }         
            
    function count_redactions($query) {
        return $this->db->get_scalar("redaction__count_by_query", true, $query); }
            
/* -------------------------UPDATE------------------------------ */

    function update_subset($id, $name, $extensions, $count) 
    {
        $p = array();
        $p[] = $id;
        $p[] = $name;
        $p[] = $extensions;
        $p[] = $count;
        return $this->db->execute("subset__update", true, $p); 
    }

    function update_label($id, $name) 
    {
        $p = array();
        $p[] = $id;
        $p[] = $name;
        return $this->db->execute("label__update", true, $p); 
    }

    function delete_label($id) {
        return $this->db->execute("label__delete", true, $id); }
            
    function get_data_all($query) {   
        return $this->db->get_records("data__get_allitems", true, $query); }
    
    function count_data_all($query) {        
        return $this->db->get_scalar("data__count_allitems", true, $query); }

    function get_data_emails($query) {        
        return $this->db->get_records("data__get_emails", true, $query); }
    
    function count_data_emails($query) {        
        return $this->db->get_scalar("data__count_emails", true, $query); }

    function get_data_attachments($query) {
        return $this->db->get_records("data__get_attachments", true, $query); }
    
    function count_data_attachments($query) {
        return $this->db->get_scalar("data__count_attachments", true, $query); }
    
    function get_data_images($query) {
        return $this->db->get_records("data__get_images", true, $query); }
            
    function count_data_images($query) {
        return $this->db->get_scalar("data__count_images", true, $query); }

    function get_sources() {
        return $this->db->get_records("source__get", true); }

    function get_psttypes() {
        return $this->db->get_records("psttype__get", true); }

    function get_mimetypes() {
        return $this->db->get_records("mimetype__get", true); }

    function get_mimesubtypes() {
        return $this->db->get_records("mimesubtype__get", true); }
            
    function get_labels() {
        return $this->db->get_records("label__get", true); }
            
    function get_labels_count() {
        return $this->db->get_records("label__get_count", true); }
}

