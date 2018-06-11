<?php
namespace Controller;

require "../models/repository.php";

class Labels extends BaseController
{
    const lname_id    = "name";
    const create_id   = "create";
    const new_name_id = "newname";
    const update_id   = "update";
    const cancel_id   = "cancel";
    const action_key  = "action";
    const id_key      = "id";
    
    private $lname;
    private $create;
    private $new_name;
    private $update;
    private $cancel;
    private $action;
    private $id;
    
    protected function load_postvalues()
    {
        $this->lname    = $this->get_state(self::lname_id);
        $this->create   = $this->get_state(self::create_id);
        $this->new_name = $this->get_state(self::new_name_id);
        $this->update   = $this->get_state(self::update_id);
        $this->cancel   = $this->get_state(self::cancel_id);
    }

    protected function load_getvalues()
    {
        $this->action = $this->get_state(self::action_key);
        $this->id     = $this->get_state(self::id_key);
    }

    protected function process_events()
    {
        if ($this->create != "")
        {
            $repo = new \Model\Repository();
            $repo->create_label($this->lname);
            $repo = null;
            $this->action = "";
        }
        else if ($this->update != "")
        {
            $repo = new \Model\Repository();
            $repo->update_label($this->id, $this->new_name);
            $repo = null;
            $this->action = "";
        }
        else if ($this->cancel != "")
        {
            $this->action = "";
        }
        else if ($this->action == self::ACTION_DELETE)
        {
            $repo = new \Model\Repository();
            $repo->delete_label($this->id);
            $repo = null;
            $this->action = "";
        }
    }

    function main()
    {
        $repo = new \Model\Repository();
        $labels = $repo->get_labels_count();
        $repo = null;
        $this->set_html_vars($labels);
    }

    private function set_html_vars($labels)
    {
        $html = $this->get_labels_html($labels);
        $this->set('lname_id', self::lname_id);
        $this->set('create_id', self::create_id);
        $this->set('labels_html', $html);
    }

    private function get_labels_html($labels)
    {
        $sb = "";
        foreach ($labels as $row)
        {
            $id        = $row[0];
            $name      = $row[1];
            $itemcount = $row[2];

            if ($itemcount == 0)
                $itemcount = ""; //for layout purposes

            $sb .= "\n\t<tr>";

            if ($id == $this->id && $this->action == self::ACTION_EDIT)
            {
                $sb .= "\n\t\t<td colspan='4' class='formtdedit'>";
                $sb .= "<input name='" . self::new_name_id . "' type='text' value='$name'/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
                $sb .= "<input type='submit' name='" . self::update_id . "' value='Update'/>";
                $sb .= "<input type='submit' name='" . self::cancel_id . "' value='Cancel'/>";
                    
                $sb .= "</td>";
            }
            else
            {
                $sb .= "\n\t\t<td>$name</td>";
                $sb .= "\n\t\t<td align='right'>$itemcount</td>";
                $sb .= "\n\t\t<td><a blank' href='?page=labels&action=" . self::ACTION_EDIT ."&id=$id'>edit</a></td>";

                if ($itemcount != "")
                    $sb .= "\n\t\t<td align='center'>n/a</td>";
                else
                    $sb .= "\n\t\t<td><a class='deleteCell' onclick=\"return confirm('delete label?')\" href='?page=labels&action=" . self::ACTION_DELETE ."&id=$id'>delete</a></td>";
            }
            $sb .= "\n\t</tr>";
        }
        return $sb;
    }
}

