import requests
import os
from colorama import Fore, Style

def certificate_transparency(target, output_folder=None, wordlist=None):
    """
    Perform certificate transparency enumeration using crt.sh.
    Creates crt_subs.txt and returns a list of unique subdomains.
    """
    subs = set()
    
    # Use current directory if no output folder specified
    if output_folder is None:
        output_folder = '.'
    
    try:
        url = f"https://crt.sh/?q=%25.{target}&output=json"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                name = item.get('name_value', '')
                name = name.replace('*.', '')
                if name and '.' in name:
                    subs.add(name)
        else:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} crt.sh request failed with status {response.status_code}")
    except requests.RequestException as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Error fetching from crt.sh: {e}")
    
    # Create crt_subs.txt
    crt_subs_file = os.path.join(output_folder, 'crt_subs.txt')
    with open(crt_subs_file, 'w') as f:
        for sub in sorted(subs):
            f.write(f'{sub}\n')
    
    return list(subs)
