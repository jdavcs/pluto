<?php
namespace Model;

class Item extends BaseModel
{
    private $item_id;              
    private $source_id;            
    private $source_name;          
    private $parent_id;         
    private $tree_level;           
    private $publicid;            
    private $redacttype_id;
    private $origin_id;            
    private $psttype_id;           
    private $psttype_name;         
    private $pstfolder_id;        
    private $pstfolder_name;       
    private $conttype_id;      
    private $conttype_name;        
    private $cont_isextracted;     
    private $file_mimetype_id;     
    private $file_mimetype_name;   
    private $file_mimesubtype_id;  
    private $file_mimesubtype_name;
    private $file_mimedetector_id; 
    private $file_mimedetails;     
    private $file_name;            
    private $file_extension; 
    private $file_size;           
    private $file_attch_position;

    private $properties;
    private $relationships1;
    private $relationships2;
    private $redactions;
    private $labels;

    function __construct($item_id)
    {
        parent::__construct();
        
        $db = new \Db();
        $db->open();

        $item = $db->get_record("data__get_item", true, $item_id);

        $params = array("0" => $item_id);
        $this->properties = $db->get_records("item_property__get_by_item", true, $params);
        $this->relationships1 = $db->get_records("item_relationship__get_by_item1", true, $params); //item = object
        $this->relationships2 = $db->get_records("item_relationship__get_by_item2", true, $params); //item = subject
        $this->labels = $db->get_records("item_label__get_by_item", true, $params);

        $db->close();

        $this->item_id                = $item[0];
        $this->source_id              = $item[1];
        $this->source_name            = $item[2];
        $this->parent_id              = $item[3];
        $this->tree_level             = $item[4];
        $this->publicid               = $item[5];
        $this->redacttype_id          = $item[6];
        $this->origin_id              = $item[7];
        $this->psttype_id             = $item[8];
        $this->psttype_name           = $item[9];
        $this->pstfolder_id           = $item[10];
        $this->pstfolder_name         = $item[11];
        $this->conttype_id            = $item[12];
        $this->conttype_name          = $item[13];
        $this->cont_isextracted       = $item[14];
        $this->file_mimetype_id       = $item[15];
        $this->file_mimetype_name     = $item[16];
        $this->file_mimesubtype_id    = $item[17];
        $this->file_mimesubtype_name  = $item[18];
        $this->file_mimedetector_id   = $item[19];
        $this->file_mimedetails       = $item[20];
        $this->file_name              = $item[21];
        $this->file_extension         = $item[22];
        $this->file_size              = $item[23];
        $this->file_attch_position    = $item[24];
    }

    function item_id() { return $this->item_id; }             
        
    function source_id() { return $this->source_id; }            

    function source_name() { return $this->source_name; }          

    function parent_id() { return $this->parent_id; }            

    function tree_level() { return $this->tree_level; }           

    function publicid() { return $this->publicid; }             

    function redacttype_id() { return $this->redacttype_id; }        

    function origin_id() { return $this->origin_id; }            

    function psttype_id() { return $this->psttype_id; }           

    function psttype_name() { return $this->psttype_name; }         

    function pstfolder_id() { return $this-pstfolder_id; }         

    function pstfolder_name() { return $this->pstfolder_name; }       

    function conttype_id() { return $this->conttype_id; }          

    function conttype_name() { return $this->conttype_name; }        

    function cont_isextracted() { return $this->cont_isextracted; }     

    function file_mimetype_id() { return $this->file_mimetype_id; }     

    function file_mimetype_name() { return $this->file_mimetype_name; }   

    function file_mimesubtype_id() { return $this->file_mimesubtype_id; }  

    function file_mimesubtype_name() { return $this->file_mimesubtype_name; }

    function file_mimedetector_id() { return $this->file_mimedetector_id; } 

    function file_mimedetails() { return $this->file_mimedetails; }     

    function file_name() { return $this->file_name; }            

    function file_extension() { return $this->file_extension; }       

    function file_size() { return $this->file_size; }            

    function file_attch_position() { return $this->file_attch_position; } 

    function properties() { return $this->properties; }

    function relationships1() { return $this->relationships1; }

    function relationships2() { return $this->relationships2; }

    function redactions() { return $this->redactions; }
    
    function labels() { return $this->labels; }

    function update_labels($newlabels)
    {
        $db = new \Db();
        $db->open();

        $db->execute("item_label__delete_by_item", true, $this->item_id);

        foreach($newlabels as $label_id)
        {
            $params = array();
            $params["0"] = $this->item_id;
            $params["1"] = $label_id;
            $db->execute("item_label__create", true, $params);
        }
        $db->close();            
    }
}

