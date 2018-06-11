<?php
namespace Controller;

require "../models/repository.php";
require "../models/subset.php";
require "../lib/sql_factory.php";

class EditSubset extends BaseController
{
    const sname_id      = "sname";
    const ext_id        = "ext";
    const save_id       = "save";
    const id_key        = "id";
    const prefix_origin = "origin_";
    const prefix_mst    = "mst_";
    
    private $sname;
    private $ext;
    private $ssave;
    private $id;
    
    protected function load_postvalues()
    {
        $this->sname  = $this->get_state(self::sname_id);
        $this->ext    = $this->get_state(self::ext_id);
        $this->ssave  = $this->get_state(self::save_id);
    }

    protected function load_getvalues()
    {
        $this->id = $this->get_state(self::id_key);
    }

    protected function process_events()
    {
        if ($this->ssave != "")        
            if ($this->id != "")
                $this->update_subset();
            else
                $this->create_subset();        
    }

    function main()
    {
        $repo = new \Model\Repository();

        if ($this->id != "")
        {
            $subset = new \Model\Subset($this->id);
            $this->sname = $subset->name();
            $this->ext = $subset->extensions();            
            $this->set_html_vars($repo, $subset->originpsttypes(), $subset->mimesubtypes());
        }
        else
        {
            $origins = $repo->get_psttypes();
            $mimesubtypes = $repo->get_mimesubtypes();
            $this->set_html_vars($repo, $origins, $mimesubtypes);
        }
        $repo = null;
    }

    private function set_html_vars($repo, $origins, $mimesubtypes)
    {
        $this->set('sname_id', self::sname_id);
        $this->set('ext_id', self::ext_id);
        $this->set('save_id', self::save_id);
        $this->set('reset_id', self::RESET_ID);

        $this->set('sname', $this->sname);
        $this->set('ext', $this->ext);

        $this->set('origins_html', $this->get_origins_html($origins));
        $this->set('mimetypes_html', $this->get_mimetypes_html($mimesubtypes));
        
        if ($this->id != "")
        {
            $this->set('page_title', 'Edit');
            $this->set('sql_html', $this->get_sql_html($repo, $origins, $mimesubtypes));
        }
        else
        {        
            $this->set('page_title', 'Create');
            $this->set('sql_html', '');
        }
    }

    private function get_origins_html($origins)
    {
        $sb = "";
        foreach ($origins as $row)
        {
            $id   = $row[0];
            $name = $row[1];

            $checked = "";
            if (count($row) == 6 && $row[2])
                $checked = "checked";

            $sb .= "<input type='checkbox' name='" . self::prefix_origin . $id . "' " . $checked . "> " . $name . "<br/>";
        }
        return $sb;
    }
    
    private function get_mimetypes_html($mimesubtypes)
    {
        $cols = count($mimesubtypes) / 3;

        $sb = "";

        $sb .= "\n<table>";
        $sb .= "\n<tr valign='top'>";
        $counter = 0;
        foreach ($mimesubtypes as $row)
        {
            if ($counter % $cols == 0)
                $sb .= "\n<td>";

            $id   = $row[0];
            $name = $row[1];

            $checked = "";
            if (count($row) == 6 && $row[2])
                $checked = "checked";

            $sb .= "<input type='checkbox' name='" . self::prefix_mst . $id . "' " . $checked . "> " . $name . "<br/>";
            
            if ($counter % $cols == ($cols-1))
                $sb .= "\n</td>";

            $counter++;
        }
        $sb .= "\n</tr>";
        $sb .= "\n</table>";
        return $sb;
    }

    private function get_sql_html($repo, $origins, $mimesubtypes)
    {
        $sb = "";
        $sf = new \SqlFactory();

        $origin_ids = array();
        foreach ($origins as $row)
            if (count($row) == 6 && $row[2])
                $origin_ids[] = $row[0];

        $mst_ids = array();
        foreach ($mimesubtypes as $row)
            if (count($row) == 6 && $row[2])
                $mst_ids[] = $row[0];

        $sql = $sf->get_distro_view($this->id, $origin_ids, $mst_ids, $this->ext, "[CREATE/ALTER]");

        $sb .= "<tr bgcolor='#f1f1f1' valign='top'>";
        $sb .= "<td class='addedit-name'>Current SQL</td>";
        $sb .= "<td style='padding-top:10px;'><pre>$sql</pre></td>";
        $sb .= "</tr>";

        return $sb;
    }

    private function create_subset()
    {
        $repo = new \Model\Repository();
        $id = $repo->create_subset($this->sname, $this->ext);
        $this->createupdate_helper($repo, $id, "CREATE");
        header("Location: ?page=subsets&message=add");
    }

    private function update_subset()
    {
        $repo = new \Model\Repository();
        $this->createupdate_helper($repo, $this->id, "ALTER");
        header("Location: ?page=subsets&message=update");
    }
    
    private function createupdate_helper($repo, $id, $command)
    {
        $origin_ids = array();
        foreach ($repo->get_psttypes() as $row)
        {
            $checkbox = self::prefix_origin . $row[0];
            if ($this->get_state($checkbox) == "on")
                $origin_ids[] = $row[0];           
        }
        $repo->link_subset_originpsttype($id, $origin_ids);

        $mst_ids = array();
        foreach ($repo->get_mimesubtypes() as $row)
        {
            $checkbox = self::prefix_mst . $row[0];
            if ($this->get_state($checkbox) == "on")
                $mst_ids[] = $row[0];           
        }
        $repo->link_subset_mimesubtype($id, $mst_ids);

        $sf = new \SqlFactory();
        $sql = $sf->get_distro_view($id, $origin_ids, $mst_ids, $this->ext, $command);

        $repo->execute_sql($sql);

        $viewname = $sf->get_distro_view_name($id);
        $count = $repo->get_scalar_sql("SELECT COUNT(*) FROM $viewname;");
        $repo->update_subset($id, $this->sname, $count, $this->ext);
        $repo = null;
    }
}

