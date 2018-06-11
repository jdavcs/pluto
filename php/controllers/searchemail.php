<?php
namespace Controller;

require "../webcontrols/pager.php";
require "../webcontrols/dropdownlist.php";
require "../models/repository.php";

class SearchEmail extends BaseController
{
    const label_id     = "label";
    const source_id      = "source";
    const from_id        = "from";
    const to_id          = "to";
    const cc_id          = "cc";
    const bcc_id         = "bcc";
    const date_start_id  = "date_start";
    const date_end_id    = "date_end";
    const subject_id     = "subject";
    const emailheader_id = "header";
    const body_id        = "body";
    const meta_id        = "meta";
    const total_id       = "total";
    const search_id      = "search";

    const dspl_name    = "dspl";
    const dspl_all     = "all";
    const dspl_calc    = "calc";
    const dspl_samp    = "samp";
    const samp_size_id = "samp_size";
    
    private $label;
    private $source;
    private $from;
    private $to; 
    private $cc;
    private $bcc;
    private $date_start;
    private $date_end;
    private $subject;
    private $emailheader;
    private $body;
    private $meta;
    private $total;
    private $dspl;
    private $samp_size;

    private $pager;

    function __construct($view)
    {
        parent::__construct($view);
        $this->pager = new \WebControl\Pager();
    }

    protected function load_postvalues()
    {
        $this->label        = $this->get_state(self::label_id);
        $this->source       = $this->get_state(self::source_id);
        $this->from         = $this->get_state(self::from_id);
        $this->to           = $this->get_state(self::to_id); 
        $this->cc           = $this->get_state(self::cc_id);
        $this->bcc          = $this->get_state(self::bcc_id);
        $this->date_start   = $this->get_state(self::date_start_id);
        $this->date_end     = $this->get_state(self::date_end_id);
        $this->subject      = $this->get_state(self::subject_id);
        $this->emailheader  = $this->get_state(self::emailheader_id);
        $this->body         = $this->get_state(self::body_id);
        $this->meta         = $this->get_state(self::meta_id);
        $this->total        = $this->get_state(self::total_id);
        $this->dspl         = $this->get_state(self::dspl_name);
        $this->samp_size    = $this->get_state(self::samp_size_id);
    }

    function main()
    {
        $query = $this->get_query();

        $repo = new \Model\Repository();

        $labels = $repo->get_labels();
        $sources = $repo->get_sources();
        $items = $repo->get_data_emails($query);
   
        $this->handle_count($repo, $query);
        $this->pager->set_rows(count($items));   
        $this->set_html_vars($labels, $sources, $items);
    }

    private function handle_count($repo, $query)
    {
        if (isset($_POST[self::search_id]))
            if ($this->dspl == self::dspl_calc)
            {
                $this->total = $repo->count_data_emails($query);
                $this->pager->set_total($this->total);
            }
            else
                $this->total = ""; //reset!
        else
            if ($this->total != "")            
                $this->pager->set_total($this->total);
    }

    private function get_query()
    {       
       $sb = "";
       if ($this->label != '' ||
           $this->source != '' || 
           $this->from != '' || 
           $this->to != '' || 
           $this->cc != '' || 
           $this->bcc != '' || 
           $this->date_start != '' || 
           $this->date_end != '' || 
           $this->subject != '' || 
           $this->emailheader != '' || 
           $this->body != '' || 
           $this->meta != '')
       {              
            if ($this->label != "")
                $sb .= " INNER JOIN item_label il ON il.label_id = $this->label AND il.item_id = i.item_id ";
            
            $sb .= " AND ";            

            if ($this->source != "")
                $sb .= " i.source_id = $this->source AND ";

            $date_start = $this->get_formatted_date($this->date_start);
            if ($date_start != "")
                $sb .= " di.email_date >= '" . $date_start . "' AND ";
            
            $date_end = $this->get_formatted_date($this->date_end);
            if ($date_end != "")
                $sb .= " di.email_date <= '" . $date_end . "' AND ";

            if ($this->from != "")
                $sb .= " MATCH(di.email_from) AGAINST('$this->from' IN BOOLEAN MODE) AND ";

            if ($this->to != "")                
                $sb .= " MATCH(di.email_to) AGAINST('$this->to' IN BOOLEAN MODE) AND ";

            if ($this->cc != "")
                $sb .= " MATCH(di.email_cc) AGAINST('$this->cc' IN BOOLEAN MODE) AND ";

            if ($this->bcc != "")
                $sb .= " MATCH(di.email_bcc) AGAINST('$this->bcc' IN BOOLEAN MODE) AND ";

            if ($this->subject != "")
                $sb .= " MATCH(di.email_subject) AGAINST('$this->subject' IN BOOLEAN MODE) AND ";

            if ($this->emailheader != "")
                $sb .= " MATCH(di.email_header) AGAINST('$this->emailheader' IN BOOLEAN MODE) AND ";

            if ($this->body != "")
                $sb .= " MATCH(di.email_body) AGAINST('$this->body' IN BOOLEAN MODE) AND ";

            if ($this->meta != "")
                $sb .= " MATCH(di.email_metadata) AGAINST('$this->meta' IN BOOLEAN MODE) AND ";

            $sb = substr($sb, 0, strlen($sb)-4);
 
        }
        if ($this->dspl == self::dspl_samp)
            $sb .= " ORDER BY RAND() LIMIT " . $this->samp_size;
        else
            $sb .= " LIMIT " . $this->pager->get_offset() . ", " . $this->pager->get_page_size();
        
        return $sb;        
    }

    private function set_html_vars($labels, $sources, $items)
    {
        $this->set('from_id', self::from_id);
        $this->set('to_id', self::to_id); 
        $this->set('cc_id', self::cc_id);
        $this->set('bcc_id', self::bcc_id);
        $this->set('date_start_id', self::date_start_id);
        $this->set('date_end_id', self::date_end_id);
        $this->set('subject_id', self::subject_id);
        $this->set('emailheader_id', self::emailheader_id);
        $this->set('body_id', self::body_id);
        $this->set('meta_id', self::meta_id);
        $this->set('total_id', self::total_id);
        $this->set('search_id', self::search_id);
        $this->set('reset_id', self::RESET_ID);
            
        $this->set('dspl_name', self::dspl_name);
        $this->set('dspl_all', self::dspl_all);
        $this->set('dspl_calc', self::dspl_calc);
        $this->set('dspl_samp', self::dspl_samp);
        $this->set('samp_size_id', self::samp_size_id);

        $ddl = new \WebControl\DropDownList();

        $html = $ddl->get_html(self::label_id, $labels, $this->label, 0, 1, true, 'data');
        $this->set('label_html', $html);
        
        $html = $ddl->get_html(self::source_id, $sources, $this->source, 0, 1, true, 'data');
        $this->set('source_html', $html);
        
        $html = $this->get_items_html($items);
        $this->set('items_html', $html);
        
        $this->set('hidden_html', $this->get_hidden_html());
        
        if ($this->dspl == self::dspl_samp)
            $this->set('grid_title_html', "<div style='font-size:110%;font-weight:bold;padding:10px 0px 9px 0px;'>Displaying random sample of " . $this->samp_size . "</div>");
        else
            $this->set('grid_title_html', $this->pager->get_html());

        $this->set('from', $this->from);
        $this->set('to', $this->to); 
        $this->set('cc', $this->cc);
        $this->set('bcc', $this->bcc);
        $this->set('date_start', $this->date_start);
        $this->set('date_end', $this->date_end);
        $this->set('subject', $this->subject);
        $this->set('emailheader', $this->emailheader);
        $this->set('body', $this->body);
        $this->set('meta', $this->meta);
        $this->set('total', $this->total);
        $this->set('meta', $this->meta);
        
        $this->set('samp_size', $this->samp_size);
    }

    private function get_hidden_html()
    {
        return $sb = "\n<input type='hidden' id='" . self::total_id . 
            "' name='" . self::total_id . "' value='" . $this->total . "'/>";
    }

    private function get_items_html($items)
    {
        $sb = "";
        foreach ($items as $row)
        {
            $item_id        = $row[0];
            $source_id      = $row[1];
            $source_name    = $row[2];
            $public_id      = $row[3];
            $from           = $row[4];
            $to             = $row[5];
            $date           = $row[6];
            $subject        = $row[7];

            //hack: removes internal outlook data
            $pos = strpos($from, '/');
            if ($pos > -1)
                $from = substr($from, 0, $pos-2);

            $sb .= "\n\t<tr>";
            $sb .= "\n\t\t<td>$item_id</td>";
            $sb .= "\n\t\t<td>$public_id</td>";
            $sb .= "\n\t\t<td>$source_name</td>";
            $sb .= "\n\t\t<td>$from</td>";
            $sb .= "\n\t\t<td>$to</td>";
            $sb .= "\n\t\t<td>$date</td>";
            $sb .= "\n\t\t<td>$subject</td>";
            $sb .= "\n\t\t<td><a target='_blank' href='?page=viewitem&id=$item_id'>view details</a></td>";
            $sb .= "\n\t</tr>";
        }
        return $sb;
    }
    
    private function get_formatted_date($datestr)
    {
        $sb = "";
        if ($datestr != "")
        {
            date_default_timezone_set('UTC');
            try {
                $date = date_create($datestr);
                if ($date != null)
                    $sb =  date_format($date, 'Y-m-d');
            }
            catch (Exception $e) {}
        }
        return $sb;      
    }
}

