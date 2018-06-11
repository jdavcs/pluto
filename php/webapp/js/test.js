function mark(id)
{
    var area = document.getElementById(id);
    var color = area.style.backgroundColor;
    
    if (color == "white")
        area.style.backgroundColor = "green";
    else if (color == "green")
        area.style.backgroundColor = "maroon";
    else
        area.style.backgroundColor = "white";
}

function mark_all(rows, cols)
{
    for (var i=0; i<cols; i++)
        mark_cells(i, rows, 0);
    for (var i=0; i<rows; i++)
        mark_cells(i, cols, 1);
}

function mark_cells(x_index, y_count, is_row) //for rows: row index, # of columns, 1; for cols: col index, # of rows, 0.
{
    //determine if we need to reset column colors
    var color_prev = "";
    var color_reset = 0;
    
    for (var i=0; i<y_count; i++)        
    {
        if (is_row)
            var id = "r" + x_index + "c" + i;
        else
            var id = "r" + i + "c" + x_index;


        var area = document.getElementById(id);
        var color_next = area.style.backgroundColor;

        if (color_prev == "")
            color_prev = color_next;

        if (color_prev != color_next)
            color_reset = 1;            
    }

    for (var i=0; i<y_count; i++)
    {
        if (is_row)
            var id = "r" + x_index + "c" + i;
        else
            var id = "r" + i + "c" + x_index;
    
        if (color_reset)
        {
            var area = document.getElementById(id);
            var color_next = area.style.backgroundColor;
            area.style.backgroundColor = "white";
        }
        else
            mark(id);
    }
}

function open_window_image(source_id, filename, type)
{
    var url = "viewimage.php?s=" + source_id + "&fn=" + filename + "&t=" + type;
    window.open(url, "image", "location=0, menubar=0, status=0, titlebar=0, toolbar=0, left=200, width=640, height=480");
}
