# ReconX-CLI: Automated Subdomain Enumeration Tool

A fast, modular CLI-based reconnaissance tool for automated subdomain enumeration with multiple enumeration techniques.

## Features

- **Passive Enumeration**: Uses subfinder, amass, and assetfinder
- **Active Enumeration**: Uses knockpy and ffuf for DNS brute forcing
- **Certificate Transparency**: Queries crt.sh for SSL certificate logs
- **Verification & Filtering**: Validates live subdomains using httpx
- **Parallel Execution**: Runs enumeration phases concurrently for speed
- **Modular Architecture**: Clean separation of concerns with independent modules

## Installation

### Prerequisites

Ensure the following tools are installed on your system:

```bash
# Passive enumeration tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/owasp/amass/v3/...@latest
go install -v github.com/tomnomnom/assetfinder@latest

# Active enumeration tools
pip install knockpy
go install -v github.com/ffuf/ffuf@latest

# Verification tool
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Python dependencies
pip install requests
```

## Usage

```bash
python main.py <TARGET>
```

### Example

```bash
python main.py example.com
```

## Output

Results are saved to `final_subdomains.txt` containing all verified live subdomains.

## Project Structure

```
ReconX-CLI/
├── main.py                 # Main entry point
├── passive_enum.py         # Passive enumeration module
├── active_enum.py          # Active enumeration module
├── cert_trans.py           # Certificate transparency module
├── verify_filter.py        # Verification and filtering module
├── __init__.py             # Package initialization
└── README.md               # This file
```

## Modules

- **passive_enum.py**: Performs passive subdomain discovery using public sources
- **active_enum.py**: Performs active DNS brute forcing
- **cert_trans.py**: Queries certificate transparency logs
- **verify_filter.py**: Filters and verifies live subdomains

## Performance

The tool runs enumeration phases in parallel using ThreadPoolExecutor for maximum speed while maintaining system stability.

## Output Files

- `final_subdomains.txt` - Final list of verified live subdomains
- `filtered_subs.txt` - Filtered subdomains before verification
- `live_subs_detailed.txt` - Detailed information about live subdomains
- Various tool output files (subfinder.txt, amass_passive.txt, etc.)
