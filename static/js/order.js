$(document).ready(function () {

    $("#payment").click(function () {
            document.getElementById('paymentmode').value = $('#payment').val();
        });

    $("#pay").click(function (event) {

        var formdata = new FormData();
        formdata.append('paymentmode',document.getElementById('paymentmode').value);

        var amounts = $("#amounts").val();
        var amounts_arr = amounts.split(',');
        var subtotal = 0
        for (var i = 0; i < amounts_arr.length; i++) {
            subtotal += parseInt(amounts_arr[i]);
        }
        document.getElementById('subtotal').innerHTML = subtotal;
        alert(document.getElementById('paymentmode').value);
        if (document.getElementById('paymentmode').value == "online") {
            var amount = subtotal * 100;
            var options = {
                    "key": "rzp_test_dRWiKHS7zr2Gki",
                    "amount": amount,
                    "name": "Eatigo Food Ordering Website",
                    "description": "Online Payment System",
                    "image": "http://ecourses.aec.edu.in/aditya/images/po4.png",
                    "handler": function (response) {


                        if (response.razorpay_payment_id == "") {

                            var xml = new XMLHttpRequest();
                            xml.onreadystatechange = function () {
                                if (this.readyState == 4 && this.status == 200) {
                                    var ar = JSON.parse(this.response);
                                    document.getElementById("neworderids").value = ar['order_ids'];
                                    $("#order-details-form").submit();
                                }
                            };
                            xml.open('POST', '/orderplace', true);
                            xml.send(formdata);

                        }
                        else {
                            //alert('Success');
                            var xml = new XMLHttpRequest();
                            xml.onreadystatechange = function () {
                                if (this.readyState == 4 && this.status == 200) {
                                    var ar = JSON.parse(this.response);
                                    document.getElementById("neworderids").value = ar['order_ids'];
                                    $("#order-details-form").submit();
                                }
                            };
                            xml.open('POST', '/orderplace', true);
                            xml.send(formdata);
                        }
                    },
                    "prefill": {

                        "email":
                            "{{ request.session.CUSTEMAIL }}"
                    },
                    "notes":
                        {
                            "address":
                                ""
                        }
                    ,
                    "theme":
                        {
                            "color":
                                "#F37254"
                        }
                }
            ;
            var rzp1 = new Razorpay(options);
            rzp1.open();
        }
        else{
            var xml = new XMLHttpRequest();
            xml.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    var ar = JSON.parse(this.response);
                    document.getElementById("neworderids").value = ar['order_ids'];
                    $("#order-details-form").submit();
                }
            };
            xml.open('POST', '/orderplace', true);
            xml.send(formdata);
        }

        // var paymentmode = $("#paymentmode").val();
        // alert(paymentmode);
        // $.ajax({
        //     type: "POST", dataType: "json", url: 'orderplace', async: true,
        //     data:
        //         {
        //             csrfmiddlewaretoken: csrf_token,
        //             paymentmode: paymentmode,
        //         },
        //     success: function (json) {
        //         if (json.message) {
        //             if (json.order_ids) {
        //                 document.getElementById("neworderids").value = json.order_ids;
        //                 $("#order-details-form").submit();
        //             }
        //             else {
        //                 alert(json.message);
        //             }
        //         }
        //     }
        // });
    });

    var csrf_token = $("#token").val();
    $(".remove-item").click(function () {

        var id = $(this).attr('id');
        var index = id.search("-");
        var item_id = id.slice(0, index);
        var item_qty_obj = document.getElementById(item_id + '-item-id');
        var item_amount_obj = document.getElementById(item_id + '-item-amount');
        var amount = item_amount_obj.value;
        var subtotal = parseInt(document.getElementById('subtotal').innerText) - parseInt(amount);
        document.getElementById('subtotal').innerText = subtotal;
        $(item_qty_obj).remove();


        $.ajax({
            type: "POST", dataType: "json", url: '/removeitemfromcart', async: true,
            data:
                {
                    csrfmiddlewaretoken: csrf_token,
                },
            success: function (json) {
                if (json.message) {
                    alert(json.message);
                }
            }
        });


    });
});