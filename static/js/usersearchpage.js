
function click_view_restaurant(button){
        var id = button.id;
        var obj = document.getElementById(id+"_restaurant_name_city")
        var val = obj.value;
        window.location.replace(val);
    }

$(document).ready(function () {
//    alert('YO');

});
