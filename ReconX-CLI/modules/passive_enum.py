import subprocess
import os

def passive_enumeration(target):
    """
    Perform passive subdomain enumeration using subfinder, amass, and assetfinder.
    Returns a list of unique subdomains.
    """
    subs = set()

    # Run subfinder
    try:
        subprocess.run(['subfinder', '-d', target, '-silent', '-o', 'subfinder.txt'], check=True)
        if os.path.exists('subfinder.txt'):
            with open('subfinder.txt', 'r') as f:
                subs.update(line.strip() for line in f if line.strip())
    except subprocess.CalledProcessError:
        print("[-] subfinder failed")

    # Run amass passive
    try:
        subprocess.run(['amass', 'enum', '-passive', '-d', target, '-o', 'amass_passive.txt'], check=True)
        if os.path.exists('amass_passive.txt'):
            with open('amass_passive.txt', 'r') as f:
                subs.update(line.strip() for line in f if line.strip())
    except subprocess.CalledProcessError:
        print("[-] amass passive failed")

    # Run assetfinder
    try:
        with open('assetfinder.txt', 'w') as f:
            subprocess.run(['assetfinder', '--subs-only', target], stdout=f, check=True)
        if os.path.exists('assetfinder.txt'):
            with open('assetfinder.txt', 'r') as f:
                subs.update(line.strip() for line in f if line.strip())
    except subprocess.CalledProcessError:
        print("[-] assetfinder failed")

    return list(subs)
