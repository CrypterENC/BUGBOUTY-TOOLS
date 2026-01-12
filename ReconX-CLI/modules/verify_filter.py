import subprocess
import re

def verification_filtering(all_subs_raw, target):
    """
    Filter subdomains and verify live ones using httpx.
    Returns a list of live subdomains.
    """
    # Filter invalid domains
    pattern = rf'^[a-zA-Z0-9.-]+\.{re.escape(target)}$'
    filtered = [sub for sub in all_subs_raw if not sub.startswith('*') and re.match(pattern, sub)]

    # Write filtered to file
    with open('filtered_subs.txt', 'w') as f:
        for sub in filtered:
            f.write(f'{sub}\n')

    # Run httpx
    live_subs = []
    try:
        subprocess.run(['httpx', '-l', 'filtered_subs.txt', '-silent', '-title', '-status-code', '-tech-detect', '-content-length', '-o', 'live_subs_detailed.txt'], check=True, timeout=300)
        # Read the detailed output
        with open('live_subs_detailed.txt', 'r') as f:
            for line in f:
                parts = line.split()
                if parts:
                    url = parts[0].replace('https://', '').replace('http://', '')
                    live_subs.append(url)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        print("[-] httpx failed, using filtered as fallback")
        live_subs = filtered

    return live_subs
