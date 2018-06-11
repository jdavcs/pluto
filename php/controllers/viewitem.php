<?php
namespace Controller;

require "../models/item.php";
require "../models/emailitem.php";


class ViewItem extends BaseController
{
    const update_id = "update";
    const label_prefix = "lbl_";
    const MAX_LENGTH = 204800; 
    
    private $item_id;

    protected function load_postvalues() {}

    function __construct($view)
    {
        parent::__construct($view);
        $this->load_values();
    }

    protected function load_values()
    {
        $this->item_id = "";
        if (isset($_GET["id"]) && is_numeric($_GET["id"]))
            $this->item_id = trim($_GET["id"]);
        else
            die("Item ID invalid or not provided");
    }

    function main()
    {
        $item = new \Model\Item($this->item_id);
        
        if($_SERVER['REQUEST_METHOD'] == "POST")
            $this->update_item($item);

        $is_email = false;
        if ($item->psttype_id() == $this->config['psttype_email_id'])
        {
            $is_email = true;
            $emailitem = new \Model\EmailItem($this->item_id);
        }

        $is_file = false;
        if ($item->psttype_id() == 10 || $item->psttype_id() == null) //checking tree level is not enough: there are pst items there!
            $is_file = true;

        $mimetype = "UNKNOWN";
        if ($item->file_mimetype_id() != "")
            $mimetype = $item->file_mimetype_name() . "/" . $item->file_mimesubtype_name();

        $sb = "";
        $sb .= "<table class='datadisplay-table'>";
        $sb .= "<tr><td colspan='2' class='datadisplay-td-header'>Common Data</td></tr>";
        $sb .= $this->get_html_tr('Internal ID', $item->item_id());
        $sb .= $this->get_html_tr('Public ID', $item->publicid());
        $sb .= $this->get_html_tr('Custodian', $item->source_name());

        if ($item->parent_id() != null)
        {
            $parent_item = new \Model\Item($item->parent_id());
            if ($parent_item->psttype_id() == $this->config['psttype_email_id'])
                $parentrel = "Attached to";
            else
                $parentrel = "Extracted from";

            $sb .= $this->get_html_tr($parentrel, "<a href='?page=viewitem&id=" . $parent_item->item_id() . "'>" . $parent_item->publicid() . "</a>", False);
        }
        
        if ($item->origin_id() != null)
        {
            $origin_item = new \Model\Item($item->origin_id());        
            $sb .= $this->get_html_tr('Originated from', "<a href='?page=viewitem&id=" . $origin_item->item_id() . "'>" . $origin_item->publicid() . "</a>", False);
        }

        if ($item->psttype_id() != "")
        {
            $sb .= "<tr><td colspan='2' class='datadisplay-td-header'>PST Data</td></tr>";
            $sb .= $this->get_html_tr('PST Type', $item->psttype_name());
            $sb .= $this->get_html_tr('PST Folder', $item->pstfolder_name());
        
            if ($is_email)
            {
                $sb .= "<tr><td colspan='2' class='datadisplay-td-header'>Email Data</td></tr>";

                $sb .= $this->get_html_tr('To', $emailitem->to());
                $sb .= $this->get_html_tr('CC', $emailitem->cc());
                $sb .= $this->get_html_tr('BCC', $emailitem->bcc());
                $sb .= $this->get_html_tr('From', $emailitem->from());
                $sb .= $this->get_html_tr('Date', $emailitem->e_date());
                $sb .= $this->get_html_tr('Subject', $emailitem->subject());
                $sb .= $this->get_html_tr('Header', $emailitem->e_header());
                $sb .= $this->get_html_tr('Body', $emailitem->body());
            }
        }

        if ($is_file)
        {
            $sb .= "<tr><td colspan='2' class='datadisplay-td-header'>File Attachment Data</td></tr>";
            $sb .= $this->get_html_tr('MIME Type', $mimetype);
            
            if ($item->file_mimedetails() != null)
                $sb .= $this->get_html_tr('MIME Type Details', $item->file_mimedetails());
            
            $sb .= $this->get_html_tr('Original Filename', $item->file_name() . $item->file_extension());
            $sb .= $this->get_html_tr('File Size', $this->format_size($item->file_size()));

            if ($item->conttype_id() != null)
            {
                $extracted = "";
                if (!$item->cont_isextracted())
                    $extracted = " <span style='red'>(not extracted)</span>";

                $sb .= $this->get_html_tr('Container Type', $item->conttype_name() . $extracted);
            }

            //check for extracted text
            foreach ($item->properties() as $ip)
                if ($ip[0] == $this->config['property_file_extracted_text_id'])
                {
                    $sb .= $this->get_html_tr('Extracted Text', $ip[1]);
                    break;
                }
        }

        if (count($item->properties()) > 0)
        {
            $sb .= "<tr><td colspan='2' class='datadisplay-td-header'>Extracted Meta Data</td></tr>";
            foreach ($item->properties() as $ip)
            {
                if ($is_email)
                {
                    if ($ip[0] != $this->config['property_pst_header_id'] &&
                        $ip[0] != $this->config['property_pst_body_id'] &&
                        $ip[0] != $this->config['property_file_extracted_text_id'])
                        $sb .= $this->get_html_tr($ip[2], $ip[1]);
                }
                else
                {
                   if ($ip[0] != $this->config['property_file_extracted_text_id'])
                        $sb .= $this->get_html_tr($ip[2], $ip[1]);
                }
            }
        }
        $sb .= "</table>";

        $this->set('item_data', $sb);
        $this->set('labels_html', $this->get_labels_html($item));
    }

    function get_labels_html($item)
    {
        $sb = "";
        $sb .= "\n<table class='datadisplay-table'>";
        $sb .= "\n\t<tr><td colspan='2' class='datadisplay-td-header'>Assigned Labels</td></tr>";
        $sb .= "\n\t<td class='datadisplay-td-data'>";

        $checked = "";
        foreach ($item->labels() as $il)
        {
            if ($il[0] != null)
                $checked = "checked";
            else
                $checked = "";

            $id = self::label_prefix . $il[1];
            $sb .= "\n\t<input type='checkbox' id='$id' name='$id' " . $checked . ">" . $il[2] . "</br>";
        }            
            
        $sb .= "\n\t<br/><input type='submit' value='Update' id='" . self::update_id . "' />";
        $sb .= "&nbsp;&nbsp;&nbsp;<input type='submit' value='Reset' id='" . self::RESET_ID . "'/>";
        $sb .= "\n\t</td>";
        $sb .= "\n</table>";
        return $sb;
    }

    private function truncate($val)
    {
        if (strlen($val) > self::MAX_LENGTH)        
            return substr($val, 0, self::MAX_LENGTH) . " <p style='color:red'>...[TEXT TRUNCATED]...</p>";        
        else 
            return $val;
    }

    function get_html_tr($name, $val, $remove_specialchars = True)
    {
        $val = $this->truncate($val);
        $val = trim($val);

        if ($remove_specialchars)
            $val = htmlspecialchars($val);

        $val = str_replace("\n", "<br>", $val);
        
        $sb = "\n<tr valign='top'>";
        $sb .= "\n\t<td class='datadisplay-td-title'>$name</td>";
        $sb .= "\n\t<td class='datadisplay-td-data'>" . $val . "</td>";
        $sb .= "\n</tr>";
        return $sb;
    }

    function format_size($bytes)
    {
        $types = array('', 'KB', 'MB', 'GB');
        for( $i = 0; $bytes >= 1024 && $i < (count($types) - 1); $bytes /= 1024, $i++ );
            return( round( $bytes, 2 ) . " " . $types[$i] );
    }

    function update_item($item) //not the best implementation: later consider moving out of this file. 
    {
        $newlabels = array();
        foreach ($item->labels() as $il)
        {
            $checkboxid = self::label_prefix . $il[1];
            if (isset($_POST[$checkboxid]))
               $newlabels[] = $il[1];
        }            
        $item->update_labels($newlabels);     

        //now redirect to reload checkboxes
        header('Location: ' . $_SERVER['REQUEST_URI']);        
    }
}

