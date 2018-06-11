function formSubmit()
{
    document.getElementById("form1").submit();
}

function pagerSubmit(offset)
{
    document.getElementById("hidOffset").value = offset;
    document.getElementById("form1").submit();
}
