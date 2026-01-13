#!/usr/bin/env python3
import argparse
import sys
import os
import subprocess
import venv
import platform
import concurrent.futures
import shutil
from colorama import Fore, Back, Style, init

init(autoreset=True)

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
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Already running in a virtual environment")
        return True
    
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Creating Python virtual environment...")
    
    try:
        venv.create(venv_path, with_pip=True)
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Virtual environment created at {venv_path}")
    except Exception as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to create virtual environment: {e}")
        return False
    
    pip_executable = get_pip_executable(venv_path)
    
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Installing Python dependencies from requirements.txt...")
    try:
        result = subprocess.run(
            [pip_executable, 'install', '-r', 'requirements.txt'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to install dependencies: {result.stderr}")
            return False
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Python dependencies installed successfully")
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Dependency installation timed out")
        return False
    except Exception as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Error installing dependencies: {e}")
        return False
    
    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Activating virtual environment...")
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
    
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Relaunching script in virtual environment...\n")
    
    try:
        os.execv(python_executable, [python_executable, script_path] + sys.argv[1:])
    except Exception as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to relaunch in venv: {e}")
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
    print(f"\n{Fore.YELLOW}[?]{Style.RESET_ALL} Enter wordlist path for {phase_name} phase:")
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Leave empty to use default or skip this phase")
    wordlist_path = input(f"{Fore.YELLOW}>>>{Style.RESET_ALL} ").strip()
    
    if not wordlist_path:
        return None
    
    if not os.path.exists(wordlist_path):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Wordlist not found: {wordlist_path}")
        retry = input(f"{Fore.YELLOW}[?]{Style.RESET_ALL} Try another path? (y/n): ").strip().lower()
        if retry == 'y':
            return get_wordlist_from_user(phase_name)
        return None
    
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Using wordlist: {wordlist_path}")
    return wordlist_path

def cleanup_intermediate_files(folder):
    """Remove intermediate phase files after final results are created"""
    intermediate_files = [
        'passive_enum.txt',
        'active_enum.txt',
        'cert_trans.txt',
        'passive_subs.txt',
        'active_subs.txt',
        'crt_subs.txt',
        'filtered_subs.txt',
        'live_subs_detailed.txt',
        'subfinder.txt',
        'assetfinder.txt',
        'ffuf_subs.json'
    ]
    
    for filename in intermediate_files:
        filepath = os.path.join(folder, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Cleaned up: {filename}")
            except Exception as e:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to remove {filename}: {e}")

def main():
    if not check_venv_active():
        print("\n" + "="*60)
        print(f"{Fore.CYAN}ReconX-CLI: Automated Subdomain Enumeration Tool{Style.RESET_ALL}")
        print("="*60 + "\n")
        if not create_and_activate_venv():
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to setup virtual environment")
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

    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Checking and installing required tools...\n")
    ensure_tools_installed()

    # Create target-specific folder
    target_folder = create_target_folder(target)
    print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Created results folder: {target_folder}\n")

    print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Starting subdomain enumeration for {target}\n")
    
    # Prompt for wordlist
    print("\n" + "="*60)
    print(f"{Fore.CYAN}Wordlist Configuration{Style.RESET_ALL}")
    print("="*60)
    active_wordlist = get_wordlist_from_user("Phase 2 (Active Enumeration)")

    # Run phases sequentially
    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Running Phase 1: Passive Enumeration...")
    passive_subs = passive_enumeration(target, target_folder)
    
    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Running Phase 2: Active Enumeration...")
    active_subs = active_enumeration(target, target_folder, active_wordlist)
    
    print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Running Phase 3: Certificate Transparency...")
    cert_subs = certificate_transparency(target, target_folder)

    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Passive enumeration completed: {len(passive_subs)} subdomains")
    save_phase_results(target_folder, 'passive_enum', passive_subs)
    
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Active enumeration completed: {len(active_subs)} subdomains")
    save_phase_results(target_folder, 'active_enum', active_subs)
    
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Certificate transparency completed: {len(cert_subs)} subdomains")
    save_phase_results(target_folder, 'cert_trans', cert_subs)

    # Combine raw subdomains from all three phases
    all_subs_raw = set(passive_subs + active_subs + cert_subs)
    
    # Create all_subs_raw.txt by combining passive_subs.txt, active_subs.txt, and crt_subs.txt
    all_subs_raw_file = os.path.join(target_folder, 'all_subs_raw.txt')
    with open(all_subs_raw_file, 'w') as f:
        for sub in sorted(all_subs_raw):
            f.write(f'{sub}\n')
    
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Total raw subdomains: {len(all_subs_raw)}")

    # Phase 4: Verification & Filtering
    live_subs = verification_filtering(list(all_subs_raw), target, target_folder)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Live subdomains verified: {len(live_subs)}")

    # Output final results
    output_file = os.path.join(target_folder, 'live_subs.txt')
    with open(output_file, 'w') as f:
        for sub in sorted(live_subs):
            f.write(f"{sub}\n")

    print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Results saved to {output_file}\n")

    # Cleanup intermediate files
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} Cleaning up intermediate files...\n")
    cleanup_intermediate_files(target_folder)

    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Enumeration completed successfully!\n")

if __name__ == "__main__":
    main()
