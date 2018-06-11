<?php echo $form_html ?>

<p class="pagetitle">Search All Items</p>

<table cellpadding="2" class="searchfilter-table">
    <tr>
        <td class='searchfilter-name'>Label</td>
        <td><?php echo $label_html?></td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Custodian</td>
        <td><?php echo $source_html?></td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Item Type</td>
        <td><?php echo $itemtype_html?></td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Text</td>
        <td><input type="text" id="<?php echo $text_id?>" 
                name="<?php echo $text_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $text?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Metadata</td>
        <td><input type="text" id="<?php echo $meta_id?>" 
                name="<?php echo $meta_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $meta?>"/>
        </td>
    </tr>
    <tr>
        <td></td>
        <td class='searchfilter-name' style='text-align:left;'>
            <input type="radio" name="<?php echo $dspl_name?>" value="<?php echo $dspl_all?>" checked/> Display results &nbsp;(fastest option)</br>
            <input type="radio" name="<?php echo $dspl_name?>" value="<?php echo $dspl_calc?>"/> Display results and calculate total count</br>
            <input type="radio" name="<?php echo $dspl_name?>" value="<?php echo $dspl_samp?>"/> Display random sample of size
            <input type="text" id="<?php echo $samp_size_id?>" name="<?php echo $samp_size_id?>" 
            style="width:30px;text-align:right;" value="<?php echo $samp_size?>" maxlength="3"/>
             <?php echo $hidden_html?>
        </td>
    </tr>
    <tr>
        <td></td>
        <td style='padding-top:10px;'>
            <input type="submit" id="<?php echo $search_id?>" 
                name="<?php echo $search_id?>" value="Search"/>
            &nbsp;
            <input type="submit" id="<?php echo $reset_id?>" 
                name="<?php echo $reset_id?>" value="Reset"/>
        </td>
    </tr>
</table>

<p>

<table cellpadding='5' cellspacing='1' class='grid'>
    <tr>
        <td colspan='5'><?php echo $grid_title_html?></td>
    </tr>
    <tr class='hdrRow'>
        <td>Internal ID</td>
        <td>Public ID</td>
        <td>Custodian/Source</td>
        <td>Type</td>
        <td>&nbsp;</td>
    </tr>
    <?php echo $items_html?>
</table>

</form>
