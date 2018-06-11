<?php echo $form_html ?>

<p class="pagetitle">Automated Redactions</p>

<table cellpadding="2" class="searchfilter-table">
    <tr>
        <td class='searchfilter-name'>Redaction Type</td>
        <td><?php echo $rule_html?></td>
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
        <td>Type</td>
        <td>Original Value</td>
        <td>Generated Value</td>
        <td>Item-Property Count</td>
        <td>&nbsp;</td>
    </tr>
    <?php echo $redactions_html?>
</table>

</form>
