<?php echo $form_html ?>

<p class="pagetitle">Search Email Items</p>

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
        <td class='searchfilter-name'>From</td>
        <td><input type="text" id="<?php echo $from_id?>" 
                name="<?php echo $from_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $from?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>To</td>
        <td><input type="text" id="<?php echo $to_id?>" 
                name="<?php echo $to_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $to?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>CC</td>
        <td><input type="text" id="<?php echo $cc_id?>" 
                name="<?php echo $cc_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $cc?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>BCC</td>
        <td><input type="text" id="<?php echo $bcc_id?>" 
                name="<?php echo $bcc_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $bcc?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Dates</td>
        <td><input type="text" id="<?php echo $date_start_id?>" 
                name="<?php echo $date_start_id?>" maxlength="50" 
                style="width:80px" value="<?php echo $date_start?>"/>
            --
            <input type="text" id="<?php echo $date_end_id?>" 
                name="<?php echo $date_end_id?>" maxlength="50" 
                style="width:80px" value="<?php echo $date_end?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Subject</td>
        <td><input type="text" id="<?php echo $subject_id?>" 
                name="<?php echo $subject_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $subject?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Header</td>
        <td><input type="text" id="<?php echo $emailheader_id?>" 
                name="<?php echo $emailheader_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $emailheader?>"/>
        </td>
    </tr>
    <tr>
        <td class='searchfilter-name'>Body</td>
        <td><input type="text" id="<?php echo $body_id?>" 
                name="<?php echo $body_id?>" maxlength="50" 
                style="width:300px" value="<?php echo $body?>"/>
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
        <td>From</td>
        <td>To</td>
        <td>Date</td>
        <td>Subject</td>
        <td>&nbsp;</td>
    </tr>
    <?php echo $items_html; ?>
</table>

</form>
