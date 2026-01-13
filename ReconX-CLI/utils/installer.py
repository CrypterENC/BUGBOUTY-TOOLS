#!/usr/bin/env python3
import subprocess
import sys
import os
import platform
import shutil

class ToolInstaller:
    def __init__(self):
        self.os_type = platform.system()
        self.is_windows = self.os_type == "Windows"
        self.is_linux = self.os_type == "Linux"
        self.missing_tools = []
        self.failed_installs = []

    def detect_os(self):
        """Detect operating system"""
        print(f"[*] Detected OS: {self.os_type}")
        if self.is_windows:
            print("[*] Windows detected - using Windows installation methods")
        elif self.is_linux:
            print("[*] Linux detected - using Linux installation methods")
        else:
            print(f"[-] Unsupported OS: {self.os_type}")
            return False
        return True

    def check_command_exists(self, command):
        """Check if a command exists in PATH"""
        return shutil.which(command) is not None

    def check_python_package(self, package):
        """Check if a Python package is installed"""
        try:
            __import__(package)
            return True
        except ImportError:
            return False

    def run_command(self, command, shell=False):
        """Run a shell command and return success status"""
        try:
            if isinstance(command, str):
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
            else:
                result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=300)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"[-] Command timed out: {command}")
            return False
        except Exception as e:
            print(f"[-] Error running command: {e}")
            return False

    def check_go_installed(self):
        """Check if Go is installed"""
        if self.check_command_exists("go"):
            print("[+] Go is already installed")
            return True
        print("[-] Go is not installed")
        return False

    def install_go(self):
        """Install Go"""
        print("[*] Installing Go...")
        
        if self.is_windows:
            print("[*] Please install Go from https://golang.org/dl/")
            print("[*] Or use: choco install golang (if you have Chocolatey)")
            if self.check_command_exists("choco"):
                if self.run_command("choco install golang -y"):
                    print("[+] Go installed successfully")
                    return True
            return False
        
        elif self.is_linux:
            if self.run_command("sudo apt-get update"):
                if self.run_command("sudo apt-get install -y golang-go"):
                    print("[+] Go installed successfully")
                    return True
        
        return False

    def get_go_path(self):
        """Get Go binary path"""
        if self.is_windows:
            return os.path.expandvars("%USERPROFILE%\\go\\bin")
        else:
            home = os.path.expanduser("~")
            return os.path.join(home, "go", "bin")

    def add_go_to_path(self):
        """Add Go binaries to PATH"""
        go_path = self.get_go_path()
        
        if self.is_windows:
            os.environ['PATH'] = go_path + os.pathsep + os.environ.get('PATH', '')
            print(f"[+] Added {go_path} to PATH")
        else:
            shell_profile = os.path.expanduser("~/.bashrc")
            if os.path.exists(os.path.expanduser("~/.zshrc")):
                shell_profile = os.path.expanduser("~/.zshrc")
            
            with open(shell_profile, 'a') as f:
                f.write(f"\nexport PATH=$PATH:{go_path}\n")
            
            os.environ['PATH'] = go_path + os.pathsep + os.environ.get('PATH', '')
            print(f"[+] Added {go_path} to PATH in {shell_profile}")

    def install_subfinder(self):
        """Install Subfinder"""
        print("[*] Installing Subfinder...")
        
        if self.check_command_exists("subfinder"):
            print("[+] Subfinder is already installed")
            return True
        
        if not self.check_go_installed():
            if not self.install_go():
                print("[-] Failed to install Go")
                return False
        
        self.add_go_to_path()
        
        if self.run_command("go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"):
            print("[+] Subfinder installed successfully")
            return True
        
        print("[-] Failed to install Subfinder")
        return False

    def install_assetfinder(self):
        """Install Assetfinder"""
        print("[*] Installing Assetfinder...")
        
        if self.check_command_exists("assetfinder"):
            print("[+] Assetfinder is already installed")
            return True
        
        if not self.check_go_installed():
            if not self.install_go():
                print("[-] Failed to install Go")
                return False
        
        self.add_go_to_path()
        
        if self.run_command("go install -v github.com/tomnomnom/assetfinder@latest"):
            print("[+] Assetfinder installed successfully")
            return True
        
        print("[-] Failed to install Assetfinder")
        return False

    def install_ffuf(self):
        """Install FFUF"""
        print("[*] Installing FFUF...")
        
        if self.check_command_exists("ffuf"):
            print("[+] FFUF is already installed")
            return True
        
        if not self.check_go_installed():
            if not self.install_go():
                print("[-] Failed to install Go")
                return False
        
        self.add_go_to_path()
        
        if self.run_command("go install -v github.com/ffuf/ffuf@latest"):
            print("[+] FFUF installed successfully")
            return True
        
        print("[-] Failed to install FFUF")
        return False

    def install_httpx(self):
        """Install HTTPX"""
        print("[*] Installing HTTPX...")
        
        if self.check_command_exists("httpx"):
            print("[+] HTTPX is already installed")
            return True
        
        if not self.check_go_installed():
            if not self.install_go():
                print("[-] Failed to install Go")
                return False
        
        self.add_go_to_path()
        
        if self.run_command("go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"):
            print("[+] HTTPX installed successfully")
            return True
        
        print("[-] Failed to install HTTPX")
        return False


    def install_gowitness(self):
        """Install GoWitness"""
        print("[*] Installing GoWitness...")
        
        if self.check_command_exists("gowitness"):
            print("[+] GoWitness is already installed")
            return True
        
        if not self.check_go_installed():
            if not self.install_go():
                print("[-] Failed to install Go")
                return False
        
        self.add_go_to_path()
        
        # Try installing from go install first
        if self.run_command("go install github.com/sensepost/gowitness@latest"):
            print("[+] GoWitness installed successfully")
            return True
        
        # If that fails, try installing from git repository
        print("[*] Attempting to install from GitHub repository...")
        if self.run_command("go install github.com/sensepost/gowitness.git@latest"):
            print("[+] GoWitness installed successfully from GitHub")
            return True
        
        print("[-] Failed to install GoWitness")
        return False

    def install_requests(self):
        """Install Requests"""
        print("[*] Installing Requests...")
        
        if self.check_python_package("requests"):
            print("[+] Requests is already installed")
            return True
        
        if self.run_command(f"{sys.executable} -m pip install requests"):
            print("[+] Requests installed successfully")
            return True
        
        print("[-] Failed to install Requests")
        return False

    def check_all_tools(self):
        """Check if all required tools are installed"""
        print("\n[*] Checking for required tools...\n")
        
        tools = {
            "subfinder": self.check_command_exists("subfinder"),
            "assetfinder": self.check_command_exists("assetfinder"),
            "ffuf": self.check_command_exists("ffuf"),
            "httpx": self.check_command_exists("httpx"),
            "gowitness": self.check_command_exists("gowitness"),
            "requests": self.check_python_package("requests"),
        }
        
        for tool, installed in tools.items():
            status = "[+]" if installed else "[-]"
            print(f"{status} {tool}: {'Installed' if installed else 'Missing'}")
        
        self.missing_tools = [tool for tool, installed in tools.items() if not installed]
        return len(self.missing_tools) == 0

    def install_all_missing_tools(self):
        """Install all missing tools"""
        if not self.missing_tools:
            print("\n[+] All required tools are already installed!\n")
            return True
        
        print(f"\n[*] Found {len(self.missing_tools)} missing tool(s): {', '.join(self.missing_tools)}\n")
        print("[*] Starting installation...\n")
        
        installers = {
            "subfinder": self.install_subfinder,
            "assetfinder": self.install_assetfinder,
            "ffuf": self.install_ffuf,
            "httpx": self.install_httpx,
            "gowitness": self.install_gowitness,
            "requests": self.install_requests,
        }
        
        for tool in self.missing_tools:
            if tool in installers:
                if not installers[tool]():
                    self.failed_installs.append(tool)
            print()
        
        if self.failed_installs:
            print(f"\n[-] Failed to install: {', '.join(self.failed_installs)}")
            return False
        
        print("\n[+] All tools installed successfully!\n")
        return True

    def verify_installation(self):
        """Verify all tools are installed"""
        print("[*] Verifying installation...\n")
        
        if self.check_all_tools():
            print("\n[+] All tools verified and ready to use!\n")
            return True
        else:
            print(f"\n[-] Some tools are still missing: {', '.join(self.missing_tools)}\n")
            return False

    def run(self):
        """Run the installer"""
        print("\n" + "="*60)
        print("ReconX-CLI Tool Installer")
        print("="*60 + "\n")
        
        if not self.detect_os():
            return False
        
        print()
        
        if self.check_all_tools():
            print("\n[+] All required tools are already installed!\n")
            return True
        
        print()
        response = input("[?] Install missing tools? (y/n): ").strip().lower()
        
        if response != 'y':
            print("[-] Installation cancelled")
            return False
        
        print()
        
        if not self.install_all_missing_tools():
            print("\n[!] Some tools failed to install. Please install them manually.")
            print("[!] See DOCS.md for manual installation instructions.")
            return False
        
        return self.verify_installation()


def ensure_tools_installed():
    """Ensure all tools are installed before running enumeration"""
    installer = ToolInstaller()
    
    if not installer.detect_os():
        print("[-] Unsupported operating system")
        sys.exit(1)
    
    if not installer.check_all_tools():
        print(f"\n[!] Missing tools detected: {', '.join(installer.missing_tools)}")
        print("[*] Attempting automatic installation...\n")
        
        if not installer.install_all_missing_tools():
            print("\n[!] Some tools failed to install.")
            print("[!] Please install them manually or run: python setup.py")
            print("[!] See DOCS.md for manual installation instructions.")
            sys.exit(1)
    
    if not installer.verify_installation():
        print("[-] Tool verification failed")
        sys.exit(1)


if __name__ == "__main__":
    installer = ToolInstaller()
    success = installer.run()
    sys.exit(0 if success else 1)
