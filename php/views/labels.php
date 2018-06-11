<?php echo $form_html ?>

<p class="pagetitle">Labels</p>

<table cellpadding="2">
    <tr>
        <td><input type="text" id="<?php echo $lname_id?>" 
                name="<?php echo $lname_id?>" maxlength="50" 
                style="width:200px"/></td>
        <td><input type="submit" id="<?php echo $create_id?>" 
                name="<?php echo $create_id?>" value="Create New"/></td>
    </tr>
</table>

<p>

<table cellpadding='5' cellspacing='1' class='grid'>
    <tr class='hdrRow'>
        <td>Label</td>
        <td>Item Count</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
    </tr>
    <?php echo $labels_html?>
</table>

</form>
