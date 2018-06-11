<?php
namespace WebControl;

class DropDownList extends BaseControl
{
    function get_html($id, $data, $selected_value, $data_index, $text_index, $show_select_all, $css)
    {
        $sb = "";
        $sb .= "\n<select id='$id' name='$id' cssClass='$css'>";

        if ($show_select_all)
            $sb .= "\n\t<option value=''>Select all</option>";

        $select = "";
        foreach ($data as $row)
        {
           if ($row[$data_index] == $selected_value)
               $select = " selected";
           $sb .= "\n\t<option value='$row[$data_index]'$select>$row[$text_index]</option>";
                $select = "";
        }
        $sb .= "\n</select>";
        return $sb;
    }
}

