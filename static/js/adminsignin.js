$(document).ready(function () {


    $("form").submit(function (event) {
        event.preventDefault();

        var csrf_token = $("#token").val();
        var email = $("#signincredentials").val();
        var pwd = $("#pwd").val();
        //alert(pwd);
    $.ajax({
        url: '/adminsigninaction',
        type: 'post',
        data:
            {
                csrfmiddlewaretoken:csrf_token,
                signincredentials:email,
                pwd:pwd,
            },
        success: function(json){
        // Perform operation on return value
        if(json.valid)
        {
            //$("form").submit();
             window.location.replace('/');
        }
        else
        {
            if(json.error_email)
            {
                document.getElementById('error').innerText = "";
                document.getElementById('error-email').innerText = json.error_email;
            }
            if(json.error_pwd)
            {
                document.getElementById('error').innerText = "";
                document.getElementById('error-pwd').innerText = json.error_pwd;
            }
            if(json.message)
            {
                document.getElementById('error-email').innerText = "";
                document.getElementById('error-pwd').innerText = "";
                document.getElementById('error').innerText = json.message;
            }
        }
      },
 });

    })


});
