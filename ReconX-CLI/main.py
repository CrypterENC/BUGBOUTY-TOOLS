#!/usr/bin/env python3
import argparse
import sys
import os
import concurrent.futures

from utils.installer import ensure_tools_installed
from modules.passive_enum import passive_enumeration
from modules.active_enum import active_enumeration
from modules.cert_trans import certificate_transparency
from modules.verify_filter import verification_filtering

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

    print(f"\n[+] Starting subdomain enumeration for {target}\n")

    # Run phases in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        passive_future = executor.submit(passive_enumeration, target)
        active_future = executor.submit(active_enumeration, target)
        cert_future = executor.submit(certificate_transparency, target)

        passive_subs = passive_future.result()
        active_subs = active_future.result()
        cert_subs = cert_future.result()

    print(f"[+] Passive enumeration completed: {len(passive_subs)} subdomains")
    print(f"[+] Active enumeration completed: {len(active_subs)} subdomains")
    print(f"[+] Certificate transparency completed: {len(cert_subs)} subdomains")

    # Combine raw subdomains
    all_subs_raw = set(passive_subs + active_subs + cert_subs)
    print(f"[+] Total raw subdomains: {len(all_subs_raw)}")

    # Phase 4: Verification & Filtering
    live_subs = verification_filtering(list(all_subs_raw), target)
    print(f"[+] Live subdomains verified: {len(live_subs)}")

    # Output final results
    output_file = 'final_subdomains.txt'
    with open(output_file, 'w') as f:
        for sub in sorted(live_subs):
            f.write(f"{sub}\n")

    print(f"\n[+] Results saved to {output_file}\n")

if __name__ == "__main__":
    main()
