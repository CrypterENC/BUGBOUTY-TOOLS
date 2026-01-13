import subprocess
import re
import os

def verification_filtering(all_subs_raw, target, output_folder=None, wordlist=None):
    """
    Filter subdomains and verify live ones using httpx.
    Returns a list of live subdomains.
    """
    # Use current directory if no output folder specified
    if output_folder is None:
        output_folder = '.'
    
    # Filter invalid domains
    pattern = rf'^[a-zA-Z0-9.-]+\.{re.escape(target)}$'
    filtered = [sub for sub in all_subs_raw if not sub.startswith('*') and re.match(pattern, sub)]

    # Write filtered to file
    filtered_file = os.path.join(output_folder, 'filtered_subs.txt')
    with open(filtered_file, 'w') as f:
        for sub in filtered:
            f.write(f'{sub}\n')

    # Run httpx
    live_subs = []
    try:
        detailed_file = os.path.join(output_folder, 'live_subs_detailed.txt')
        subprocess.run(['httpx', '-l', filtered_file, '-silent', '-title', '-status-code', '-tech-detect', '-content-length', '-o', detailed_file], check=True, timeout=300)
        # Read the detailed output
        with open(detailed_file, 'r') as f:
            for line in f:
                parts = line.split()
                if parts:
                    url = parts[0].replace('https://', '').replace('http://', '')
                    live_subs.append(url)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        print("[-] httpx failed, using filtered as fallback")
        live_subs = filtered

    return live_subs
