var rating = "";
function markstar(star){
    var count = star.id[0];
    var subid = star.id.substring(1);
    rating = count;
    for(var i=1;i<=5;i++)
    {
        if(i<= count)
        {
            document.getElementById(i+subid).style.color = "orange";
        }
        else
        {
            document.getElementById(i+subid).style.color = "black";
        }

    }
}
function a_mouse_entered(event){
    var id = event.id;
    document.getElementById(id).style.background = "lightgrey";
}

function a_mouse_exit(event){
    var id = event.id;
    document.getElementById(id).style.background = "white";
}

$(document).ready(function () {
    var csrf_token = $("#token").val();
    var text_once_clicked = false;
    $("#write-review-text").click(function (event) {
        if(!text_once_clicked){
            text_once_clicked = true;
            document.getElementById("div-star").style.display = "block";
        }
    });

    $("#form-write-review").submit(function (event) {
        event.preventDefault();
        var review = $("#write-review-text").val();
        var restaurant_id = $("#restaurant_id").val();
        if(review && rating)
        {
            $.ajax({
            type:"POST",dataType:"json",url:"/addrestaurantreview",async:true,
            data:
                {
                    csrfmiddlewaretoken: csrf_token,
                    review:review,
                    rating:parseFloat(rating),
                    restaurant_id:restaurant_id
                },
            success:function (json) {
                if(json.message)
                {
                    alert(json.message);
                }
                if(json.rating)
                {
                    alert(json.rating);
                }
                if(json.review)
                {
                    alert(json.review);
                }

            }
            });
        }
        else
        {
            alert('Rating and Review both are necessary');
        }
    });


});