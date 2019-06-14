$(document).ready(function () {



    $("#price").bind('input',function () {
        if($("#price").val() && $("#gst").val() )
        {
            var price = parseFloat($("#price").val());
            var gst = parseFloat($("#gst").val());
            var mrp = parseInt(price*(gst/100));
            document.getElementById("mrp").value = mrp;
            //alert(mrp);
        }
    });

    $("#gst").bind('input',function () {
        if($("#price").val() && $("#gst").val() )
        {
            var price = parseFloat($("#price").val());
            var gst = parseFloat($("#gst").val());
            var mrp = parseInt(price + price*(gst/100));
            document.getElementById("mrp").value = mrp;
            //alert(mrp);
        }
    });

    $("#mrp").bind('input',function () {
        if($("#mrp").val() && $("#gst").val() )
        {
            var mrp = parseFloat($("#mrp").val());
            var gst = parseFloat($("#gst").val());
            var price = parseInt(mrp * (100/(gst+100)));
            document.getElementById("price").value = price;
            //alert(mrp);
        }
    });

    $("#update").click(function () {
        var price = parseFloat($("#price").val());
        var gst = parseFloat($("#gst").val());
        var mrp = parseInt(price + price*(gst/100));
    });


});