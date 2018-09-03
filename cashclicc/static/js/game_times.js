var timer;

function Stop() {
    clearTimeout(timer);
}

function GetGameTimes() {
    $('.box').each(function(i, obj) {
         var id = $(this).attr('id');
         var time_id = "time-".concat(id);
         var name_id = "name-".concat(id);
         var xmlhttp;
         if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp=new XMLHttpRequest();
         }
         else {// code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
         }
         xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState==4 && xmlhttp.status==200) {
                var response = xmlhttp.responseText;
            if (response == "quit" || response.substring(0, 4) == "None") {
                obj.style.display = "None";
            }
            else if (response.substring(0, 6) == "orange") {
                document.getElementById(time_id).style.color = "orange";
                var time = response.substring(7, 15);
                var user = response.substring(16, response.length);
                document.getElementById(time_id).innerHTML=time;
                document.getElementById(name_id).innerHTML=user;
            }
            else if (response.substring(0, 3) == "red") {
                document.getElementById(time_id).style.color = "red";
                var time = response.substring(4, 12);
                var user = response.substring(13, response.length);
                document.getElementById(time_id).innerHTML=time;
                document.getElementById(name_id).innerHTML=user;
            }
            else {
                var time = response.substring(0, 8);
                var user = response.substring(9, response.length);
                document.getElementById(time_id).innerHTML=time;
                document.getElementById(name_id).innerHTML=user;
            }
            }
         }
         var url = "/refresh_game/".concat(id);
         xmlhttp.open("GET", url, true);
         xmlhttp.send();
    });
    timer = setTimeout(GetGameTimes, 333);
}

$(function() {
    GetGameTimes();
});

/*
function GetServerTime() {
    var xmlhttp;
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            var response = xmlhttp.responseText;
            if (response == "quit") {
                document.getElementById("time").style.color = "red";
                document.getElementById("time").innerHTML="Game Over!";
                document.getElementById("game_button").className = "cashed-out";
                document.getElementById("game_button").value = "CASHED OUT";
                Stop();
            }
            else if (response.substring(0, 6) == "orange") {
                document.getElementById("time").style.color = "orange";
                var time = response.substring(7, 15);
                var user = response.substring(16, response.length);
                document.getElementById("time").innerHTML=time;
                document.getElementById("name").innerHTML=user;
            }
            else if (response.substring(0, 3) == "red") {
                document.getElementById("time").style.color = "red";
                var time = response.substring(4, 12);
                var user = response.substring(13, response.length);
                document.getElementById("time").innerHTML=time;
                document.getElementById("name").innerHTML=user;
            }
            else {
                var time = response.substring(0, 8);
                var user = response.substring(9, response.length);
                document.getElementById("time").innerHTML=time;
                document.getElementById("name").innerHTML=user;
            }
        }
    }
    var current_url = window.location.href;
    var id = current_url.substring(current_url.length - 2, current_url.length);
    var url = "/refresh_game/".concat(id);
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    timer = setTimeout(GetServerTime, 500);
}*/