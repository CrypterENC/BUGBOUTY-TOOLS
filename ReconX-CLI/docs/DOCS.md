# ReconX-CLI Documentation

Complete documentation for ReconX-CLI - Automated Subdomain Enumeration Tool

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Examples](#examples)
5. [API Reference](#api-reference)
6. [Architecture](#architecture)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Automatic Installation (Recommended)

ReconX-CLI automatically detects and installs missing tools on first run. Supports **Kali Linux** and **Windows**.

```bash
# Just run - tools will be installed automatically
python main.py example.com
```

Or run setup manually:

```bash
python setup.py
```

### Manual Installation (TL;DR)

```bash
# Install Go tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/owasp/amass/v3/...@latest
go install -v github.com/tomnomnom/assetfinder@latest
go install -v github.com/ffuf/ffuf@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Install Python dependencies
pip install -r requirements.txt

# Add Go binaries to PATH
export PATH=$PATH:$(go env GOPATH)/bin
```

### Usage (TL;DR)

```bash
python main.py example.com
```

Results saved to `final_subdomains.txt`

---

## Installation

### System Requirements

- Python 3.7+
- **Kali Linux** or **Windows** (with bash or PowerShell)
- Internet connection for passive and certificate transparency enumeration

### Automatic Installation (Recommended)

ReconX-CLI includes an auto-installer that detects your OS and installs all required tools automatically.

#### Option 1: Run During Enumeration

```bash
python main.py example.com
```

The tool will automatically:
1. Detect your OS (Kali Linux or Windows)
2. Check for missing tools
3. Install missing tools automatically
4. Verify installation
5. Start enumeration

#### Option 2: Run Setup Script

```bash
python setup.py
```

This will:
1. Check all required tools
2. Prompt for installation confirmation
3. Install missing tools
4. Verify installation

### Manual Installation

If you prefer to install tools manually:

#### 1. Install Go (if not already installed)

**Kali Linux:**
```bash
sudo apt-get update
sudo apt-get install -y golang-go
```

**Windows:**
- Download from https://golang.org/dl/
- Or use Chocolatey: `choco install golang`

#### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or individually:
```bash
pip install requests knockpy
```

#### 3. Install Go-based Tools

```bash
# Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Amass
go install -v github.com/owasp/amass/v3/...@latest

# Assetfinder
go install -v github.com/tomnomnom/assetfinder@latest

# FFUF
go install -v github.com/ffuf/ffuf@latest

# HTTPX
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
```

#### 4. Add Go Binaries to PATH

**Kali Linux:**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**
- Go binaries are typically in `%USERPROFILE%\go\bin`
- Add to PATH via System Environment Variables

### Verify Installation

Check that all tools are installed:

```bash
# Check Go tools
which subfinder
which amass
which assetfinder
which ffuf
which httpx

# Check Python packages
python -c "import requests; print(requests.__version__)"
python -c "import knockpy; print('Knockpy installed')"
```

### Auto-Installer Features

The `installer.py` module provides:

- **OS Detection**: Automatically detects Kali Linux or Windows
- **Tool Checking**: Verifies all required tools are installed
- **Auto-Installation**: Installs missing tools with appropriate methods for your OS
- **PATH Management**: Automatically adds Go binaries to PATH
- **Verification**: Confirms all tools work after installation
- **Error Handling**: Graceful fallback if installation fails

### Troubleshooting Installation

**Command not found errors**

If you get "command not found" errors after installation:

```bash
# Kali Linux: Reload shell profile
source ~/.bashrc
# or
source ~/.zshrc

# Windows: Restart PowerShell or Command Prompt
```

**Permission denied**

On Kali Linux, ensure binaries are executable:

```bash
chmod +x $(go env GOPATH)/bin/*
```

**Python import errors**

Reinstall Python packages:

```bash
pip install --upgrade -r requirements.txt
```

**Installation fails**

If auto-installation fails, try manual installation or check:

```bash
# Check Go installation
go version

# Check Python version
python --version

# Check pip
pip --version
```

---

## Usage

### Command Syntax

```bash
python main.py TARGET [OPTIONS]
```

### Arguments

- **TARGET** (required): The target domain to enumerate subdomains for
  - Example: `example.com`, `target.org`, `company.net`

### Basic Usage

```bash
# Automatic tool installation and enumeration
python main.py google.com
```

On first run, the tool will:
1. Check for required tools
2. Install any missing tools (if needed)
3. Verify installation
4. Start enumeration

### Console Output

The tool displays progress for each phase:

```
[*] Checking and installing required tools...

[*] Checking for required tools...

[+] subfinder: Installed
[+] amass: Installed
[+] assetfinder: Installed
[+] knockpy: Installed
[+] ffuf: Installed
[+] httpx: Installed
[+] requests: Installed

[+] All tools verified and ready to use!

[+] Starting subdomain enumeration for example.com

[+] Passive enumeration completed: 245 subdomains
[+] Active enumeration completed: 89 subdomains
[+] Certificate transparency completed: 156 subdomains
[+] Total raw subdomains: 412
[+] Live subdomains verified: 87

[+] Results saved to final_subdomains.txt
```

### Output Files

After execution, the following files are generated:

| File | Description |
|------|-------------|
| `final_subdomains.txt` | Final list of verified live subdomains (main output) |
| `filtered_subs.txt` | Subdomains after filtering but before verification |
| `live_subs_detailed.txt` | Detailed information about live subdomains with status codes |
| `subfinder.txt` | Raw output from subfinder |
| `amass_passive.txt` | Raw output from amass passive enumeration |
| `assetfinder.txt` | Raw output from assetfinder |
| `knockpy_results.json` | Raw output from knockpy in JSON format |
| `ffuf_subs.json` | Raw output from ffuf in JSON format |

### Enumeration Phases

**Phase 1: Passive Enumeration (1-5 minutes)**
Uses public data sources without active scanning:
- Subfinder: Fast passive subdomain discovery
- Amass: Comprehensive passive enumeration
- Assetfinder: Alternative passive source

**Phase 2: Active Enumeration (5-15 minutes)**
Performs DNS brute forcing:
- Knockpy: DNS brute force with common wordlists
- FFUF: Fast HTTP fuzzing for subdomain discovery

**Phase 3: Certificate Transparency (30s-2 minutes)**
Queries SSL certificate logs:
- crt.sh: Public certificate transparency logs

**Phase 4: Verification & Filtering (5-10 minutes)**
Validates and filters results:
- Removes invalid domains
- Verifies live subdomains using HTTPX
- Detects technologies and status codes

### Performance Tips

1. **Run on a fast connection**: Passive and certificate transparency phases require internet access
2. **Use a powerful machine**: Active enumeration is CPU-intensive
3. **Run during off-peak hours**: To avoid rate limiting from target servers
4. **Check tool availability**: Ensure all external tools are installed and in PATH

### Interpreting Results

**final_subdomains.txt**

Each line contains a verified live subdomain:

```
api.example.com
admin.example.com
mail.example.com
cdn.example.com
staging.example.com
```

**live_subs_detailed.txt**

Contains detailed information about each live subdomain:

```
https://api.example.com [200] [Apache] [Content-Length: 1234]
https://admin.example.com [403] [Nginx] [Content-Length: 567]
https://mail.example.com [301] [IIS] [Content-Length: 0]
```

---

## Examples

### Example 1: Simple Domain Enumeration

```bash
python main.py google.com
```

### Example 2: Enumerate Multiple Domains

```bash
#!/bin/bash
for domain in example.com target.org company.net; do
    echo "[*] Enumerating $domain"
    python main.py $domain
    mv final_subdomains.txt results_${domain}.txt
done
```

### Example 3: Filter Results by Pattern

```bash
# Get only API subdomains
grep "^api\." final_subdomains.txt

# Get only admin subdomains
grep "admin" final_subdomains.txt

# Get subdomains with specific TLD
grep "\.co\.uk$" final_subdomains.txt
```

### Example 4: Programmatic Usage

```python
#!/usr/bin/env python3
import sys
from passive_enum import passive_enumeration
from active_enum import active_enumeration
from cert_trans import certificate_transparency
from verify_filter import verification_filtering

def enumerate_domain(target):
    print(f"[*] Enumerating {target}")
    
    # Run individual phases
    passive = passive_enumeration(target)
    active = active_enumeration(target)
    cert = certificate_transparency(target)
    
    print(f"  Passive: {len(passive)}")
    print(f"  Active: {len(active)}")
    print(f"  Certificate: {len(cert)}")
    
    # Combine and verify
    all_subs = list(set(passive + active + cert))
    live = verification_filtering(all_subs, target)
    
    print(f"  Live: {len(live)}")
    return live

if __name__ == "__main__":
    target = sys.argv[1]
    results = enumerate_domain(target)
    
    for sub in sorted(results):
        print(sub)
```

### Example 5: Custom Filtering

```python
#!/usr/bin/env python3
import re
import sys
from verify_filter import verification_filtering

def filter_by_pattern(subdomains, pattern):
    """Filter subdomains by regex pattern"""
    return [sub for sub in subdomains if re.match(pattern, sub)]

# Read subdomains
with open('final_subdomains.txt', 'r') as f:
    all_subs = [line.strip() for line in f]

# Filter by pattern (e.g., api, admin, staging)
patterns = ['^api\.', '^admin\.', '^staging\.']
filtered = []
for pattern in patterns:
    filtered.extend(filter_by_pattern(all_subs, pattern))

print(f"Found {len(filtered)} matching subdomains:")
for sub in sorted(set(filtered)):
    print(sub)
```

### Example 6: Integration with Other Tools

```bash
#!/bin/bash
# Run ReconX-CLI and pipe results to other tools

TARGET="example.com"

# Enumerate subdomains
python main.py $TARGET

# Scan with nmap
cat final_subdomains.txt | while read sub; do
    echo "[*] Scanning $sub"
    nmap -p 80,443 $sub
done

# Check with curl
cat final_subdomains.txt | while read sub; do
    echo "[*] Checking $sub"
    curl -I https://$sub 2>/dev/null | head -1
done
```

### Example 7: Parallel Enumeration of Multiple Domains

```python
#!/usr/bin/env python3
import concurrent.futures
import sys
from passive_enum import passive_enumeration
from active_enum import active_enumeration
from cert_trans import certificate_transparency
from verify_filter import verification_filtering

def enumerate_domain(target):
    """Enumerate a single domain"""
    try:
        passive = passive_enumeration(target)
        active = active_enumeration(target)
        cert = certificate_transparency(target)
        
        all_subs = list(set(passive + active + cert))
        live = verification_filtering(all_subs, target)
        
        return target, live
    except Exception as e:
        print(f"[-] Error enumerating {target}: {e}")
        return target, []

def enumerate_domains(targets):
    """Enumerate multiple domains in parallel"""
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(enumerate_domain, t): t for t in targets}
        
        for future in concurrent.futures.as_completed(futures):
            target, subdomains = future.result()
            results[target] = subdomains
            print(f"[+] {target}: {len(subdomains)} live subdomains")
    
    return results

if __name__ == "__main__":
    targets = ['example.com', 'target.org', 'company.net']
    results = enumerate_domains(targets)
    
    # Save results
    for target, subs in results.items():
        with open(f'results_{target}.txt', 'w') as f:
            for sub in sorted(subs):
                f.write(f"{sub}\n")
```

### Example 8: Export Results in Different Formats

```python
#!/usr/bin/env python3
import json
import csv

def read_subdomains(filename='final_subdomains.txt'):
    """Read subdomains from file"""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def export_json(subdomains, output='results.json'):
    """Export to JSON"""
    data = {
        'count': len(subdomains),
        'subdomains': sorted(subdomains)
    }
    with open(output, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"[+] Exported to {output}")

def export_csv(subdomains, output='results.csv'):
    """Export to CSV"""
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Subdomain'])
        for sub in sorted(subdomains):
            writer.writerow([sub])
    print(f"[+] Exported to {output}")

# Read and export
subs = read_subdomains()
export_json(subs)
export_csv(subs)
```

### Example 9: Monitor for New Subdomains

```python
#!/usr/bin/env python3
import os
import time
from datetime import datetime
from passive_enum import passive_enumeration
from active_enum import active_enumeration
from cert_trans import certificate_transparency
from verify_filter import verification_filtering

def monitor_domain(target, interval=3600):
    """Monitor domain for new subdomains"""
    previous_subs = set()
    
    while True:
        print(f"\n[*] Checking {target} at {datetime.now()}")
        
        # Enumerate
        passive = passive_enumeration(target)
        active = active_enumeration(target)
        cert = certificate_transparency(target)
        
        all_subs = set(passive + active + cert)
        live = set(verification_filtering(list(all_subs), target))
        
        # Find new subdomains
        new_subs = live - previous_subs
        removed_subs = previous_subs - live
        
        if new_subs:
            print(f"[+] NEW SUBDOMAINS: {new_subs}")
        
        if removed_subs:
            print(f"[-] REMOVED SUBDOMAINS: {removed_subs}")
        
        previous_subs = live
        
        # Wait before next check
        print(f"[*] Waiting {interval} seconds until next check...")
        time.sleep(interval)

if __name__ == "__main__":
    target = "example.com"
    monitor_domain(target, interval=3600)  # Check every hour
```

### Example 10: Generate Report

```python
#!/usr/bin/env python3
from datetime import datetime
import json

def generate_report(target, subdomains):
    """Generate enumeration report"""
    report = {
        'target': target,
        'timestamp': datetime.now().isoformat(),
        'total_subdomains': len(subdomains),
        'subdomains': sorted(subdomains),
        'statistics': {
            'api_count': len([s for s in subdomains if 'api' in s]),
            'admin_count': len([s for s in subdomains if 'admin' in s]),
            'staging_count': len([s for s in subdomains if 'staging' in s]),
            'mail_count': len([s for s in subdomains if 'mail' in s]),
            'cdn_count': len([s for s in subdomains if 'cdn' in s]),
        }
    }
    
    # Save report
    with open(f'report_{target}.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"ENUMERATION REPORT: {target}")
    print(f"{'='*50}")
    print(f"Timestamp: {report['timestamp']}")
    print(f"Total Subdomains: {report['total_subdomains']}")
    print(f"\nStatistics:")
    for key, value in report['statistics'].items():
        print(f"  {key}: {value}")
    print(f"{'='*50}\n")
    
    return report

# Read results and generate report
with open('final_subdomains.txt', 'r') as f:
    subs = [line.strip() for line in f if line.strip()]

generate_report('example.com', subs)
```

---

## API Reference

### Module: passive_enum.py

**Function: `passive_enumeration(target)`**

Performs passive subdomain enumeration using public data sources.

**Parameters:**
- `target` (str): Target domain name

**Returns:**
- `list`: List of subdomains discovered through passive enumeration

**Example:**
```python
from passive_enum import passive_enumeration

subs = passive_enumeration('example.com')
print(f"Found {len(subs)} passive subdomains")
```

**Tools Used:**
- Subfinder
- Amass (passive mode)
- Assetfinder

---

### Module: active_enum.py

**Function: `active_enumeration(target)`**

Performs active subdomain enumeration through DNS brute forcing.

**Parameters:**
- `target` (str): Target domain name

**Returns:**
- `list`: List of subdomains discovered through active enumeration

**Example:**
```python
from active_enum import active_enumeration

subs = active_enumeration('example.com')
print(f"Found {len(subs)} active subdomains")
```

**Tools Used:**
- Knockpy (DNS brute force)
- FFUF (HTTP fuzzing)

**Timeouts:**
- Knockpy: 300 seconds (5 minutes)
- FFUF: 600 seconds (10 minutes)

---

### Module: cert_trans.py

**Function: `certificate_transparency(target)`**

Performs certificate transparency enumeration using crt.sh.

**Parameters:**
- `target` (str): Target domain name

**Returns:**
- `list`: List of subdomains discovered from certificate transparency logs

**Example:**
```python
from cert_trans import certificate_transparency

subs = certificate_transparency('example.com')
print(f"Found {len(subs)} subdomains from CT logs")
```

**API Used:**
- crt.sh certificate transparency API

**Timeout:**
- 30 seconds

---

### Module: verify_filter.py

**Function: `verification_filtering(all_subs_raw, target)`**

Filters and verifies live subdomains.

**Parameters:**
- `all_subs_raw` (list): List of subdomains to filter and verify
- `target` (str): Target domain name (used for validation pattern)

**Returns:**
- `list`: List of verified live subdomains

**Example:**
```python
from verify_filter import verification_filtering

all_subs = ['api.example.com', 'admin.example.com', 'invalid.com']
live_subs = verification_filtering(all_subs, 'example.com')
print(f"Verified {len(live_subs)} live subdomains")
```

**Filtering Criteria:**
- Removes wildcard entries (starting with `*`)
- Validates domain format using regex
- Ensures subdomain belongs to target domain

**Verification:**
- Uses HTTPX to check if subdomains are live
- Detects HTTP status codes
- Identifies technologies (tech-detect)
- Records content length

**Timeout:**
- 300 seconds (5 minutes)

---

### Module: main.py

**Function: `main()`**

Entry point for the CLI tool.

**Command Line Arguments:**
- `TARGET`: Target domain (required)

**Example:**
```bash
python main.py example.com
```

**Execution Flow:**
1. Parses command line arguments
2. Runs passive, active, and certificate transparency phases in parallel
3. Combines results from all phases
4. Runs verification and filtering
5. Saves results to `final_subdomains.txt`

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    main.py (Entry Point)                │
│              - Argument parsing                          │
│              - Orchestration                             │
│              - Parallel execution                        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐ ┌─────────┐ ┌──────────────┐
   │Passive  │ │ Active  │ │Certificate   │
   │Enum     │ │ Enum    │ │Transparency  │
   └────┬────┘ └────┬────┘ └──────┬───────┘
        │           │             │
        └───────────┼─────────────┘
                    │
                    ▼
        ┌──────────────────────┐
        │ Verify & Filter      │
        │ (verify_filter.py)   │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Output Results       │
        │ final_subdomains.txt │
        └──────────────────────┘
```

### Data Flow

```
TARGET
  │
  ├─→ [Passive Enum] → 245 subdomains
  ├─→ [Active Enum] → 89 subdomains
  └─→ [Cert Trans] → 156 subdomains
       │
       └─→ Combined: 412 subdomains (deduplicated)
            │
            └─→ [Verify & Filter]
                 │
                 ├─→ Filter: 387 valid subdomains
                 └─→ Verify: 87 live subdomains
                      │
                      └─→ OUTPUT: final_subdomains.txt
```

### Execution Model

**Sequential Execution**
```
Passive → Active → Cert Trans → Verify → Output
[1-5m]   [5-15m]  [30s-2m]     [5-10m]
Total: ~20-35 minutes
```

**Parallel Execution (Current)**
```
Passive ─┐
Active  ─┼─→ Verify → Output
Cert    ─┘
[5-15m]    [5-10m]
Total: ~10-25 minutes (40% faster)
```

### Performance Characteristics

- **Time Complexity**: O(n) where n = combined size of all enumeration sources
- **Space Complexity**: O(s) where s = total subdomains (typical: 10-100 MB)
- **Bottlenecks**: Network I/O, DNS queries, HTTP verification

---

## Troubleshooting

### Installation Issues

#### "command not found" errors

**Solution:**
```bash
# Check if Go is installed
go version

# Add Go binaries to PATH
export PATH=$PATH:$(go env GOPATH)/bin

# Make permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

#### Python module not found

**Solution:**
```bash
pip install requests
```

#### Permission denied when running tools

**Solution:**
```bash
chmod +x $(go env GOPATH)/bin/*
```

### Execution Issues

#### No subdomains found

**Causes & Solutions:**

a) **Target domain doesn't exist**
```bash
nslookup example.com
dig example.com
```

b) **Tools not installed**
```bash
which subfinder
which amass
which assetfinder
which knockpy
which ffuf
which httpx
```

c) **Network connectivity issues**
```bash
ping google.com
curl https://crt.sh
```

d) **Rate limiting**
- Wait 5-10 minutes before retrying
- Use a VPN if needed

#### Tool timeout errors

**Solution:**

a) **Increase timeout values** in the respective module
b) **Run tools individually** to identify the culprit
c) **Check system resources** with `top` or `htop`

#### Memory exhaustion

**Solution:**

a) **Reduce wordlist size** for active enumeration
b) **Run on a machine with more RAM**
c) **Process results in batches**

#### JSON parsing errors

**Solution:**

a) **Check tool output format**
b) **Update tool** to latest version
c) **Check file permissions**

### Output Issues

#### Empty output files

**Causes & Solutions:**

a) **Verification phase failed** - Check if HTTPX is installed
b) **Filtering too aggressive** - Review filtered_subs.txt
c) **All subdomains are down** - Verify target domain is online

#### Invalid subdomains in results

**Causes & Solutions:**

a) **Regex pattern too permissive** - Tighten validation rules
b) **Certificate transparency includes related domains** - Manual review recommended
c) **Active enumeration false positives** - Verify results manually

### Performance Issues

#### Tool runs very slowly

**Causes & Solutions:**

a) **Slow internet connection** - Use a faster network
b) **System resource constraints** - Close unnecessary applications
c) **Large wordlist** - Use smaller wordlist
d) **Rate limiting** - Use different IP/VPN

#### High CPU/Memory usage

**Solution:**

a) **Reduce parallelism** - Set max_workers=1 in main.py
b) **Reduce wordlist size**
c) **Run phases sequentially**

### Network Issues

#### Connection timeout to crt.sh

**Solution:**

a) **Increase timeout** in cert_trans.py
b) **Check crt.sh availability** with `curl -I https://crt.sh`
c) **Use proxy** if needed

#### DNS resolution failures

**Solution:**

a) **Check DNS configuration** with `nslookup` or `dig`
b) **Use different DNS server** (e.g., 8.8.8.8)
c) **Check network connectivity** with `ping 8.8.8.8`

### Tool-Specific Issues

#### Subfinder returns no results

**Solution:**
```bash
subfinder -d example.com -v
cat ~/.config/subfinder/config.yaml
```

#### Amass takes too long

**Solution:**
```bash
amass enum -passive -d example.com
timeout 600 amass enum -passive -d example.com
```

#### Knockpy returns JSON parsing error

**Solution:**
```bash
knockpy --version
pip install --upgrade knockpy
```

#### FFUF finds too many false positives

**Solution:**
```bash
ffuf -u https://FUZZ.example.com -w wordlist.txt -mc 200
```

#### HTTPX verification is very slow

**Solution:**
```bash
httpx -l subdomains.txt -timeout 5
httpx -l subdomains.txt -threads 100
```

### Debugging Steps

#### 1. Enable verbose logging

Add debug output to modules with print statements

#### 2. Test individual tools

```bash
subfinder -d example.com -silent -o test_subfinder.txt
amass enum -passive -d example.com -o test_amass.txt
assetfinder --subs-only example.com > test_assetfinder.txt
```

#### 3. Check intermediate files

```bash
ls -lah *.txt *.json
wc -l *.txt
head -20 final_subdomains.txt
```

#### 4. Run with Python debugger

```bash
python -m pdb main.py example.com
```

---

## Project Structure

```
ReconX-CLI/
├── main.py                    # Entry point
├── passive_enum.py            # Passive enumeration module
├── active_enum.py             # Active enumeration module
├── cert_trans.py              # Certificate transparency module
├── verify_filter.py           # Verification & filtering module
├── __init__.py                # Package initialization
├── README.md                  # Project README
└── DOCS.md                    # This file
```

---

## Key Features

- **Passive Enumeration**: Uses subfinder, amass, and assetfinder
- **Active Enumeration**: Uses knockpy and ffuf for DNS brute forcing
- **Certificate Transparency**: Queries crt.sh for SSL certificate logs
- **Verification & Filtering**: Validates live subdomains using httpx
- **Parallel Execution**: Runs enumeration phases concurrently for speed
- **Modular Architecture**: Clean separation of concerns with independent modules
- **Fast**: Optimized for speed with parallel execution
- **Reliable**: Graceful error handling and fallback mechanisms

---

## FAQ

**Q: How long does enumeration take?**
A: Typically 10-25 minutes depending on domain popularity and network speed.

**Q: Can I use this on any domain?**
A: Only on domains you own or have explicit permission to test.

**Q: What if a tool is not installed?**
A: The tool will skip that phase and continue with others. Install missing tools for complete results.

**Q: Can I run multiple domains in parallel?**
A: Yes, see the Examples section for parallel enumeration scripts.

**Q: How do I integrate this with my workflow?**
A: Use the API reference to import modules into your scripts.

---

## Version Information

- **Version**: 1.0.0
- **Author**: iDOR
- **Last Updated**: 2026-01-13

---

## Disclaimer

ReconX-CLI is designed for authorized security testing and reconnaissance. Users are responsible for ensuring they have proper authorization before enumerating any target domain. Unauthorized access to computer systems is illegal.

---

## License

ReconX-CLI is provided as-is for authorized security testing only.
