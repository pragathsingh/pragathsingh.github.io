function place_order() {
   window.location.replace('checkout');
}

function remove_all_items(){

}

$(document).ready(function () {

    var csrf_token = $("#token").val();
    var amounts = $("#amounts").val();
    var amounts_arr = amounts.split(',');
    var subtotal = 0
    for(var i=0;i<amounts_arr.length;i++)
    {
        subtotal += parseInt(amounts_arr[i]);
    }
    document.getElementById('subtotal').value = subtotal;


    $(".remove-item").click(function () {

        var id = $(this).attr('id');
        var index = id.search("-");
        var item_id = id.slice(0,index);
        var amount = document.getElementById(item_id+"-item-amount").value;
        var subtotal = $("#subtotal").val();
        subtotal -= amount;
        document.getElementById("subtotal").value = subtotal;
        var item_qty_obj = document.getElementById(item_id+'-item-id');

        $(item_qty_obj).remove();

         $.ajax({
            type:"POST",dataType:"json",url:'/removeitemfromcart',async:true,
            data:
                {
                    csrfmiddlewaretoken:csrf_token,
                },
            success:function (json) {
                if(json.message)
                {
                    alert(json.message);
                }
            }
        });
    });

     $("#remove-all-items").click(function () {

        var objs = document.getElementById('all-cart-items');
        $(objs).remove();
        document.getElementById('main_div').innerHTML += "<h3>There are no items in your cart.</h3>"
         $.ajax({
            type:"POST",dataType:"json",url:'/removecartitems',async:true,
            data:
                {
                    csrfmiddlewaretoken:csrf_token,
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