#!/usr/bin/env python3
import argparse
import sys
import os
import concurrent.futures
import shutil

from utils.installer import ensure_tools_installed
from modules.passive_enum import passive_enumeration
from modules.active_enum import active_enumeration
from modules.cert_trans import certificate_transparency
from modules.verify_filter import verification_filtering

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
        'knockpy_results.json',
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
    parser = argparse.ArgumentParser(
        description='ReconX-CLI: Automated Subdomain Enumeration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py example.com
  python main.py target.org
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

    # Run phases in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        passive_future = executor.submit(passive_enumeration, target, target_folder)
        active_future = executor.submit(active_enumeration, target, target_folder)
        cert_future = executor.submit(certificate_transparency, target, target_folder)

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
