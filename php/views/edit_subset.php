<?php echo $form_html ?>

<p class="pagetitle"><?php echo $page_title ?> Collection Subset</p>

<table cellpadding="5" class="addedit-table">
    <tr bgcolor='#f1f1f1'>
        <td class='addedit-name'>Subset Name</td>
        <td><input type="text" id="<?php echo $sname_id?>" 
                name="<?php echo $sname_id?>" value="<?php echo $sname?>" maxlength="50" 
                style="width:300px"/>
        </td>
    </tr>
    <tr bgcolor='#E1FAD7' valign='top'>
        <td class='addedit-name'>Origin Types to Include</td>
        <td><?php echo $origins_html?></td>
    </tr>
    <tr bgcolor='#E1FAD7' valign='top'>
        <td class='addedit-name'>MIME Types to Include</td>
        <td><?php echo $mimetypes_html?></td>
    </tr>
    <tr valign='top' bgcolor='#FADFD7'>
        <td class='addedit-name'>File Extensions to Exclude<br/>(one per line)</td>
        <td><textarea id="<?php echo $ext_id?>" 
            name="<?php echo $ext_id?>" rows="10" cols="20"><?php echo $ext?></textarea>
        </td>
    </tr>

    <?php echo $sql_html ?>

    <tr bgcolor='#f1f1f1'>
        <td></td>
        <td style='padding-top:10px;'>
            <input type="submit" id="<?php echo $save_id?>" 
                name="<?php echo $save_id?>" value="Save"/>
            &nbsp;
            <input type="submit" id="<?php echo $reset_id?>" 
                name="<?php echo $reset_id?>" value="Reset"/>
        </td>
    </tr>
</table>

</form>
