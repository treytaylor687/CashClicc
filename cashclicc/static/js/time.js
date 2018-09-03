var timer;

function Stop() {
    clearTimeout(timer);
}

function nthIndex(str, pat, n){
    var L= str.length, i= -1;
    while(n-- && i++<L){
        i= str.indexOf(pat, i);
        if (i < 0) break;
    }
    return i;
}

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
            if (response == "quit" || response.substring(0, 4) == "None") {
                document.getElementById("time").style.color = "#808080";
                document.getElementById("cash").style.color = "#808080";
                document.getElementById("time").innerHTML="ENDED";
                document.getElementById("name").style.color = "#58b968";
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
    var split_url = current_url.split("");
    var reverse_url = split_url.reverse();
    var firstPar;
    var join_url = reverse_url.join("");
    var index_of_gameid;
    if (reverse_url[0] == "/") {
        index_of_gameid = current_url.length - nthIndex(join_url, "/", 2);
    }
    else {
        index_of_gameid = current_url.length - nthIndex(join_url, "/", 1);
    }
    var id = current_url.substring(index_of_gameid, current_url.length);
    var url = "/refresh_game/".concat(id);
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    timer = setTimeout(GetServerTime, 333);
}

$(function() {
    GetServerTime();
});