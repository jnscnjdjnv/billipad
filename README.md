# Bilipad Ref - Auto Insiders

This Python script automates the process of creating accounts on Billipad.finance, completing tasks, and setting up withdrawal addresses.

## Features

- Creates multiple accounts concurrently
- Uses proxies for requests (optional)
- Generates random emails and passwords
- Creates Ethereum wallets for each account
- Completes all required tasks
- Sets withdrawal addresses
- Saves account information to a JSON file
- Retries failed account creations
- Detailed logging
- Reads referral code from external file

## Requirements

- Python 3.7+
- Required packages (install using `pip install -r requirements.txt`):
  - requests
  - eth-account
  - web3
  - colorama

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `proxies.txt` file with your proxies (one per line) in the format:
   ```
   username:password@host:port
   ```
   or
   ```
   host:port
   ```
4. Edit the `referral_code.txt` file and add your referral code:
   ```
   YOUR_REFERRAL_CODE_HERE
   ```
   Replace `YOUR_REFERRAL_CODE_HERE` with your actual referral code.

## Usage

### Using the Manager Script (Recommended)

For easier management of proxies, referral codes, and account creation, use the manager script:

```
python bilipad_manager.py
```

This will display a menu with the following options:
- Add Proxy: Add a new proxy to proxies.txt
- Delete All Proxies: Clear all proxies from proxies.txt
- Add Referral Code: Set a new referral code in referral_code.txt
- Delete Referral Code: Clear the referral code from referral_code.txt
- Start Account Creation: Begin the account creation process

### Manual Usage

1. Run the script:
   ```
   python bilipad_ref_auto_insiders.py
   ```
2. Enter the number of accounts to create when prompted
3. The script will create accounts, complete tasks, and save the information to `accounts.json`

## Running on Termux

To run this script on Termux (Android), follow these steps:

1. Install Termux from F-Droid or Google Play Store
2. Open Termux and run the following commands:

```
pkg update && pkg upgrade -y
pkg install git python -y
cd ~
git clone https://github.com/jnscnjdjnv/billipad.git
cd billipad
pip install -r requirements.txt
python bilipad_manager.py
```

## Output

- Account information is saved to `accounts.json`
- Logs are saved to `bilipad_insiders.log`
- Console output shows progress and results

## Notes

- The script uses asyncio for concurrent account creation
- Failed accounts are retried up to 3 times
- Each account creation includes a random delay to avoid detection
- You can change the referral code by editing the `referral_code.txt` file without modifying the main script

## Contact & Support

- Telegram: [@savanop121](https://t.me/savanop121)
- GitHub Repository: [billipad](https://github.com/jnscnjdjnv/billipad.git) 