$(document).ready(function () {

    var csrf_token = $("#token").val();

    $("#change").click(function () {
        var password = $("#password").val();
        var cpassword = $("#cpassword").val();
        if(password.length == 0)
        {
            document.getElementById('error-password').innerHTML = "* password is empty";
            return;
        }
        if(cpassword.length == 0)
        {
            document.getElementById('error-cpassword').innerHTML = "* confirm-password is empty";
            return;
        }
        if(password == cpassword) {
            $.ajax({
                dataType: "json", type: "POST", url: '/', async: true,
                data:
                    {
                        csrfmiddlewaretoken: csrf_token,
                        password: password,
                        cpassword: cpassword,
                    },
                success: function (json) {
                    if (json.message) {
                        alert(json.message);
                    }
                }
            });
        }
        else
        {
            //alert("password and confirm-password should be same");
            document.getElementById('error-cpassword').innerHTML = "* confirm-password not same";
        }

    });

});