<?php
namespace Controller;

require "../webcontrols/pager.php";
require "../webcontrols/dropdownlist.php";
require "../models/repository.php";

class Redactions extends BaseController
{
    const rule_id      = "rule";
    const total_id     = "total";
    const search_id    = "search";

    const dspl_name    = "dspl";
    const dspl_all     = "all";
    const dspl_calc    = "calc";
    const dspl_samp    = "samp";
    const samp_size_id = "samp_size";

    private $rule;
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
        $this->rule      = $this->get_state(self::rule_id);
        $this->total     = $this->get_state(self::total_id);
        $this->dspl      = $this->get_state(self::dspl_name);
        $this->samp_size = $this->get_state(self::samp_size_id);
    }

    function main()
    {
        $query = $this->get_query(true);

        $repo = new \Model\Repository();

        $rules = $repo->get_redactrules();
        $redactions = $repo->get_redactions($query);
   
        $this->handle_count($repo, $query);
        $this->pager->set_rows(count($redactions));   
        $this->set_html_vars($rules, $redactions);
    }

    private function handle_count($repo, $query)
    {
        if (isset($_POST[self::search_id]))
            if ($this->dspl == self::dspl_calc)
            {
                $this->total = $repo->count_redactions($this->get_query(false));
                $this->pager->set_total($this->total);
            }
            else
                $this->total = ""; //reset!
        else
            if ($this->total != "")            
                $this->pager->set_total($this->total);
    }

    private function get_query($get_data)
    {       
       $sb = " "; 
        if ($this->rule != '')
            $sb .= " WHERE rr.id = $this->rule ";

        if ($get_data)
        {
            $sb .= " GROUP BY r.id ";

            if ($this->dspl == self::dspl_samp)
                $sb .= " ORDER BY RAND() LIMIT " . $this->samp_size;
            else
            {
                $sb .= " ORDER BY COUNT(ir.item_id) desc ";
                $sb .= " LIMIT " . $this->pager->get_offset() . ", " . $this->pager->get_page_size();
            }
        }
        return $sb;        
    }

    private function set_html_vars($rules, $redactions)
    {
        $this->set('total_id', self::total_id);
        $this->set('search_id', self::search_id);
        $this->set('reset_id', self::RESET_ID);

        $this->set('dspl_name', self::dspl_name);
        $this->set('dspl_all', self::dspl_all);
        $this->set('dspl_calc', self::dspl_calc);
        $this->set('dspl_samp', self::dspl_samp);
        $this->set('samp_size_id', self::samp_size_id);


        $ddl = new \WebControl\DropDownList();
        $html = $ddl->get_html(self::rule_id, $rules, $this->rule, 0, 1, true, 'data');
        $this->set('rule_html', $html);
        
        $html = $this->get_redactions_html($redactions);
        $this->set('redactions_html', $html);
        
        $this->set('hidden_html', $this->get_hidden_html());
        
        if ($this->dspl == self::dspl_samp)
            $this->set('grid_title_html', "<div style='font-size:110%;font-weight:bold;padding:10px 0px 9px 0px;'>Displaying random sample of " . $this->samp_size . "</div>");
        else
            $this->set('grid_title_html', $this->pager->get_html());
        
        $this->set('samp_size', $this->samp_size);
    }

    private function get_hidden_html()
    {
        return $sb = "\n<input type='hidden' id='" . self::total_id . 
            "' name='" . self::total_id . "' value='" . $this->total . "'/>";
    }

    private function get_redactions_html($redactions)
    {
        $sb = "";
        foreach ($redactions as $row)
        {
            $redaction_id = $row[0];
            $rule_id      = $row[1];
            $rule_name    = $row[2];
            $original     = $row[3];
            $generated    = $row[4];
            $count        = $row[5];

            $sb .= "\n\t<tr>";
            $sb .= "\n\t\t<td>$rule_name</td>";
            $sb .= "\n\t\t<td>$original</td>";
            $sb .= "\n\t\t<td>$generated</td>";
            $sb .= "\n\t\t<td align='right'>$count</td>";
            $sb .= "\n\t\t<td><a target='_blank' href='?page=redactionitems&id=$redaction_id'>view redacted items</a></td>";
            $sb .= "\n\t</tr>";
        }
        return $sb;
    }
}

