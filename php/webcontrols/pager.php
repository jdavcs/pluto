<?php
namespace WebControl;

class Pager extends BaseControl
{
    const default_page_size = 20;
    const offset_id = "_pager_offset";
    const pagesize_id = "_pager_pageSize";

    private $page_size;
    private $offset;
    private $total;
    private $rows;

    function __construct()
    {
        parent::__construct();
        $this->init();
        $this->total = "";
        $this->rows = 0;
    }

    function get_html()
    {
        $sb = "";
        $sb = $this->get_js();
        $sb .= $this->get_hiddenfield_html(self::offset_id);
        $sb .= $this->get_body();

        return $sb;
    }

    function get_offset()
    {
        return $this->offset;
    }
    
    function get_page_size()
    {
        return $this->page_size;
    }

    function set_rows($rows)
    {
        $this->rows = $rows;
    }

    private function get_js()
    {
        $sb = "\n<script type='text/javascript'>";
        $sb .= "\nfunction pagerSubmit(offset) {";
        $sb .= "\ndocument.getElementById('" . self::offset_id . "').value = offset;";
        $sb .= "\ndocument.getElementById('" . $this->config['form_id'] . "').submit(); }";
        $sb .= "\n</script>";
        return $sb;
    }

    private function get_hiddenfield_html($field)
    {
        return "\n<input type='hidden' id='" . $field ."' name='" . $field ."'/>";
    }

    function set_total($count)
    {
        if ($count != "")
            $this->total = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total: $count";
    }

    private function get_body()
    {
        $ps = $this->page_size;
        $of = $this->offset;

        $sb = "\n<table width='100%'><tr><td class='pgrRow'>";

        if ($of > 0)
            $sb .= "\n\t<a onClick='pagerSubmit($of-$ps)' href='#'><< prev</a>";
        else
            $sb .= "<span style='color:#cacaca;'><< prev</span>";

        $sb .= "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

        if ($this->rows == $ps)
            $sb .= "\n\t<a onClick='pagerSubmit($of+$ps)' href='#'>next >></a>";
        else
            $sb .= "<span style='color:#cacaca;'>next >></span>";
           
        $sb .= $this->total . "</td>";

        $sb .= "<td align='right' class='pgrRow'>";

        $sb .= "\nPage size: <select id='" . self::pagesize_id . "' name='" . self::pagesize_id . "' onChange='formSubmit();'>";

        $select = "";
        for($i=20; $i<501; $i += 10)
        {
            if ($ps == $i)
                $select = "selected";
            $sb .= "<option $select>$i</option>";
            $select = "";
        }

        $sb .= "\n</select>";
        $sb .= "</td></tr></table>";

        return $sb;
    }

    private function init()
    {
        //check if values have been passed
        if($_SERVER['REQUEST_METHOD'] == "POST")
        {
            if (isset($_POST[self::pagesize_id]))
                $this->page_size = trim($_POST[self::pagesize_id]);
            if (isset($_POST[self::offset_id]))
                $this->offset = trim($_POST[self::offset_id]);
        }
        //assign defaults if no values were passed or reset was pressed
        if ($this->page_size == "")
            $this->page_size = self::default_page_size;
        if ($this->offset == "")
            $this->offset = 0;
    }
}
