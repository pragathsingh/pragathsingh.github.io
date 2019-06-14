function fetchordersstatus(){

    var csrf_token = $("#token").val();
    var order_ids = $("#order_id").val();
 $.ajax({
  url: 'usercheckorderstatus',
  type: 'post',data:{csrfmiddlewaretoken:csrf_token,order_ids:order_ids},
  success: function(json){

      if(json.message)
      {
          var all_stats = json.all_stats;
      }
      if(json.message == 0)
      {
          alert('No order id found')
      }

  },
 });
}

$(document).ready(function () {

    var interval = setInterval(fetchordersstatus,5000);
});
