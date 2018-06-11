<?php echo $form_html ?>

<p class="pagetitle">Redacted Collection Subsets</p>

<div class='message-confirm'><?php echo $message ?></div>

<p><a href='?page=edit_subset'>New Subset</a>
<p>

<table cellpadding='5' cellspacing='1' class='grid'>
    <tr class='hdrRow'>
        <td>Subset Name</td>
        <td>Database View</td>
        <td>Item Count</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
    </tr>
    <?php echo $subsets_html?>
</table>

</form>
