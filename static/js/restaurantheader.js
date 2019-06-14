function fetchorders(){

    var csrf_token = $("#token").val();
    var length = $("#length").val();
    var order_ids = $("#order_ids").val();
 $.ajax({
  url: 'checkorders',
  type: 'post',data:{csrfmiddlewaretoken:csrf_token,length:length,order_ids:order_ids},
  success: function(json){
   // Perform operation on return value
      if(json.message)
      {
          //alert(json.message);
            alert('There was an order');
            if(json.new_orders)
            { alert(json.new_orders); }
            if(json.all_ids)
            {document.getElementById('order_ids').value = json.all_ids;}

      }
  },
 });
}

$(document).ready(function ()
    {
        // alert(document.getElementById('logout'));
        alert('ready');
        var interval = setInterval(fetchorders,5000);

        var csrf_token = $("#token").val();
        $("#search-button").click(function () {
            var search = $("#search").val();
            if(search != '')
            { window.location.replace('usersearch?search='+search); }

        });

        $("#logout").click(function (event) {
            event.preventDefault();
                $.ajax({
                type: "POST", da1taType: "json", url: '/restaurantlogout', async: true,
                data:
                {
                    csrfmiddlewaretoken: csrf_token
                },
                success: function (json) {
                    if(json.message)
                    {
                        clearInterval(interval);
                        window.location.replace('/');
                    }
                  }
                });
        });
    });
