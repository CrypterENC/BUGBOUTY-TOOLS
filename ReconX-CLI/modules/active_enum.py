import subprocess
import json
import os
from urllib.parse import urlparse
from colorama import Fore, Style

def active_enumeration(target, output_folder=None, wordlist=None):
    """
    Perform active subdomain enumeration using ffuf.
    Combines results into active_subs.txt and returns a list of unique subdomains.
    """
    subs = set()
    
    # Use current directory if no output folder specified
    if output_folder is None:
        output_folder = '.'

    # Run ffuf for subdomain brute via HTTP
    try:
        if wordlist is None:
            wordlist = '/usr/share/wordlists/assetnote/best-dns-wordlist.txt'
        
        if not os.path.exists(wordlist):
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Wordlist not found: {wordlist}")
            return list(subs)
        
        ffuf_output = os.path.join(output_folder, 'ffuf_subs.json')
        subprocess.run(['ffuf', '-u', f'https://FUZZ.{target}', '-w', wordlist, '-t', '100', '-mc', '200,301,302,403', '-o', ffuf_output], check=True, timeout=600)
        if os.path.exists(ffuf_output):
            with open(ffuf_output, 'r') as f:
                data = json.load(f)
            for result in data.get('results', []):
                url = result['url']
                parsed = urlparse(url)
                domain = parsed.netloc
                if domain.endswith(f'.{target}'):
                    sub_part = domain[:-len(f'.{target}')]
                    subs.add(f'{sub_part}.{target}')
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} ffuf timed out")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} ffuf failed: {e}")
    except FileNotFoundError:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} ffuf not found")

    # Combine active results into active_subs.txt
    active_subs_file = os.path.join(output_folder, 'active_subs.txt')
    with open(active_subs_file, 'w') as f:
        for sub in sorted(subs):
            f.write(f'{sub}\n')

    return list(subs)
