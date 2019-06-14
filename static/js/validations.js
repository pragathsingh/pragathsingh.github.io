$(document).ready(function() {

    var formsubmit = false;
    var csrf_token = $('#token').val();
    //alert('Jquery Loaded....');0
    var validurl = $("#validation_url").val();
    alert(validurl);
    //
    nameonce = false;
    passonce = false;
    emailonce = false;
    mobileonce = false;
    confirmpasswordonce = false;

    $("#username").bind('change ', function () {usernameonce();});
    $("#username").bind('input', function () {usernamevalidation();});
    $("#password").bind('change', function () {passoncechange();});
    $("#password").bind('input', function () {passwordvalidation();});
    $("#email").bind('change', function () {emailoncechange();});
    $("#email").bind('input', function () {emailvalidation();});
    $("#mobile").bind('change', function () {mobileoncechange();});
    $("#mobile").bind('input', function () {mobilevalidation();});
    $("#confirmpassword").bind('change', function () {confirmoassoncechange();});
    $("#confirmpassword").bind('input', function () {confirmoassvalidation();});

    function usernameonce() {
        nameonce = true;
        usernamevalidation();
    }

    function emailoncechange() {
        emailonce = true;
        emailvalidation()
    }

    function passoncechange() {
        passonce = true;
        passwordvalidation();
    }

    function passwordvalidation() {
        if(passonce)
        {
            var password = $("#password").val();
            validation('password',password);
        }
    }
    function emailvalidation() {
        if(emailonce)
        {
            var email = $("#email").val();
            validation('email',email);
        }
    }
     function usernamevalidation() {
        if(nameonce)
        {
            var username = $("#username").val();
            validation('username',username);
        }
    }

    function mobileoncechange() {
        mobileonce = true;
        mobilevalidation();
    }

    function mobilevalidation() {
        if (mobileonce) {
            var mobile = $("#mobile").val();
            validation('mobile', mobile);
        }
    }
    function confirmoassoncechange() {
        confirmpasswordonce = true;
        mobilevalidation();
    }

    function confirmoassvalidation() {
        if(confirmpasswordonce)
        {
            var password = $("#password").val();
            var confirmpassword = $("#confirmpassword").val();
            validation('confirmpassword',password+","+confirmpassword);
        }
}

    function validation(key, value) {

         $.ajax({
        type: "POST", dataType: "json", url: validurl, async: true,
        data:
        {
            csrfmiddlewaretoken: csrf_token,
            value: value,
            key: key,
            submit:false
        },
        success: function (json) {

            if(key == 'password')
            { var valuereturned = json.password;}
            if(key == 'email')
            { var valuereturned = json.email;}
            if(key == 'username')
            { var valuereturned = json.username;}
            if(key == 'mobile')
            { var valuereturned = json.mobile;}


            document.getElementById('error-'+key).innerHTML = valuereturned;
          }
        });

    }
    
    $("form").submit(function (event) {
        if(!formsubmit)
        {
            event.preventDefault();
            alert('Submit Stoped');
        }

        var username = $("#username").val();
        var email = $("#email").val();
        var password = $("#password").val();
        var mobile = $("#mobile").val();
        var address = $("#address").val();
        $.ajax({
            type:"POST",dataType: "json",url:validurl,async: true,
            data:
                {
                    csrfmiddlewaretoken: csrf_token,
                    username:username,
                    email:email ,
                    password:password,
                    mobile:mobile,
                    address:address,
                    submit:true
                },
            success:function (json) {

                document.getElementById('error-username').innerHTML = json.username;
                document.getElementById('error-password').innerHTML = json.password;
                document.getElementById('error-email').innerHTML = json.email;
                document.getElementById('error-mobile').innerHTML = json.mobile;
                document.getElementById('error-address').innerHTML = json.address;
                var data = json.data;
                if( data == 'true')
                {
                    formsubmit = true;
                }
            }
        })
    });
    
});
