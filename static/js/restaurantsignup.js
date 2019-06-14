$(document).ready(function () {

    $("#addrestaurant").click(function () {

    var csrf_token = $("#token").val();
    var restauratname = $("#restaurantname").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var mobileno = $("#mobileno").val();
    var address = $("#address").val();
    var city = $("#city").val();
    var ownername = $("#ownername").val();
    var status = $("#status").val();
    var photo = $("#photo").val();
    alert(restauratname+email+password+mobileno+address+city+ownername+status+photo);
   $.ajax({
       type:"POST",dataType:"json",async:true,url:'/restaurantsignupaction',
       data:
           {
               csrfmiddlewaretoken:csrf_token,
               restaurantname:restauratname,
               email:email,
               password:password,
               address:address,
               city:city,
               mobileno:mobileno,
               ownsername:ownername,
               status:status,
               photo:photo,
           }
       ,
       success:function (json) {
           if(json.valid)
           {
               alert(json.message);
               window.location.replace('/');
           }
           else
           {
               alert(json.message);
           }
       }
        });

    });

});