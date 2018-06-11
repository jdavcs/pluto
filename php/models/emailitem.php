<?php
namespace Model;

class EmailItem extends BaseModel
{
    private $item_id;
    private $to;
    private $cc;    
    private $bcc;    
    private $from;   
    private $e_date;   
    private $subject;
    private $e_header;
    private $body;

    function __construct($item_id)
    {
        parent::__construct();

        $db = new \Db();
        $db->open();
        $item = $db->get_record("data__get_email", true, $item_id);
        $db->close();

        $this->item_id  = $item[0];
        $this->to       = $item[1];   
        $this->cc       = $item[2];  
        $this->bcc      = $item[3]; 
        $this->from     = $item[4];
        $this->e_date   = $item[5];
        $this->subject  = $item[6];
        $this->e_header = $item[7];
        $this->body     = $item[8];
    }

    function item_id() { return $this->item_id; }
    
    function to() { return $this->to; }     

    function cc() { return $this->cc; }      

    function bcc() { return $this->bcc; }     

    function from() { return $this->from; }    

    function e_date() { return $this->e_date; }    

    function subject() { return $this->subject; }

    function e_header() { return $this->e_header; }  

    function body() { return $this->body; }   
} 
