<?php
namespace Controller;

require "../models/repository.php";
require "../lib/sql_factory.php";

class Subsets extends BaseController
{
    const action_key  = "action";
    const id_key      = "id";
    
    private $action;
    private $id;
    private $message;

    protected function load_getvalues()
    {
        $this->action = $this->get_state(self::action_key);
        $this->id     = $this->get_state(self::id_key);
    
        if ($this->get_state("message") == "add")
            $this->message = "Subset has been added";
        else if ($this->get_state("message") == "update")
            $this->message = "Subset has been updated";
    }
    
    protected function process_events()
    {
        if ($this->action == self::ACTION_DELETE)
        {
            $repo = new \Model\Repository();
            $repo->delete_subset($this->id);
            $sf = new \SqlFactory();
            $viewname = $sf->get_distro_view_name($this->id);
            $repo->execute_sql("DROP VIEW $viewname;");
            
            $repo = null;
            header("Location: ?page=subsets");
        }
    }

    function main()
    {
        $repo = new \Model\Repository();
        $subsets = $repo->get_subsets();
        $repo = null;
        $this->set_html_vars($subsets);
    }

    private function set_html_vars($subsets)
    {
        $html = $this->get_subsets_html($subsets);
        $this->set('subsets_html', $html);
        $this->set('message', $this->message);
    }

    private function get_subsets_html($subsets)
    {
        $sf = new \SqlFactory();
        $sb = "";
        foreach ($subsets as $row)
        {
            $id        = $row[0];
            $name      = $row[1];
            $itemcount = $row[2];
            $viewname = $sf->get_distro_view_name($id);             

            if ($itemcount == 0)
                $itemcount = ""; //for layout purposes

            $sb .= "\n\t<tr>";
            $sb .= "\n\t\t<td>$name</td>";
            $sb .= "\n\t\t<td>$viewname</td>";
            $sb .= "\n\t\t<td align='right'>$itemcount</td>";
            $sb .= "\n\t\t<td><a blank' href='?page=edit_subset&id=$id'>edit</a></td>";
            $sb .= "\n\t\t<td><a class='deleteCell' onclick=\"return confirm('delete subset?')\" href='?page=subsets&action=" . self::ACTION_DELETE ."&id=$id'>delete</a></td>";
            $sb .= "\n\t</tr>";
        }
        return $sb;
    }
}

