import subprocess
import os

def passive_enumeration(target, output_folder=None):
    """
    Perform passive subdomain enumeration using subfinder, amass, and assetfinder.
    Returns a list of unique subdomains.
    """
    subs = set()
    
    # Use current directory if no output folder specified
    if output_folder is None:
        output_folder = '.'

    # Run subfinder
    try:
        subfinder_output = os.path.join(output_folder, 'subfinder.txt')
        subprocess.run(['subfinder', '-d', target, '-silent', '-o', subfinder_output], check=True, timeout=300)
        if os.path.exists(subfinder_output):
            with open(subfinder_output, 'r') as f:
                subs.update(line.strip() for line in f if line.strip())
    except subprocess.TimeoutExpired:
        print("[-] subfinder timed out")
    except subprocess.CalledProcessError as e:
        print(f"[-] subfinder failed: {e}")
    except FileNotFoundError:
        print("[-] subfinder not found")

    # Run amass passive
    try:
        amass_output = os.path.join(output_folder, 'amass_passive.txt')
        subprocess.run(['amass', 'enum', '-passive', '-d', target, '-o', amass_output], check=True, timeout=600)
        if os.path.exists(amass_output):
            with open(amass_output, 'r') as f:
                subs.update(line.strip() for line in f if line.strip())
    except subprocess.TimeoutExpired:
        print("[-] amass passive timed out")
    except subprocess.CalledProcessError as e:
        print(f"[-] amass passive failed: {e}")
    except FileNotFoundError:
        print("[-] amass not found")

    # Run assetfinder
    try:
        assetfinder_output = os.path.join(output_folder, 'assetfinder.txt')
        with open(assetfinder_output, 'w') as f:
            subprocess.run(['assetfinder', '--subs-only', target], stdout=f, check=True, timeout=300)
        if os.path.exists(assetfinder_output):
            with open(assetfinder_output, 'r') as f:
                subs.update(line.strip() for line in f if line.strip())
    except subprocess.TimeoutExpired:
        print("[-] assetfinder timed out")
    except subprocess.CalledProcessError as e:
        print(f"[-] assetfinder failed: {e}")
    except FileNotFoundError:
        print("[-] assetfinder not found")

    return list(subs)
