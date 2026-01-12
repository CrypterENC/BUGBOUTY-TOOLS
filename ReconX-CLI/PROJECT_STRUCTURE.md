# ReconX-CLI Project Structure

## Directory Layout

```
ReconX-CLI/
├── main.py                          # Main entry point
├── setup.py                         # Setup script (root level)
├── requirements.txt                 # Python dependencies
├── README.md                        # Project README
├── DOCS.md                          # Complete documentation
├── PROJECT_STRUCTURE.md             # This file
├── __init__.py                      # Package initialization
│
├── modules/                         # Enumeration modules
│   ├── __init__.py                 # Package initialization
│   ├── passive_enum.py             # Passive subdomain enumeration
│   ├── active_enum.py              # Active subdomain enumeration (DNS brute force)
│   ├── cert_trans.py               # Certificate transparency enumeration
│   └── verify_filter.py            # Verification and filtering module
│
├── utils/                           # Utility modules
│   ├── __init__.py                 # Package initialization
│   ├── installer.py                # Auto-installer with OS detection
│   └── setup.py                    # Setup script (utils version)
│
└── docs/                            # Documentation (legacy)
    └── INSTALLATION.md             # Installation guide (legacy)
```

## Module Descriptions

### Main Entry Point

**main.py**
- Parses command-line arguments
- Calls auto-installer to check/install tools
- Orchestrates enumeration phases
- Runs phases in parallel for speed
- Saves results to final_subdomains.txt

### Enumeration Modules (modules/)

**passive_enum.py**
- Uses: subfinder, amass, assetfinder
- Performs passive subdomain discovery from public sources
- Returns list of discovered subdomains

**active_enum.py**
- Uses: knockpy, ffuf
- Performs active DNS brute forcing
- Returns list of discovered subdomains

**cert_trans.py**
- Uses: crt.sh API
- Queries certificate transparency logs
- Returns list of subdomains from SSL certificates

**verify_filter.py**
- Uses: httpx
- Filters invalid subdomains
- Verifies live subdomains
- Returns list of verified live subdomains

### Utility Modules (utils/)

**installer.py**
- ToolInstaller class: Manages tool installation
- OS detection (Windows/Kali Linux)
- Tool availability checking
- Automatic installation with appropriate methods per OS
- PATH management for Go binaries
- Installation verification

**setup.py**
- Standalone setup script
- Calls ToolInstaller for interactive setup
- Prompts user for installation confirmation

### Configuration Files

**requirements.txt**
- Python package dependencies
- requests>=2.28.0
- knockpy>=5.0.0

**README.md**
- Project overview
- Quick start guide
- Feature list

**DOCS.md**
- Comprehensive documentation
- Installation instructions
- Usage guide
- API reference
- Architecture overview
- Troubleshooting guide
- Examples

## Import Structure

### From main.py

```python
from utils.installer import ensure_tools_installed
from modules.passive_enum import passive_enumeration
from modules.active_enum import active_enumeration
from modules.cert_trans import certificate_transparency
from modules.verify_filter import verification_filtering
```

### From setup.py

```python
from utils.installer import ToolInstaller
```

### From modules/__init__.py

```python
from .passive_enum import passive_enumeration
from .active_enum import active_enumeration
from .cert_trans import certificate_transparency
from .verify_filter import verification_filtering
```

### From utils/__init__.py

```python
from .installer import ToolInstaller, ensure_tools_installed
```

## Execution Flow

```
main.py
  │
  ├─→ ensure_tools_installed() [from utils.installer]
  │    ├─→ Detect OS
  │    ├─→ Check all tools
  │    ├─→ Install missing tools
  │    └─→ Verify installation
  │
  ├─→ passive_enumeration() [from modules.passive_enum]
  │    ├─→ Run subfinder
  │    ├─→ Run amass
  │    └─→ Run assetfinder
  │
  ├─→ active_enumeration() [from modules.active_enum]
  │    ├─→ Run knockpy
  │    └─→ Run ffuf
  │
  ├─→ certificate_transparency() [from modules.cert_trans]
  │    └─→ Query crt.sh API
  │
  ├─→ verification_filtering() [from modules.verify_filter]
  │    ├─→ Filter invalid subdomains
  │    └─→ Verify with httpx
  │
  └─→ Save results to final_subdomains.txt
```

## Running the Tool

### Option 1: Direct Execution (Recommended)

```bash
python main.py example.com
```

Automatically checks and installs tools if needed.

### Option 2: Setup First

```bash
python setup.py
python main.py example.com
```

### Option 3: Manual Installation

```bash
pip install -r requirements.txt
python utils/installer.py
python main.py example.com
```

## File Organization Benefits

1. **Modularity**: Each enumeration technique is in its own module
2. **Maintainability**: Easy to update individual modules
3. **Reusability**: Modules can be imported independently
4. **Scalability**: Easy to add new enumeration modules
5. **Organization**: Clear separation of concerns
6. **Testing**: Each module can be tested independently

## Adding New Modules

To add a new enumeration module:

1. Create file in `modules/` directory (e.g., `modules/new_enum.py`)
2. Implement enumeration function
3. Add import to `modules/__init__.py`
4. Update `main.py` to call the new function
5. Update documentation

Example:

```python
# modules/new_enum.py
def new_enumeration(target):
    """Perform new enumeration technique"""
    subs = set()
    # Implementation here
    return list(subs)
```

Then in `main.py`:

```python
from modules.new_enum import new_enumeration

# In main():
new_future = executor.submit(new_enumeration, target)
new_subs = new_future.result()
```

## Version Information

- **Version**: 1.0.0
- **Author**: iDOR
- **Last Updated**: 2026-01-13

## Project Statistics

- **Total Modules**: 4 enumeration + 1 utility
- **Total Lines of Code**: ~800
- **Supported OS**: Kali Linux, Windows
- **Python Version**: 3.7+
- **External Tools**: 7 (subfinder, amass, assetfinder, knockpy, ffuf, httpx, Go)
