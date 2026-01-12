import subprocess
import json
import os
from urllib.parse import urlparse

def active_enumeration(target, output_folder=None):
    """
    Perform active subdomain enumeration using knockpy and ffuf.
    Returns a list of unique subdomains.
    """
    subs = set()
    
    # Use current directory if no output folder specified
    if output_folder is None:
        output_folder = '.'

    # Run knockpy
    try:
        knockpy_output = os.path.join(output_folder, 'knockpy_results.json')
        subprocess.run(['knockpy', target, '-o', knockpy_output], check=True, timeout=300)
        if os.path.exists(knockpy_output):
            with open(knockpy_output, 'r') as f:
                data = json.load(f)
            subs.update(data.get('subdomains', []))
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        print("[-] knockpy failed or not found")

    # Run ffuf for subdomain brute via HTTP
    try:
        wordlist = '/usr/share/wordlists/assetnote/best-dns-wordlist.txt'
        if not os.path.exists(wordlist):
            wordlist = 'wordlist.txt'
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
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        print("[-] ffuf failed or not found")

    return list(subs)
