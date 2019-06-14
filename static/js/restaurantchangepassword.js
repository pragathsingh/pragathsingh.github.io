$(document).ready(function () {

    var csrf_token = $("#token").val();

    $("#change").click(function () {
        var oldpassword = $("#oldpassword").val();
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
                dataType: "json", type: "POST", url: '/restaurantchangepasswordaction', async: true,
                data:
                    {
                        csrfmiddlewaretoken: csrf_token,
                        oldpassword:oldpassword,
                        password: password,
                        cpassword: cpassword,
                    },
                success: function (json) {
                    if (!json.message) {
                        document.getElementById('error-old-password').innerHTML = "* old-password is incorrect";
                    }
                    else
                        {
                        alert('Password was changed');
                        window.location.replace('/')
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