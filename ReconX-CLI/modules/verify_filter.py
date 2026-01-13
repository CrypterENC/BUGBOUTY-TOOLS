import subprocess
import re
import os
from colorama import Fore, Style

def verification_filtering(all_subs_raw, target, output_folder=None, wordlist=None):
    """
    Filter subdomains and verify live ones using httpx.
    Creates filtered_subs.txt, live_subs_detailed.txt, and live_subs.txt.
    Returns a list of live subdomains.
    """
    # Use current directory if no output folder specified
    if output_folder is None:
        output_folder = '.'
    
    # Remove wildcards and filter invalid domains
    pattern = rf'^[a-zA-Z0-9.-]+\.{re.escape(target)}$'
    filtered = [sub for sub in all_subs_raw if not sub.startswith('*') and re.match(pattern, sub)]

    # Create filtered_subs.txt
    filtered_file = os.path.join(output_folder, 'filtered_subs.txt')
    with open(filtered_file, 'w') as f:
        for sub in sorted(filtered):
            f.write(f'{sub}\n')

    # Run httpx on filtered_subs.txt
    live_subs = []
    try:
        detailed_file = os.path.join(output_folder, 'live_subs_detailed.txt')
        subprocess.run(['httpx', '-l', filtered_file, '-silent', '-title', '-status-code', '-tech-detect', '-content-length', '-o', detailed_file], check=True, timeout=600)
        
        # Extract live subdomains from live_subs_detailed.txt
        if os.path.exists(detailed_file):
            with open(detailed_file, 'r') as f:
                for line in f:
                    parts = line.split()
                    if parts:
                        url = parts[0]
                        url = url.replace('https://', '').replace('http://', '')
                        live_subs.append(url)
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} httpx timed out")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} httpx failed: {e}")
    except FileNotFoundError:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} httpx not found")

    # Create live_subs.txt with extracted live subdomains
    live_subs_file = os.path.join(output_folder, 'live_subs.txt')
    with open(live_subs_file, 'w') as f:
        for sub in sorted(live_subs):
            f.write(f'{sub}\n')

    # Run gowitness to capture screenshots
    try:
        print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Running GoWitness to capture screenshots...")
        subprocess.run(['gowitness', 'scan', 'file', '-f', live_subs_file, '--write-db'], check=True, timeout=1800)
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} GoWitness screenshots captured successfully")
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} gowitness timed out")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} gowitness failed: {e}")
    except FileNotFoundError:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} gowitness not found")

    return live_subs
