#!/usr/bin/env python3
"""
Setup script for ReconX-CLI
Installs all required dependencies
"""
import sys
from installer import ToolInstaller

def main():
    print("\n" + "="*70)
    print(" "*15 + "ReconX-CLI Setup Script")
    print("="*70 + "\n")
    
    installer = ToolInstaller()
    
    if not installer.detect_os():
        print("[-] Unsupported operating system")
        return False
    
    print()
    
    # Check for existing tools
    if installer.check_all_tools():
        print("\n[+] All required tools are already installed!")
        return True
    
    print()
    print("[*] The following tools will be installed:")
    for tool in installer.missing_tools:
        print(f"    - {tool}")
    print()
    
    response = input("[?] Continue with installation? (y/n): ").strip().lower()
    if response != 'y':
        print("[-] Setup cancelled")
        return False
    
    print()
    
    # Install all missing tools
    if not installer.install_all_missing_tools():
        print("\n[!] Some tools failed to install")
        print("[!] Please try installing them manually")
        return False
    
    # Verify installation
    if not installer.verify_installation():
        print("[-] Verification failed")
        return False
    
    print("[+] Setup completed successfully!")
    print("[+] You can now run: python main.py <target_domain>")
    print()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
