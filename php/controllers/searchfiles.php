<?php
namespace Controller;

require "../webcontrols/pager.php";
require "../webcontrols/dropdownlist.php";
require "../models/repository.php";

class SearchFiles extends BaseController
{
    const label_id     = "label";
    const source_id     = "source";
    const mt_id         = "mt";
    const mst_id        = "mst";
    const fname_id      = "fname";
    const extension_id  = "extension";
    const size_min_id   = "size_min";
    const size_max_id   = "size_max";
    const text_id       = "text";
    const min_text_id   = "min_text";
    const meta_id       = "meta";
    const total_id      = "total";
    const search_id     = "search";

    const dspl_name    = "dspl";
    const dspl_all     = "all";
    const dspl_calc    = "calc";
    const dspl_samp    = "samp";
    const samp_size_id = "samp_size";
    
    private $label;
    private $source;
    private $mt;
    private $mst;
    private $fname;
    private $extension;
    private $size_min;
    private $size_max;
    private $text;
    private $min_text;
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
        $this->mt        = $this->get_state(self::mt_id);
        $this->mst       = $this->get_state(self::mst_id);
        $this->fname     = $this->get_state(self::fname_id);
        $this->extension = $this->get_state(self::extension_id);
        $this->size_min  = $this->get_state(self::size_min_id);
        $this->size_max  = $this->get_state(self::size_max_id);
        $this->text      = $this->get_state(self::text_id);
        $this->min_text  = $this->get_state(self::min_text_id);
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
        $mtypes = $repo->get_mimetypes();
        $mstypes = $repo->get_mimesubtypes();
        $items = $repo->get_data_attachments($query);
   
        $this->handle_count($repo, $query);
        $this->pager->set_rows(count($items));   
        $this->set_html_vars($labels, $sources, $mtypes, $mstypes, $items);
    }

    private function handle_count($repo, $query)
    {
        if (isset($_POST[self::search_id]))
            if ($this->dspl == self::dspl_calc)
            {
                $this->total = $repo->count_data_attachments($query);
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
           $this->mt != '' || 
           $this->mst != '' || 
           $this->fname != '' || 
           $this->extension != '' || 
           $this->size_min != '' || 
           $this->size_max != '' || 
           $this->text != '' || 
           $this->min_text != '' || 
           $this->meta != '')
       {              
            if ($this->label != "")
                $sb .= " INNER JOIN item_label il ON il.label_id = $this->label AND il.item_id = i.item_id ";
            
            $sb .= " AND ";            

            if ($this->source != "")
                $sb .= " i.source_id = $this->source AND ";
            
            if ($this->mt != "")
                $sb .= " i.file_mimetype_id = $this->mt AND ";
            
            if ($this->mst != "")
                $sb .= " i.file_mimesubtype_id = $this->mst AND ";

            if ($this->fname != "")
                $sb .= " i.file_name LIKE '%$this->fname%' AND ";
            
            if ($this->extension != "")
                $sb .= " i.file_extension LIKE '%$this->extension%' AND ";
            
            if ($this->size_min != "")
                $sb .= " i.file_size >= '" . $this->size_min . "' AND ";
            
            if ($this->size_max != "")
                $sb .= " i.file_size <= '" . $this->size_max . "' AND ";

            if ($this->text != "")
                $sb .= " MATCH(di.item_text) AGAINST('$this->text' IN BOOLEAN MODE) AND ";

            if ($this->min_text != "")
                $sb .= " LENGTH(di.item_text) > $this->min_text AND ";
            
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

    private function set_html_vars($labels, $sources, $mtypes, $mstypes, $items)
    {
        $this->set('fname_id', self::fname_id);
        $this->set('extension_id', self::extension_id);
        $this->set('size_min_id', self::size_min_id);
        $this->set('size_max_id', self::size_max_id);
        $this->set('text_id', self::text_id);
        $this->set('min_text_id', self::min_text_id);
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

        $html = $ddl->get_html(self::mt_id, $mtypes, $this->mt, 0, 1, true, 'data');
        $this->set('mt_html', $html);
        
        $html = $ddl->get_html(self::mst_id, $mstypes, $this->mst, 0, 1, true, 'data');
        $this->set('mst_html', $html);
        
        $html = $this->get_items_html($items);
        $this->set('items_html', $html);
        
        $this->set('hidden_html', $this->get_hidden_html());
        
        if ($this->dspl == self::dspl_samp)
            $this->set('grid_title_html', "<div style='font-size:110%;font-weight:bold;padding:10px 0px 9px 0px;'>Displaying random sample of " . $this->samp_size . "</div>");
        else
            $this->set('grid_title_html', $this->pager->get_html());

        $this->set('fname', $this->fname);
        $this->set('extension', $this->extension);
        $this->set('size_min', $this->size_min);
        $this->set('size_max', $this->size_max);
        $this->set('text', $this->text);
        $this->set('min_text', $this->min_text);
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
            $size           = $row[4];
            $name           = $row[5];
            $extension      = $row[6];
            $mt_name        = $row[7];
            $mst_name       = $row[8];

            $mt = "$mt_name/$mst_name";

            $sb .= "\n\t<tr>";
            $sb .= "\n\t\t<td>$item_id</td>";
            $sb .= "\n\t\t<td>$public_id</td>";
            $sb .= "\n\t\t<td>$source_name</td>";
            $sb .= "\n\t\t<td>$mt</td>";
            $sb .= "\n\t\t<td align='right'>$size</td>";
            $sb .= "\n\t\t<td>$name</td>";
            $sb .= "\n\t\t<td>$extension</td>";
            $sb .= "\n\t\t<td><a target='_blank' href='?page=viewitem&id=$item_id'>view details</a></td>";
            $sb .= "\n\t</tr>";
        }
        return $sb;
    }
}

