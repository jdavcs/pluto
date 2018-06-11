<?php

class SqlFactory
{
    function get_distro_view($id, $origin_ids, $mst_ids, $extensions, $command)
    {
        $name = $this->get_distro_view_name($id);
        $sb = "";
        $sb .= "\n$command VIEW $name \nAS";
        $sb .= "\nSELECT di.item_id";
        $sb .= "\nFROM data_item di ";
        $sb .= "\nLEFT OUTER JOIN data_item odi ON odi.item_id = di.origin_id";
        $sb .= "\nWHERE 1 ";  //placeholder so we don't choose what following block to treat as first conditional with a 'where'

        if (count($origin_ids) > 0)
        {
            $sb .= "\nAND /* filter by origin type */";
            $sb .= "\n(";
            foreach ($origin_ids as $id)            
                $sb .= "\n\t((di.origin_id IS NULL AND di.psttype_id = $id) OR odi.psttype_id = $id) OR ";
            $sb = substr($sb, 0, strlen($sb)-4);

            $sb .= "\n)";
        }

        if (count($mst_ids) > 0)
        {
            $sb .= "\nAND /* filter by mime subtype */";
            $sb .= "\n(";
            $sb .= "\n\tdi.file_mimetype_id IS NULL OR";
            foreach ($mst_ids as $id)            
                $sb .= "\n\tdi.file_mimetype_id = $id OR ";
            $sb = substr($sb, 0, strlen($sb)-4);

            $sb .= "\n)";
        }

        if ($extensions != "")
        {
            $sb .= "\nAND /* exclude file extensions */";
            $sb .= "\n(";
            $sb .= "\n\tdi.file_extension IS NULL OR";
            $sb .= "\n\t(";

            $ext_arr = explode("\n", $extensions);
            foreach ($ext_arr as $e)            
                $sb .= "\n\t\tdi.file_extension NOT LIKE '" . trim($e) . "' AND ";
            $sb = substr($sb, 0, strlen($sb)-5);

            $sb .= "\n\t)";
            $sb .= "\n)";
        }
        $sb .= ";";
        return $sb;
    }

    function get_distro_view_name($id)
    {
        return "v_distro_$id";
    }
}

