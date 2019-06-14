$(document).ready(function () {
    var csrf_token = $("#token").val();
    $("#remove-cart-items").click(function () {

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

    // $(".add-item").click(function (event) {
    //     alert('clicked');
    //     alert(event);
    // })


// $(document).on('click', '.add-item', function () {
//     // your function here
//     alert(this.id);
// });
//



    $("#add-to-cart").click(function () {

        if(itemsid_in_cart.length > 0)
        {
            var ids_str = ""
            var names_str = ""
            var qty_str = ""
            var amount_str = ""
            for(var i = 0;i<itemsid_in_cart.length;i++)
            {
                if(i < itemsid_in_cart.length - 1)
                {
                    ids_str += (itemsid_in_cart[i]+",")
                    names_str += (itemsname_in_cart[i]+",")
                    qty_str += (itemsqty_in_cart[i]+",")
                    amount_str += (itemsamount_in_cart[i]+",")
                }
                else
                {
                    ids_str += itemsid_in_cart[i]
                    names_str += itemsname_in_cart[i]
                    qty_str += itemsqty_in_cart[i]
                    amount_str += itemsamount_in_cart[i]
                }
            }

            $.ajax({
            type:"POST",dataType:"json",url:'/addtocart',async:true,
            data:
                {
                    csrfmiddlewaretoken:csrf_token,
                    ids:ids_str,
                    names:names_str,
                    qty:qty_str,
                    amounts:amount_str,

                },
            success:function (json) {

                alert(json.message);
            }
        });
        }

    });
});

var itemsid_in_cart = [];
var itemsname_in_cart = [];
var itemsqty_in_cart = [];
var itemsamount_in_cart = [];
var itemsprice_in_cart = [];
var itemsgst_in_cart = [];
var total_price = 0
var total_gst = 0
var total_amount = 0


function checkout(button) {
    var id = button.id;
    if(id == 'checkout')
    {
        window.location.replace('/checkout')
    }
}

function change_total_amount(){
    var array_len = itemsid_in_cart.length;
    var subtotal = 0;
    for(var i = 0;i<array_len;i++)
    {
        //subtotal += parseInt(document.getElementById(itemsid_in_cart[i]+'-item-net-amount').innerText);
        //subtotal += itemsamount_in_cart[i];
        subtotal += (itemsprice_in_cart[i] * itemsqty_in_cart[i]  + itemsgst_in_cart[i] * itemsqty_in_cart[i]);
    }
    document.getElementById('cart-net-amount').innerText = subtotal.toString();
    total_amount = subtotal;
}

function change_total_price() {
    var total = 0;
    var array_len = itemsid_in_cart.length;
    for(var i = 0; i< array_len; i++)
    {
        total += (itemsprice_in_cart[i] * itemsqty_in_cart[i]);
    }
    document.getElementById('cart-net-price').innerText = total.toString();
    total_price = total;
    //alert(total_price);
}
function calculate_gst() {
    var total = 0;
    var array_len = itemsid_in_cart.length;
    for(var i = 0; i< array_len; i++)
    {
        total += (itemsgst_in_cart[i] * itemsqty_in_cart[i]);
    }
    document.getElementById('cart-net-gst').innerText = total.toString();
    total_gst = total;
    // var st = (total_amount.toString() - total_price.toString());
    // alert(st);
}

function add(item_id) {
     function finding_index(element)
        { return element == item_id; }

        var index = itemsid_in_cart.findIndex(finding_index);

        var qty = itemsqty_in_cart[index];
        qty += 1;

        document.getElementById(item_id + '-item-qty').innerText = qty;
        var item_net_amount = parseInt(document.getElementById(item_id+'-item-amount').innerText);
        item_net_amount = item_net_amount * qty;
        document.getElementById(item_id+"-item-net-amount").innerText = item_net_amount;
        itemsqty_in_cart[index] = qty;
        itemsamount_in_cart[index] = item_net_amount;

        change_total_amount();
        change_total_price();
        calculate_gst();
}
function subtract(item_id) {
    function finding_index(element)
    { return element == item_id; }
    var index = itemsid_in_cart.findIndex(finding_index);

    qty -= 1;
    var item_net_amount = parseInt(document.getElementById(item_id+'-item-amount').innerText);
    item_net_amount = item_net_amount * qty;
    document.getElementById(item_id+"-item-net-amount").innerText = item_net_amount;
    itemsqty_in_cart[index] = qty;
    itemsamount_in_cart[index] = item_net_amount;

    change_total_amount();
    change_total_price();
    calculate_gst();
}

function add_cart_button(button) {
    var id = button.id;
    var index = id.search("-");
    var item_id = id.slice(0, index);

    add(item_id);
}
function subtract_cart_button(button) {
    var id = button.id;
    var index = id.search("-");
    var item_id = id.slice(0,index);

     function finding_index(element)
    { return element == item_id; }
    var index = itemsid_in_cart.findIndex(finding_index);
    var qty = itemsqty_in_cart[index];

    if(qty == 1)
    {
        subtract(item_id);
        var div_cart_item = document.getElementById(item_id+"-div-cart-item");
        div_cart_item.parentNode.removeChild(div_cart_item);
        itemsid_in_cart.splice(index,1);
        itemsamount_in_cart.splice(index,1);
        itemsqty_in_cart.splice(index,1);
        itemsgst_in_cart.splice(index,1);
        itemsprice_in_cart.splice(index,1);
        itemsname_in_cart.splice(index,1);

        if(itemsid_in_cart.length == 0)
        {
            document.getElementById('add-to-cart').style.display = "none";
            document.getElementById('remove-cart-items').style.display = "none";
            document.getElementById('checkout').style.display = "none";
        }
    }
    else {
            subtract(item_id);
    }
}

function add_item_tocart() {
    var childrens = document.getElementById('order-items-info').childNodes;
    alert();
}

function add_item(button) {

    document.getElementById('add-to-cart').style.display = "block";
    document.getElementById('remove-cart-items').style.display = "block";
    document.getElementById('checkout').style.display = "block";

    var id = (button.id).toString();
    var index = id.search("-");
    var item_id = (id.slice(0,index)).toString();

    //var item_qty_obj = document.getElementById(item_id+'-cart-value');

    //if item already exist then add it to its quantity
    var item_exists = false;
    for(var i = 0;i < itemsid_in_cart.length ; i++)
    {
        if(parseInt(item_id) == itemsid_in_cart[i])
        {
            item_exists = true;
            break;
        }
    }

    if(!item_exists)
    {
        var item_info = document.getElementById(item_id+"-item-info").value;
        var data = item_info.split(",");

        itemsid_in_cart.push(parseInt(item_id));
        itemsname_in_cart.push(data[1]);
        itemsqty_in_cart.push(1);
        itemsprice_in_cart.push(parseInt(data[3]));
        itemsgst_in_cart.push(parseInt(data[5]) - parseInt(data[3]));
        itemsamount_in_cart.push(parseInt(data[5]));


        var obj = document.getElementById("order-items-info");

        var full_div = "";
        full_div += "<div id='" + item_id + "-div-cart-item' class='cart-items'>" +
            "<input hidden='hidden' value='" + item_id + "' id='"+ item_id +"-cart-item'>";
        full_div += data[1]+"<br>";

        full_div += "<div class='cart-add-subtract'>" +
                    "<button onclick='add_cart_button(this)' id='"+ item_id +"-add-button'>+</button>" +
                    "<span style='margin: 3px;padding: 3px' id='"+ item_id +"-item-qty'>" + 1 + "</span>"+
                    "<button onclick='subtract_cart_button(this)' id='" + item_id + "-subtract-button'>-</button><br>" +
                    "<span>&#8377;<span id='" + item_id +"-item-amount'>" + data[3] + "</span></span>"
                    +"<span style='float: right'>&#8377;<span id='" + item_id
                    + "-item-net-amount'>" + data[3] +"</span>" +
                    "</div>";

        full_div +="</div>";
        obj.innerHTML += full_div;

        if(itemsid_in_cart.length == 1)
        {
           // document.getElementById('subtotal').innerText += subtotal_info;
            document.getElementById('total_values').style.display = "block";
        }
        change_total_amount();
        change_total_price();
        calculate_gst();

    }
    else
    {
        add(item_id);
    }

}
