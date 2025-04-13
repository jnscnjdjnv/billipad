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

1. Run the script:
   ```
   python bilipad_ref_auto_insiders.py
   ```
2. Enter the number of accounts to create when prompted
3. The script will create accounts, complete tasks, and save the information to `accounts.json`

## Output

- Account information is saved to `accounts.json`
- Logs are saved to `bilipad_insiders.log`
- Console output shows progress and results

## Notes

- The script uses asyncio for concurrent account creation
- Failed accounts are retried up to 3 times
- Each account creation includes a random delay to avoid detection
- You can change the referral code by editing the `referral_code.txt` file without modifying the main script 