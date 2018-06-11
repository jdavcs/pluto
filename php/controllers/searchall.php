<?php
namespace Controller;

require "../webcontrols/pager.php";
require "../webcontrols/dropdownlist.php";
require "../models/repository.php";

class SearchAll extends BaseController
{
    const label_id     = "label";
    const source_id    = "source";
    const itemtype_id  = "itemtype";
    const text_id      = "text";
    const meta_id      = "meta";
    const total_id     = "total";
    const search_id    = "search";

    const dspl_name    = "dspl";
    const dspl_all     = "all";
    const dspl_calc    = "calc";
    const dspl_samp    = "samp";
    const samp_size_id = "samp_size";

    private $label;
    private $source;
    private $itemtype;
    private $text;
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
        $this->label     = $this->get_state(self::label_id);
        $this->source    = $this->get_state(self::source_id);
        $this->itemtype  = $this->get_state(self::itemtype_id);
        $this->text      = $this->get_state(self::text_id);
        $this->meta      = $this->get_state(self::meta_id);
        $this->total     = $this->get_state(self::total_id);
        $this->dspl      = $this->get_state(self::dspl_name);
        $this->samp_size = $this->get_state(self::samp_size_id);
    }

    function main()
    {
        $query = $this->get_query();

        $repo = new \Model\Repository();

        $labels = $repo->get_labels();
        $sources = $repo->get_sources();
        $types = $repo->get_psttypes();
        $items = $repo->get_data_all($query);
   
        $this->handle_count($repo, $query);
        $this->pager->set_rows(count($items));   
        $this->set_html_vars($labels, $sources, $types, $items);
    }

    private function handle_count($repo, $query)
    {
        if (isset($_POST[self::search_id]))
            if ($this->dspl == self::dspl_calc)
            {
                $this->total = $repo->count_data_all($query);
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
        if ($this->label != '' || $this->source != '' || $this->itemtype != '' || $this->text != '' || $this->meta != '')
        {                
            if ($this->label != "")
                $sb .= " INNER JOIN item_label il ON il.label_id = $this->label AND il.item_id = i.item_id ";
            
            $sb .= " AND ";            

            if ($this->source != "")
                $sb .= " i.source_id = $this->source AND ";

            if ($this->itemtype != "")
                if (is_numeric($this->itemtype))
                    $sb .= " i.psttype_id = $this->itemtype AND ";
                else if ($psttype_id == "FILE")
                    $sb .= " i.psttype_id IS NULL AND ";

            if ($this->text != "")
                $sb .= " MATCH(di.item_text) AGAINST('$this->text' IN BOOLEAN MODE) AND ";

            if ($this->meta != "")
                $sb .= " MATCH(di.item_metadata) AGAINST('$this->meta' IN BOOLEAN MODE) AND ";

            $sb = substr($sb, 0, strlen($sb)-4);
        }
        if ($this->dspl == self::dspl_samp)
            $sb .= " ORDER BY RAND() LIMIT " . $this->samp_size;
        else
            $sb .= " LIMIT " . $this->pager->get_offset() . ", " . $this->pager->get_page_size();
        
        return $sb;        
    }

    private function set_html_vars($labels, $sources, $types, $items)
    {
        $this->set('text_id', self::text_id);
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

        $html = $ddl->get_html(self::itemtype_id, $types, $this->itemtype, 0, 1, true, 'data');
        $this->set('itemtype_html', $html);
        
        $html = $this->get_items_html($items);
        $this->set('items_html', $html);
        
        $this->set('hidden_html', $this->get_hidden_html());
        
        if ($this->dspl == self::dspl_samp)
            $this->set('grid_title_html', "<div style='font-size:110%;font-weight:bold;padding:10px 0px 9px 0px;'>Displaying random sample of " . $this->samp_size . "</div>");
        else
            $this->set('grid_title_html', $this->pager->get_html());

        $this->set('text', $this->text);
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
            $psttype_id     = $row[4];
            $psttype_name   = $row[5];

            if ($psttype_name == "")
                $psttype_name = "File";
            else
                $psttype_name = "PST $psttype_name";

            $sb .= "\n\t<tr>";
            $sb .= "\n\t\t<td>$item_id</td>";
            $sb .= "\n\t\t<td>$public_id</td>";
            $sb .= "\n\t\t<td>$source_name</td>";
            $sb .= "\n\t\t<td>$psttype_name</td>";
            $sb .= "\n\t\t<td><a target='_blank' href='?page=viewitem&id=$item_id'>view details</a></td>";
            $sb .= "\n\t</tr>";
        }
        return $sb;
    }
}

