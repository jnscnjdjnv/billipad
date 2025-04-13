#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the program banner"""
    banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════╗
███████  █████  ██    ██  █████  ███    ██ 
██      ██   ██ ██    ██ ██   ██ ████   ██ 
███████ ███████ ██    ██ ███████ ██ ██  ██ 
     ██ ██   ██  ██  ██  ██   ██ ██  ██ ██ 
███████ ██   ██   ████   ██   ██ ██   ████ 
║                                                                                ║
║  Telegram: @savanop121                                                        ║
║  GitHub: https://github.com/jnscnjdjnv/billipad.git                           ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def add_proxy():
    """Add a proxy to proxies.txt"""
    clear_screen()
    print_banner()
    print(f"{Fore.YELLOW}[*] Adding Proxy{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Enter proxy in format: username:password@host:port or host:port{Style.RESET_ALL}")
    proxy = input(f"{Fore.GREEN}Proxy: {Style.RESET_ALL}")
    
    if not proxy:
        print(f"{Fore.RED}[!] Proxy cannot be empty{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    try:
        with open("proxies.txt", "a") as f:
            f.write(proxy + "\n")
        print(f"{Fore.GREEN}[+] Proxy added successfully{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error adding proxy: {str(e)}{Style.RESET_ALL}")
    
    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def delete_proxies():
    """Delete all proxies from proxies.txt"""
    clear_screen()
    print_banner()
    print(f"{Fore.YELLOW}[*] Deleting All Proxies{Style.RESET_ALL}")
    
    confirm = input(f"{Fore.RED}Are you sure you want to delete all proxies? (y/n): {Style.RESET_ALL}")
    
    if confirm.lower() == 'y':
        try:
            with open("proxies.txt", "w") as f:
                f.write("")
            print(f"{Fore.GREEN}[+] All proxies deleted successfully{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error deleting proxies: {str(e)}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[*] Operation cancelled{Style.RESET_ALL}")
    
    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def add_referral_code():
    """Add a referral code to referral_code.txt"""
    clear_screen()
    print_banner()
    print(f"{Fore.YELLOW}[*] Adding Referral Code{Style.RESET_ALL}")
    
    referral_code = input(f"{Fore.GREEN}Enter referral code: {Style.RESET_ALL}")
    
    if not referral_code:
        print(f"{Fore.RED}[!] Referral code cannot be empty{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    try:
        with open("referral_code.txt", "w") as f:
            f.write(referral_code)
        print(f"{Fore.GREEN}[+] Referral code added successfully{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error adding referral code: {str(e)}{Style.RESET_ALL}")
    
    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def delete_referral_code():
    """Delete referral code from referral_code.txt"""
    clear_screen()
    print_banner()
    print(f"{Fore.YELLOW}[*] Deleting Referral Code{Style.RESET_ALL}")
    
    confirm = input(f"{Fore.RED}Are you sure you want to delete the referral code? (y/n): {Style.RESET_ALL}")
    
    if confirm.lower() == 'y':
        try:
            with open("referral_code.txt", "w") as f:
                f.write("")
            print(f"{Fore.GREEN}[+] Referral code deleted successfully{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error deleting referral code: {str(e)}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[*] Operation cancelled{Style.RESET_ALL}")
    
    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def start_account_creation():
    """Start the account creation process"""
    clear_screen()
    print_banner()
    print(f"{Fore.YELLOW}[*] Starting Account Creation{Style.RESET_ALL}")
    
    # Check if referral code exists
    try:
        with open("referral_code.txt", "r") as f:
            referral_code = f.read().strip()
            if not referral_code:
                print(f"{Fore.RED}[!] No referral code found. Please add a referral code first.{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                return
    except FileNotFoundError:
        print(f"{Fore.RED}[!] referral_code.txt not found. Please add a referral code first.{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    # Check if proxies exist
    try:
        with open("proxies.txt", "r") as f:
            proxies = f.readlines()
            if not proxies:
                print(f"{Fore.YELLOW}[!] No proxies found. The script will run without proxies.{Style.RESET_ALL}")
                confirm = input(f"{Fore.YELLOW}Do you want to continue without proxies? (y/n): {Style.RESET_ALL}")
                if confirm.lower() != 'y':
                    print(f"{Fore.YELLOW}[*] Operation cancelled{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                    return
    except FileNotFoundError:
        print(f"{Fore.YELLOW}[!] proxies.txt not found. The script will run without proxies.{Style.RESET_ALL}")
        confirm = input(f"{Fore.YELLOW}Do you want to continue without proxies? (y/n): {Style.RESET_ALL}")
        if confirm.lower() != 'y':
            print(f"{Fore.YELLOW}[*] Operation cancelled{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
    
    # Get number of accounts to create
    try:
        num_accounts = int(input(f"{Fore.GREEN}Enter number of accounts to create: {Style.RESET_ALL}"))
        if num_accounts <= 0:
            print(f"{Fore.RED}[!] Number of accounts must be greater than 0{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
    except ValueError:
        print(f"{Fore.RED}[!] Invalid input. Please enter a number.{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    # Run the main script
    print(f"{Fore.GREEN}[+] Starting account creation for {num_accounts} accounts...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Press Ctrl+C to stop the process{Style.RESET_ALL}")
    
    try:
        # Create a temporary file with the number of accounts
        with open("num_accounts.txt", "w") as f:
            f.write(str(num_accounts))
        
        # Run the main script
        subprocess.run([sys.executable, "bilipad_ref_auto_insiders.py"])
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}[*] Process interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error running script: {str(e)}{Style.RESET_ALL}")
    finally:
        # Clean up temporary file
        if os.path.exists("num_accounts.txt"):
            os.remove("num_accounts.txt")
        
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def main_menu():
    """Display the main menu"""
    while True:
        clear_screen()
        print_banner()
        
        print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                                {Fore.YELLOW}MAIN MENU{Fore.CYAN}                                  ║")
        print(f"╠════════════════════════════════════════════════════════════════════════════╣")
        print(f"║  {Fore.GREEN}[1]{Fore.CYAN} Add Proxy                                                                                ║")
        print(f"║  {Fore.GREEN}[2]{Fore.CYAN} Delete All Proxies                                                                      ║")
        print(f"║  {Fore.GREEN}[3]{Fore.CYAN} Add Referral Code                                                                       ║")
        print(f"║  {Fore.GREEN}[4]{Fore.CYAN} Delete Referral Code                                                                    ║")
        print(f"║  {Fore.GREEN}[5]{Fore.CYAN} Start Account Creation                                                                  ║")
        print(f"║  {Fore.GREEN}[0]{Fore.CYAN} Exit                                                                                    ║")
        print(f"╚════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        choice = input(f"{Fore.GREEN}Enter your choice: {Style.RESET_ALL}")
        
        if choice == '1':
            add_proxy()
        elif choice == '2':
            delete_proxies()
        elif choice == '3':
            add_referral_code()
        elif choice == '4':
            delete_referral_code()
        elif choice == '5':
            start_account_creation()
        elif choice == '0':
            clear_screen()
            print(f"{Fore.GREEN}[+] Thank you for using Bilipad Manager{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}[!] Invalid choice. Please try again.{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print(f"{Fore.GREEN}[+] Thank you for using Bilipad Manager{Style.RESET_ALL}")
        sys.exit(0) 