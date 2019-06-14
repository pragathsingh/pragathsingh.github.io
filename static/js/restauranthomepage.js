$(document).ready(function () {

    var csrf_token = $("#token").val();

    $(".accept").click(function (event) {
        var id = event.target.id;
        var id_list = id.split('-');
        var status_id = id_list[0];
        $.ajax({
            type:"POST",dataType:"json",url:'/changeorderstatus',async:true,
            data:
                {csrfmiddlewaretoken:csrf_token,order_id:status_id},
            success:function (json) {
                if(json.message)
                {
                    document.getElementById(id).style.display = "none";
                    alert(status_id+"-delivery");
                    document.getElementById(id+"-delivery").style.display = "block";
                }
            }
        });
    });

    $(".deliver").click(function (event) {
        var id = event.target.id;
        var id_list = id.split('-');
        var status_id = id_list[0];
        $.ajax({
            type:"POST",dataType:"json",url:'/changedeliverystatus',async:true,
            data:
                {csrfmiddlewaretoken:csrf_token,order_id:status_id},
            success:function (json) {
                if(json.message)
                {
                    document.getElementById(id).style.display = "none";
                }
            }
        });
    });
});