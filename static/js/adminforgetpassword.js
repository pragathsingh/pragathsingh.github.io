$(document).ready(function () {

    var csrf_token = $("#token").val();

    $("#send").click(function () {
        var email = $("#email").val();
        $.ajax({
        dataType:"json",type:"POST",url:'adminforgetpasswordaction',async:true,
        data:
            {
                csrfmiddlewaretoken:csrf_token,
                email:email
            },
        success:function (json) {
            if(json.message)
            {
                alert(json.message);
            }
        }

        });

    });

});