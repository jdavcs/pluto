<?php
namespace Model;

class Subset extends BaseModel
{
    private $subset_id;              
    private $name;            
    private $itemcount;          
    private $extensions;         

    private $originpsttypes;
    private $mimesubtypes;

    function __construct($subset_id)
    {
        parent::__construct();
        
        $db = new \Db();
        $db->open();

        $subset = $db->get_record("subset__read", true, $subset_id);

        $params = array("0" => $subset_id);
        $this->originpsttypes = $db->get_records("psttype__get_by_subset", true, $params);
        $this->mimesubtypes = $db->get_records("mimesubtype__get_by_subset", true, $params); 

        $db->close();

        $this->subset_id  = $subset[0];
        $this->name       = $subset[1];
        $this->itemcount  = $subset[2];
        $this->extensions = $subset[3];
    }

    function subset_id() { return $this->subset_id; }             
        
    function name() { return $this->name; }            

    function itemcount() { return $this->itemcount; }          

    function extensions() { return $this->extensions; }            
    
    function originpsttypes() { return $this->originpsttypes; }

    function mimesubtypes() { return $this->mimesubtypes; }
}

