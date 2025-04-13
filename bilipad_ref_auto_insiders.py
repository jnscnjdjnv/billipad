import os
import json
import uuid
import random
import time
import requests
import asyncio
import re
import sys
from eth_account import Account
from web3 import Web3
from urllib.parse import urlparse
import logging

# Configure logging with UTF-8 encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bilipad_insiders.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Constants
BASE_URL = 'https://billipad.finance/api'
REFERRAL_CODE_FILE = 'referral_code.txt'
ACCOUNTS_FILE = 'accounts.json'
EMAIL_DOMAIN = 'ptct.net'
PROXIES_FILE = 'proxies.txt'
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30  # Increased timeout
TASK_RETRY_COUNT = 3  # Number of retries for each task
TASK_RETRY_DELAY = 5  # Seconds to wait between task retries
DISABLE_SSL_WARNINGS = True  # Disable SSL warnings

# Global variables
accounts = []
proxies = []
referral_code = ''

# Disable SSL warnings
if DISABLE_SSL_WARNINGS:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_referral_code():
    """Load referral code from file"""
    global referral_code
    try:
        if not os.path.exists(REFERRAL_CODE_FILE):
            logging.warning(f"[!] {REFERRAL_CODE_FILE} not found, using empty referral code")
            referral_code = ''
            return
        
        with open(REFERRAL_CODE_FILE, 'r') as f:
            referral_code = f.read().strip()
        
        if not referral_code:
            logging.warning("[!] Referral code is empty")
        else:
            logging.info(f"[+] Loaded referral code: {referral_code}")
    except Exception as e:
        logging.error(f"[-] Error loading referral code: {str(e)}")
        referral_code = ''

def get_referral_link():
    """Get the referral link with the loaded code"""
    return f'https://Billipad.finance/ref/{referral_code}'

def load_proxies():
    """Load proxies from file"""
    try:
        if not os.path.exists(PROXIES_FILE):
            logging.error(f"[-] {PROXIES_FILE} not found")
            return []
        
        # Read the file content and log it for debugging
        with open(PROXIES_FILE, 'r', encoding='utf-8') as f:
            file_content = f.read()
            logging.info(f"[*] Raw file content: {repr(file_content)}")
            
            # Split by newlines and filter empty lines
            proxy_lines = [line.strip() for line in file_content.split('\n') if line.strip()]
            logging.info(f"[*] Found {len(proxy_lines)} non-empty lines in {PROXIES_FILE}")
            
            # Log each line for debugging
            for i, line in enumerate(proxy_lines):
                logging.info(f"[*] Line {i+1}: {repr(line)}")
        
        if not proxy_lines:
            logging.warning(f"[!] No proxies found in {PROXIES_FILE}")
            return []
        
        valid_proxies = []
        for line in proxy_lines:
            try:
                proxy = line.strip()
                logging.info(f"[*] Processing proxy line: {proxy}")
                
                # Handle different proxy formats
                if '@' in proxy:
                    # Format: username:password@host:port
                    auth, host_port = proxy.split('@')
                    if ':' in auth:
                        username, password = auth.split(':')
                    else:
                        username, password = auth, ''
                    
                    if ':' in host_port:
                        host, port = host_port.split(':')
                    else:
                        host, port = host_port, ''
                    
                    proxy_url = f"http://{username}:{password}@{host}:{port}"
                    logging.info(f"[+] Parsed proxy: {host}:{port} with auth")
                else:
                    # Format: host:port
                    if ':' in proxy:
                        host, port = proxy.split(':')
                    else:
                        host, port = proxy, ''
                    
                    proxy_url = f"http://{host}:{port}"
                    logging.info(f"[+] Parsed proxy: {host}:{port} without auth")
                
                if not host or not port:
                    logging.warning(f"[!] Invalid proxy format: {line}")
                    continue
                
                valid_proxies.append(proxy_url)
                logging.info(f"[+] Added proxy: {proxy_url}")
            except Exception as e:
                logging.warning(f"[!] Error parsing proxy line '{line}': {str(e)}")
        
        logging.info(f"[+] Successfully loaded {len(valid_proxies)} proxies")
        return valid_proxies
    except Exception as e:
        logging.error(f"[-] Error loading proxies: {str(e)}")
        import traceback
        logging.error(f"[-] Traceback: {traceback.format_exc()}")
        return []

def get_random_proxy():
    """Get a random proxy from the list"""
    if not proxies:
        logging.warning("[!] No valid proxies available, proceeding without proxy")
        return None
    
    proxy = random.choice(proxies)
    logging.info(f"[*] Using proxy: {proxy}")
    return proxy

def create_random_email():
    """Create a random email and credentials"""
    username = f"user{random.randint(1000000, 9999999)}"
    email = f"{username}@{EMAIL_DOMAIN}"
    password = f"Pass{random.randint(100000, 999999)}"
    
    logging.info(f"[+] Created email: {email}")
    
    return {
        "username": username,
        "email": email,
        "password": password,
        "deviceId": str(uuid.uuid4())
    }

def generate_wallet():
    """Generate a new Ethereum wallet"""
    account = Account.create()
    return {
        "address": account.address,
        "privateKey": account.key.hex()
    }

def create_headers(auth_token=None, referer='signup'):
    """Create headers for API requests"""
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.5",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Brave\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "Referer": f"https://billipad.finance/{referer}",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    
    if auth_token:
        headers["cookie"] = f"authToken={auth_token}"
    
    return headers

def make_request(method, url, data=None, headers=None, proxy=None, timeout=REQUEST_TIMEOUT, retry_count=3):
    """Make HTTP request with proxy support and retry logic"""
    for attempt in range(retry_count):
        try:
            proxies = None
            if proxy:
                proxies = {
                    'http': proxy,
                    'https': proxy
                }
                logging.info(f"[*] Making request with proxy: {proxy}")
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout, verify=False)
            else:
                response = requests.post(url, json=data, headers=headers, proxies=proxies, timeout=timeout, verify=False)
            
            # Check for 402 Payment Required error
            if response.status_code == 402:
                logging.error(f"[-] Payment Required error: {response.text}")
                # Try to extract more information from the response
                try:
                    error_data = response.json()
                    logging.error(f"[-] Error details: {error_data}")
                except:
                    pass
                raise Exception(f"Payment Required: {response.text}")
            
            response.raise_for_status()
            return response.json(), response.headers
        except requests.exceptions.RequestException as e:
            if attempt < retry_count - 1:
                wait_time = (attempt + 1) * 2
                logging.warning(f"Request failed (attempt {attempt+1}/{retry_count}): {str(e)}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logging.error(f"Request error after {retry_count} attempts: {str(e)}")
                raise

def register_user(credentials, proxy):
    """Register a new user"""
    try:
        username = credentials["username"]
        email = credentials["email"]
        password = credentials["password"]
        device_id = credentials["deviceId"]
        
        headers = create_headers(None, f'signup?ref={referral_code}')
        
        # Add additional headers that might help
        headers.update({
            "Origin": "https://billipad.finance",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        })
        
        data = {
            "username": username,
            "email": email,
            "password": password,
            "deviceId": device_id,
            "referralLink": get_referral_link()
        }
        
        # Try to get the signup page first to get any necessary cookies
        try:
            signup_url = f"https://billipad.finance/signup?ref={referral_code}"
            requests.get(signup_url, headers=headers, proxies={'http': proxy, 'https': proxy} if proxy else None, verify=False, timeout=REQUEST_TIMEOUT)
            logging.info("[+] Visited signup page to get cookies")
        except Exception as e:
            logging.warning(f"[!] Failed to visit signup page: {str(e)}")
        
        # Wait a bit before making the actual request
        time.sleep(2)
        
        response, _ = make_request('POST', f"{BASE_URL}/signup", data, headers, proxy)
        
        logging.info(f"[+] Successfully registered: {email}")
        return response
    except Exception as e:
        logging.error(f"[-] Registration failed for {credentials['email']}: {str(e)}")
        raise

def login_user(credentials, proxy):
    """Login a user"""
    try:
        email = credentials["email"]
        password = credentials["password"]
        device_id = credentials["deviceId"]
        
        headers = create_headers(None, 'login')
        
        # Add additional headers that might help
        headers.update({
            "Origin": "https://billipad.finance",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        })
        
        data = {
            "email": email,
            "password": password,
            "deviceId": device_id
        }
        
        # Try to get the login page first to get any necessary cookies
        try:
            login_url = "https://billipad.finance/login"
            requests.get(login_url, headers=headers, proxies={'http': proxy, 'https': proxy} if proxy else None, verify=False, timeout=REQUEST_TIMEOUT)
            logging.info("[+] Visited login page to get cookies")
        except Exception as e:
            logging.warning(f"[!] Failed to visit login page: {str(e)}")
        
        # Wait a bit before making the actual request
        time.sleep(2)
        
        response, response_headers = make_request('POST', f"{BASE_URL}/login", data, headers, proxy)
        
        logging.info(f"Login data: userId={response.get('user', {}).get('id', 'none')}, hasToken={bool(response.get('token'))}")
        logging.info(f"Cookies: {'Present' if 'set-cookie' in response_headers else 'None'}")
        
        if not response.get('user') or not response['user'].get('id'):
            raise Exception('No valid user data received')
        
        auth_token = response.get('token')
        
        if not auth_token:
            set_cookie = response_headers.get('set-cookie')
            if set_cookie:
                cookie_string = set_cookie if isinstance(set_cookie, str) else '; '.join(set_cookie)
                token_match = re.search(r'authToken=([^;]+)', cookie_string)
                if token_match and token_match.group(1):
                    auth_token = token_match.group(1)
                    logging.info('[+] Token from cookie')
        
        if not auth_token:
            logging.warning('[!] No token found')
        
        logging.info(f"[+] Logged in: {email}")
        if auth_token:
            logging.info(f"[+] Token: {auth_token[:20]}...")
        
        return {
            "token": auth_token,
            "user": response['user']
        }
    except Exception as e:
        logging.error(f"[-] Login failed for {credentials['email']}: {str(e)}")
        raise

def check_auth(auth_token, proxy):
    """Check authentication status"""
    try:
        headers = create_headers(auth_token, 'dashboard')
        
        response, _ = make_request('GET', f"{BASE_URL}/auth-check", headers=headers, proxy=proxy)
        
        logging.info('[+] Auth check OK')
        return response
    except Exception as e:
        logging.error(f"[-] Auth check failed: {str(e)}")
        raise

def complete_task(user_id, auth_token, task_index, proxy):
    """Complete a task for a user with retry logic"""
    for attempt in range(TASK_RETRY_COUNT):
        try:
            headers = create_headers(auth_token, 'dashboard')
            
            data = {
                "action": "updateTask",
                "value": 10,
                "taskIndex": task_index,
                "clicks": 2
            }
            
            response, _ = make_request('POST', f"{BASE_URL}/referral?userId={user_id}", data, headers, proxy)
            
            logging.info(f"[+] Task {task_index + 1} done for user: {user_id}")
            return response
        except Exception as e:
            if attempt < TASK_RETRY_COUNT - 1:
                wait_time = TASK_RETRY_DELAY * (attempt + 1)
                logging.warning(f"[-] Task {task_index + 1} failed (attempt {attempt+1}/{TASK_RETRY_COUNT}): {str(e)}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logging.error(f"[-] Task {task_index + 1} failed after {TASK_RETRY_COUNT} attempts: {str(e)}")
                raise

def submit_withdrawal_address(user_id, wallet_address, auth_token, proxy):
    """Submit withdrawal address for a user"""
    try:
        headers = create_headers(auth_token, 'dashboard')
        
        data = {
            "userId": user_id,
            "walletAddress": wallet_address
        }
        
        response, _ = make_request('POST', f"{BASE_URL}/withdraw", data, headers, proxy)
        
        logging.info(f"[+] Withdrawal address set for user: {user_id}")
        return response
    except Exception as e:
        logging.error(f"[-] Withdrawal address failed: {str(e)}")
        raise

def save_accounts():
    """Save accounts to file"""
    try:
        # Create the file if it doesn't exist
        if not os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'w') as f:
                json.dump([], f)
            logging.info(f"[+] Created new {ACCOUNTS_FILE} file")
        
        # Save the accounts
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump(accounts, f, indent=2)
        logging.info(f"[+] Saved {len(accounts)} accounts to {ACCOUNTS_FILE}")
    except Exception as e:
        logging.error(f"[-] Failed to save accounts: {str(e)}")

def create_account():
    """Create a new account with all tasks"""
    try:
        proxy = get_random_proxy()
        
        credentials = create_random_email()
        logging.info(f"[*] Creating account: {credentials['email']}")
        
        register_user(credentials, proxy)
        
        logging.info('Waiting 2s...')
        time.sleep(2)
        
        login_result = login_user(credentials, proxy)
        auth_token = login_result["token"]
        user_id = login_result["user"]["id"]
        
        logging.info(f"[*] User ID: {user_id}")
        
        logging.info('Waiting 2s...')
        time.sleep(2)
        
        if auth_token:
            check_auth(auth_token, proxy)
        else:
            logging.warning('[!] No token, skipping auth check')
        
        # Try to complete tasks with better error handling
        tasks_completed = 0
        for task_index in range(7):
            try:
                complete_task(user_id, auth_token or '', task_index, proxy)
                tasks_completed += 1
                time.sleep(1 + random.random())
            except Exception as e:
                logging.error(f"[-] Failed to complete task {task_index + 1}: {str(e)}")
                # Continue with next task even if this one failed
        
        if tasks_completed < 7:
            logging.warning(f"[!] Only completed {tasks_completed}/7 tasks")
        
        wallet = generate_wallet()
        logging.info(f"[*] Wallet: {wallet['address']}")
        
        try:
            submit_withdrawal_address(user_id, wallet["address"], auth_token or '', proxy)
        except Exception as e:
            logging.error(f"[-] Failed to submit withdrawal address: {str(e)}")
            # Continue anyway, we still want to save the account
        
        account_data = {
            "username": credentials["username"],
            "email": credentials["email"],
            "password": credentials["password"],
            "userId": user_id,
            "deviceId": credentials["deviceId"],
            "authToken": auth_token,
            "wallet": wallet,
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "proxy": proxy,
            "tasksCompleted": tasks_completed
        }
        
        accounts.append(account_data)
        # Save accounts after each successful account creation
        save_accounts()
        
        logging.info(f"[+] Account created: {credentials['email']}")
        return account_data
    except Exception as e:
        logging.error(f"[-] Account creation failed: {str(e)}")
        return None

def process_accounts(count):
    """Process multiple accounts sequentially"""
    logging.info(f"Starting {count} accounts...")
    
    successful = 0
    failed = 0
    
    for i in range(count):
        logging.info(f"\n[*] Account {i + 1}/{count}")
        
        try:
            result = create_account()
            if result:
                successful += 1
                logging.info(f"[+] Account {i + 1} done")
            else:
                failed += 1
                logging.info(f"[-] Account {i + 1} failed")
            
            if i < count - 1:
                logging.info("Waiting 5s...")
                time.sleep(5)
        except Exception as e:
            logging.error(f"[-] Account {i + 1} error: {str(e)}")
            failed += 1
    
    logging.info(f"\n[+] Done: {successful} OK, {failed} failed")
    logging.info(f"[*] Saved to {ACCOUNTS_FILE}")
    
    return {"successful": successful, "failed": failed}

def retry_create_accounts(count, max_retries=MAX_RETRIES):
    """Retry account creation with backoff"""
    remaining_count = count
    retry_count = 0
    
    while remaining_count > 0 and retry_count < max_retries:
        result = process_accounts(remaining_count)
        remaining_count -= result["successful"]
        
        if remaining_count > 0:
            retry_count += 1
            logging.info(f"\n[!] {remaining_count} accounts left. Retry {retry_count}/{max_retries}")
            
            if retry_count < max_retries:
                delay = 10000 + random.randint(0, 5000)
                logging.info(f"Waiting {delay}ms...")
                time.sleep(delay / 1000)
    
    if remaining_count > 0:
        logging.info(f"\n[-] Failed to create all accounts after {max_retries} retries")
        logging.info(f"Created {count - remaining_count}/{count}")
    else:
        logging.info(f"\n[+] All {count} accounts created")

def main():
    """Main function"""
    global proxies, accounts
    
    # Load referral code
    load_referral_code()
    
    # Load proxies
    proxies = load_proxies()
    if not proxies:
        logging.warning("[!] No proxies loaded. The script will run without proxies.")
        user_input = input("Do you want to continue without proxies? (y/n): ")
        if user_input.lower() != 'y':
            logging.info("[*] Exiting script as requested.")
            return
    else:
        logging.info(f"[+] Successfully loaded {len(proxies)} proxies")
        for i, proxy in enumerate(proxies):
            logging.info(f"[+] Proxy {i+1}: {proxy}")
    
    # Load existing accounts if file exists
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, 'r') as f:
                accounts = json.load(f)
            logging.info(f"[+] Loaded {len(accounts)} existing accounts from {ACCOUNTS_FILE}")
        except Exception as e:
            logging.error(f"[-] Error loading existing accounts: {str(e)}")
            accounts = []
    else:
        # Create empty accounts file if it doesn't exist
        try:
            with open(ACCOUNTS_FILE, 'w') as f:
                json.dump([], f)
            logging.info(f"[+] Created new {ACCOUNTS_FILE} file")
        except Exception as e:
            logging.error(f"[-] Error creating accounts file: {str(e)}")
    
    print('------------------------------')
    print('Bilipad Ref - Auto Insiders')
    print('------------------------------')
    
    # Check if the website is accessible
    try:
        proxy = get_random_proxy() if proxies else None
        proxies_dict = {'http': proxy, 'https': proxy} if proxy else None
        
        logging.info(f"[*] Testing website accessibility with proxy: {proxy}")
        response = requests.get("https://billipad.finance", proxies=proxies_dict, verify=False, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            logging.warning(f"[!] Website returned status code {response.status_code}")
            user_input = input("The website might be down or changed. Do you want to continue anyway? (y/n): ")
            if user_input.lower() != 'y':
                logging.info("[*] Exiting script as requested.")
                return
        else:
            logging.info("[+] Website is accessible")
    except Exception as e:
        logging.warning(f"[!] Could not access the website: {str(e)}")
        user_input = input("The website might be down or changed. Do you want to continue anyway? (y/n): ")
        if user_input.lower() != 'y':
            logging.info("[*] Exiting script as requested.")
            return
    
    count = input('How many accounts to create? ')
    try:
        count = int(count.strip())
        if count <= 0:
            print('Enter a positive number')
            return
    except ValueError:
        print('Enter a valid number')
        return
    
    retry_create_accounts(count)

if __name__ == "__main__":
    main() 