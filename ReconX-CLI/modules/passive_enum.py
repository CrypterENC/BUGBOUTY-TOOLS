import subprocess
import os

def passive_enumeration(target, output_folder=None):
    """
    Perform passive subdomain enumeration using subfinder and assetfinder.
    Combines results into passive_subs.txt and returns a list of unique subdomains.
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

    # Combine passive results into passive_subs.txt
    passive_subs_file = os.path.join(output_folder, 'passive_subs.txt')
    with open(passive_subs_file, 'w') as f:
        for sub in sorted(subs):
            f.write(f'{sub}\n')

    return list(subs)
