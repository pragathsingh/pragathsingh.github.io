$(document).ready(function ()
    {
        var csrf_token = $("#token").val();
        $("#search-button").click(function () {
            var search = $("#search").val();
            if(search != '')
            { window.location.replace('adminsearch?search='+search); }

        });

        $("#logout").click(function (event) {
            event.preventDefault();
                $.ajax({
                type: "POST", dataType: "json", url: '/adminlogoutaction', async: true,
                data:
                {
                    csrfmiddlewaretoken: csrf_token
                },
                success: function (json) {
                    if(json.message)
                    {
                        window.location.replace('/');
                    }
                  }
                });
        });
    });

function HomePageOnLoad() {
        var name_lower = document.getElementById('username').value;
        var name_upper = name_lower.charAt(0).toUpperCase() + name_lower.substr(1);
        document.getElementById("welcome").innerText += name_upper;
        var obj = document.getElementById("user-name")
        if(obj)
        {
            obj.innerText += name_upper;
        }

        var photo_path = document.getElementById('photo').value;
        //document.getElementById('user_photo').src = "/static/" + photo_path;
        document.getElementById("welcome").style.background = name_upper;
    }


