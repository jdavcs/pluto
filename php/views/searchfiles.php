<?php echo $form_html ?>

<p class="pagetitle">Search Attachments</p>

<table cellpadding="2" class="searchfilter-table">
    <tr>
        <td class='searchfilter-name'>Label</td>
        <td><?php echo $label_html?></td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Custodian</td>
        <td><?php echo $source_html; ?></td>
    </tr>
    <tr>
        <td class='searchfilter-name'>MIME Type</td>
        <td><?php echo $mt_html; ?></td>
    </tr>
    <tr>
        <td class='searchfilter-name'>MIME Subtype</td>
        <td><?php echo $mst_html; ?></td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Original name</td>
        <td><input type="text" id="<?php echo $fname_id?>" 
                name="<?php echo $fname_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $fname?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Extension</td>
        <td><input type="text" id="<?php echo $extension_id?>" 
                name="<?php echo $extension_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $extension?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Sizes</td>
        <td><input type="text" id="<?php echo $size_min_id?>" 
                name="<?php echo $size_min_id?>" 
                style="width:80px" value="<?php echo $size_min?>"/>
            --
            <input type="text" id="<?php echo $size_max_id?>" 
                name="<?php echo $size_max_id?>" 
                style="width:80px" value="<?php echo $size_max?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Text</td>
        <td><input type="text" id="<?php echo $text_id?>" 
                name="<?php echo $text_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $text?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Minimum Text Length</td>
        <td><input type="text" id="<?php echo $min_text_id?>" 
                name="<?php echo $min_text_id?>" maxlength="50" 
                style="width:50px" value="<?php echo $min_text?>"/>
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
        <td colspan='8'><?php echo $grid_title_html?></td>
    </tr>
    <tr class='hdrRow'>
        <td>Internal ID</td>
        <td>Public ID</td>
        <td>Custodian/Source</td>
        <td>MIME Type</td>
        <td align='right'>Size</td>
        <td>Name</td>
        <td>Extension</td>
        <td>&nbsp;</td>
    </tr>
    <?php echo $items_html; ?>
</table>

</form>
