# Installation Guide

## System Requirements

- Python 3.7+
- Linux/macOS/Windows with bash or PowerShell
- Internet connection for passive and certificate transparency enumeration

## Prerequisites

ReconX-CLI depends on several external tools. Install them before using the tool.

### 1. Install Go (if not already installed)

```bash
# macOS
brew install go

# Linux (Ubuntu/Debian)
sudo apt-get install golang-go

# Or download from https://golang.org/dl/
```

### 2. Install Passive Enumeration Tools

#### Subfinder
```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

#### Amass
```bash
go install -v github.com/owasp/amass/v3/...@latest
```

#### Assetfinder
```bash
go install -v github.com/tomnomnom/assetfinder@latest
```

### 3. Install Active Enumeration Tools

#### Knockpy
```bash
pip install knockpy
```

#### FFUF
```bash
go install -v github.com/ffuf/ffuf@latest
```

### 4. Install Verification Tool

#### HTTPX
```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
```

### 5. Install Python Dependencies

```bash
pip install requests
```

## Verify Installation

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
```

## Troubleshooting

### Command not found errors

If you get "command not found" errors, ensure Go binaries are in your PATH:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH=$PATH:$(go env GOPATH)/bin

# Then reload
source ~/.bashrc  # or source ~/.zshrc
```

### Permission denied

On Linux/macOS, ensure binaries are executable:

```bash
chmod +x $(go env GOPATH)/bin/*
```

### Python import errors

Reinstall the requests package:

```bash
pip install --upgrade requests
```

## Docker Installation (Optional)

If you prefer using Docker:

```bash
docker build -t reconx-cli .
docker run -it reconx-cli example.com
```

(Requires Dockerfile to be created in the project root)
