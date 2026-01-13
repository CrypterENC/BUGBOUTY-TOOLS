#!/usr/bin/env python3
import argparse
import sys
import os
import subprocess
import venv
import platform
import concurrent.futures
import shutil

from utils.installer import ensure_tools_installed
from modules.passive_enum import passive_enumeration
from modules.active_enum import active_enumeration
from modules.cert_trans import certificate_transparency
from modules.verify_filter import verification_filtering

def check_venv_active():
    """Check if running inside a virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def get_venv_path():
    """Get the path to the venv directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'venv')

def create_and_activate_venv():
    """Create venv and install dependencies"""
    venv_path = get_venv_path()
    
    if check_venv_active():
        print("[+] Already running in a virtual environment")
        return True
    
    print("[*] Creating Python virtual environment...")
    
    try:
        venv.create(venv_path, with_pip=True)
        print(f"[+] Virtual environment created at {venv_path}")
    except Exception as e:
        print(f"[-] Failed to create virtual environment: {e}")
        return False
    
    pip_executable = get_pip_executable(venv_path)
    
    print("[*] Installing Python dependencies from requirements.txt...")
    try:
        result = subprocess.run(
            [pip_executable, 'install', '-r', 'requirements.txt'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            print(f"[-] Failed to install dependencies: {result.stderr}")
            return False
        print("[+] Python dependencies installed successfully")
    except subprocess.TimeoutExpired:
        print("[-] Dependency installation timed out")
        return False
    except Exception as e:
        print(f"[-] Error installing dependencies: {e}")
        return False
    
    print("\n[*] Activating virtual environment...")
    relaunch_in_venv(venv_path)
    return True

def get_pip_executable(venv_path):
    """Get the pip executable path for the venv"""
    if platform.system() == "Windows":
        return os.path.join(venv_path, 'Scripts', 'pip.exe')
    else:
        return os.path.join(venv_path, 'bin', 'pip')

def get_python_executable(venv_path):
    """Get the python executable path for the venv"""
    if platform.system() == "Windows":
        return os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        return os.path.join(venv_path, 'bin', 'python')

def relaunch_in_venv(venv_path):
    """Relaunch the script inside the virtual environment"""
    python_executable = get_python_executable(venv_path)
    script_path = os.path.abspath(__file__)
    
    print(f"[+] Relaunching script in virtual environment...\n")
    
    try:
        os.execv(python_executable, [python_executable, script_path] + sys.argv[1:])
    except Exception as e:
        print(f"[-] Failed to relaunch in venv: {e}")
        sys.exit(1)

def create_target_folder(target):
    """Create a folder for the target domain"""
    target_folder = target.replace('.', '_')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    return target_folder

def save_phase_results(folder, phase_name, subdomains):
    """Save phase results to a text file"""
    filename = os.path.join(folder, f"{phase_name}.txt")
    with open(filename, 'w') as f:
        for sub in sorted(subdomains):
            f.write(f"{sub}\n")
    return filename

def get_wordlist_from_user(phase_name):
    """Prompt user for wordlist path"""
    print(f"\n[?] Enter wordlist path for {phase_name} phase:")
    print("[*] Leave empty to use default or skip this phase")
    wordlist_path = input(">>> ").strip()
    
    if not wordlist_path:
        return None
    
    if not os.path.exists(wordlist_path):
        print(f"[-] Wordlist not found: {wordlist_path}")
        retry = input("[?] Try another path? (y/n): ").strip().lower()
        if retry == 'y':
            return get_wordlist_from_user(phase_name)
        return None
    
    print(f"[+] Using wordlist: {wordlist_path}")
    return wordlist_path

def cleanup_intermediate_files(folder):
    """Remove intermediate phase files after final results are created"""
    intermediate_files = [
        'passive_enum.txt',
        'active_enum.txt',
        'cert_trans.txt',
        'filtered_subs.txt',
        'live_subs_detailed.txt',
        'subfinder.txt',
        'amass_passive.txt',
        'assetfinder.txt',
        'ffuf_subs.json'
    ]
    
    for filename in intermediate_files:
        filepath = os.path.join(folder, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"[*] Cleaned up: {filename}")
            except Exception as e:
                print(f"[-] Failed to remove {filename}: {e}")

def main():
    if not check_venv_active():
        print("\n" + "="*60)
        print("ReconX-CLI: Automated Subdomain Enumeration Tool")
        print("="*60 + "\n")
        if not create_and_activate_venv():
            print("[-] Failed to setup virtual environment")
            sys.exit(1)
    
    parser = argparse.ArgumentParser(
        description='ReconX-CLI: Automated Subdomain Enumeration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python reconx_cli.py example.com
  python reconx_cli.py target.org
        """
    )
    parser.add_argument('TARGET', help='Target domain for subdomain enumeration')
    args = parser.parse_args()

    target = args.TARGET

    print(f"\n[*] Checking and installing required tools...\n")
    ensure_tools_installed()

    # Create target-specific folder
    target_folder = create_target_folder(target)
    print(f"\n[+] Created results folder: {target_folder}\n")

    print(f"\n[+] Starting subdomain enumeration for {target}\n")
    
    # Prompt for wordlists
    print("\n" + "="*60)
    print("Wordlist Configuration")
    print("="*60)
    active_wordlist = get_wordlist_from_user("Active Enumeration (FFUF)")
    cert_wordlist = get_wordlist_from_user("Certificate Transparency")

    # Run phases in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        passive_future = executor.submit(passive_enumeration, target, target_folder)
        active_future = executor.submit(active_enumeration, target, target_folder, active_wordlist)
        cert_future = executor.submit(certificate_transparency, target, target_folder, cert_wordlist)

        passive_subs = passive_future.result()
        active_subs = active_future.result()
        cert_subs = cert_future.result()

    print(f"[+] Passive enumeration completed: {len(passive_subs)} subdomains")
    save_phase_results(target_folder, 'passive_enum', passive_subs)
    
    print(f"[+] Active enumeration completed: {len(active_subs)} subdomains")
    save_phase_results(target_folder, 'active_enum', active_subs)
    
    print(f"[+] Certificate transparency completed: {len(cert_subs)} subdomains")
    save_phase_results(target_folder, 'cert_trans', cert_subs)

    # Combine raw subdomains
    all_subs_raw = set(passive_subs + active_subs + cert_subs)
    print(f"[+] Total raw subdomains: {len(all_subs_raw)}")

    # Phase 4: Verification & Filtering
    live_subs = verification_filtering(list(all_subs_raw), target, target_folder)
    print(f"[+] Live subdomains verified: {len(live_subs)}")

    # Output final results
    output_file = os.path.join(target_folder, 'live_subs.txt')
    with open(output_file, 'w') as f:
        for sub in sorted(live_subs):
            f.write(f"{sub}\n")

    print(f"\n[+] Results saved to {output_file}\n")

    # Cleanup intermediate files
    print(f"[*] Cleaning up intermediate files...\n")
    cleanup_intermediate_files(target_folder)

    print(f"[+] Enumeration completed successfully!\n")

if __name__ == "__main__":
    main()
