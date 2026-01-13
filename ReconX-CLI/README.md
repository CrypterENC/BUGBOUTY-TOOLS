# ReconX-CLI: Automated Subdomain Enumeration Tool

A comprehensive, modular CLI-based reconnaissance tool for automated subdomain enumeration with multiple enumeration techniques and screenshot capture capabilities.

## Features

- **Passive Enumeration (Phase 1)**: Uses subfinder and assetfinder for passive subdomain discovery
- **Active Enumeration (Phase 2)**: Uses ffuf for DNS brute forcing with user-provided wordlists
- **Certificate Transparency (Phase 3)**: Queries crt.sh for SSL certificate logs
- **Verification & Filtering (Phase 4)**: Validates live subdomains using httpx with detailed information
- **Screenshot Capture**: Uses GoWitness to capture screenshots of live subdomains with configurable timeouts
- **Sequential Execution**: Runs enumeration phases sequentially for organized workflow
- **Automatic Setup**: Creates and activates Python venv, installs all dependencies automatically
- **Interactive Configuration**: Prompts user for wordlists and screenshot options
- **Colored Output**: Uses colorama for better terminal visibility
- **Modular Architecture**: Clean separation of concerns with independent modules

## Installation

### Quick Start

Simply run the script - it will automatically:
1. Create a Python virtual environment
2. Install all Python dependencies from requirements.txt
3. Check and install required tools (subfinder, assetfinder, ffuf, httpx, gowitness)
4. Relaunch itself in the virtual environment

```bash
python3 reconx_cli.py <TARGET>
```

### Manual Tool Installation (Optional)

If you prefer to install tools manually:

```bash
# Passive enumeration tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/tomnomnom/assetfinder@latest

# Active enumeration tool
go install -v github.com/ffuf/ffuf@latest

# Verification tool
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Screenshot capture tool
go install github.com/sensepost/gowitness@latest

# Python dependencies
pip install -r requirements.txt
```

## Usage

```bash
python3 reconx_cli.py <TARGET>
```

### Example

```bash
python3 reconx_cli.py example.com
```

### Interactive Prompts

During execution, you will be prompted for:

1. **Phase 2 Wordlist**: Enter path to DNS wordlist for active brute forcing
   - Example: `/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt`
   - Leave empty to skip Phase 2

2. **GoWitness Options**: Choose screenshot capture settings
   - Default: Standard timeout
   - Better: 15s timeout with 2 retries (slower but more reliable for slow hosts)

## Workflow

ReconX-CLI executes subdomain enumeration in 4 sequential phases:

### Phase 1: Passive Enumeration
- Uses **subfinder** and **assetfinder** for passive subdomain discovery
- Output: `passive_subs.txt`

### Phase 2: Active Enumeration
- Uses **ffuf** for DNS brute forcing with user-provided wordlist
- Output: `active_subs.txt`

### Phase 3: Certificate Transparency
- Queries **crt.sh** for SSL certificate logs
- Output: `crt_subs.txt`

### Phase 4: Verification & Filtering
1. Combines all subdomains into `all_subs_raw.txt`
2. Filters invalid domains and wildcards → `filtered_subs.txt`
3. Verifies live subdomains with **httpx** → `live_subs_detailed.txt`
4. Extracts live subdomains → `live_subs.txt`
5. Captures screenshots with **gowitness** (with configurable timeouts)
6. Cleans up intermediate files

## Output Files

Final output directory contains:

- **`live_subs.txt`** - Final list of verified live subdomains (one per line)
- **`all_subs_raw.txt`** - Combined raw subdomains from all phases
- **`gowitness.db`** - SQLite database with screenshots and metadata
- **`screenshots/`** - Directory containing captured screenshots

## Project Structure

```
ReconX-CLI/
├── reconx_cli.py           # Main entry point
├── requirements.txt        # Python dependencies
├── setup.py               # Setup configuration
├── utils/
│   └── installer.py       # Tool installation and checking
├── modules/
│   ├── passive_enum.py    # Phase 1: Passive enumeration
│   ├── active_enum.py     # Phase 2: Active enumeration
│   ├── cert_trans.py      # Phase 3: Certificate transparency
│   └── verify_filter.py   # Phase 4: Verification & filtering
├── docs/
│   ├── DOCS.md           # Detailed documentation
│   └── INSTALLATION.md   # Installation guide
└── README.md             # This file
```

## Modules

- **passive_enum.py**: Performs passive subdomain discovery using subfinder and assetfinder
- **active_enum.py**: Performs active DNS brute forcing using ffuf
- **cert_trans.py**: Queries certificate transparency logs via crt.sh
- **verify_filter.py**: Filters, verifies live subdomains with httpx, and captures screenshots with gowitness

## Requirements

- Python 3.6+
- Go 1.16+ (for tool installation)
- Internet connection (for crt.sh queries and tool downloads)

## Supported Platforms

- Linux
- macOS
- Windows (with WSL recommended)

## Performance

- **Sequential Execution**: Each phase waits for the previous to complete, ensuring organized workflow
- **Parallel Tool Execution**: Individual tools (subfinder, assetfinder) run concurrently within Phase 1
- **Timeout Handling**: All subprocess calls include timeouts to prevent hanging
- **Configurable Screenshot Options**: Choose between standard or better timeouts for GoWitness based on target responsiveness
