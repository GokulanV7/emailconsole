# Gmail Interactive Client - Installation & Deployment Guide

## 🚀 Quick Start (Local Usage)

### Method 1: Direct Execution
```bash
cd /path/to/mailgen
source venv/bin/activate
python main.py
```

### Method 2: Using the CLI Launcher
```bash
cd /path/to/mailgen
source venv/bin/activate
./gmail-client
```

## 📦 Installing as a System-wide CLI Tool

### Method 1: Using pip (Recommended)
```bash
cd /path/to/mailgen
pip install -e .
```

After installation, you can run from anywhere:
```bash
gmail-client
# or
gmc
```

### Method 2: Manual Installation
```bash
# Copy to a directory in your PATH
sudo cp gmail-client /usr/local/bin/
sudo chmod +x /usr/local/bin/gmail-client

# Install dependencies globally
pip install nltk python-dateutil
```

## 🌐 Hosting Options

### 1. GitHub Repository
```bash
# Create a new repository on GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/gmail-interactive-client.git
git push -u origin main
```

### 2. PyPI Package
```bash
# Build the package
python setup.py sdist bdist_wheel

# Upload to PyPI (requires account)
pip install twine
twine upload dist/*
```

### 3. Docker Container
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x gmail-client

ENTRYPOINT ["./gmail-client"]
```

Build and run:
```bash
docker build -t gmail-client .
docker run -it gmail-client
```

### 4. Homebrew Formula (macOS)
Create a formula file for Homebrew distribution.

## 🔧 Environment Setup

### Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### System-wide Installation
```bash
pip install nltk python-dateutil
```

## 📋 Requirements

- Python 3.8+
- Internet connection
- Gmail account with App Password enabled

## 🔐 Security Notes

- Never commit credentials to version control
- Use Gmail App Passwords instead of account passwords
- The application prompts for credentials at runtime (not stored)

## 🐛 Troubleshooting

### Keyboard Interrupt Handling
The application now handles Ctrl+C gracefully:
- During credential entry: Exits cleanly
- During menu navigation: Returns to menu or exits
- During operations: Cancels operation and returns to menu

### Common Issues
1. **Import errors**: Ensure all dependencies are installed
2. **Permission denied**: Make sure the launcher script is executable
3. **IMAP errors**: Check Gmail settings and App Password

## 📚 Usage Examples

### Quick Commands
```bash
# Start the application
gmail-client

# Or use the short alias
gmc
```

### Keyboard Shortcuts
- `Ctrl+C`: Cancel current operation or exit
- `Enter`: Confirm selection
- Numbers `1-5`: Menu navigation
- Date inputs: Direct date searches in option 4

## 🔄 Updates

To update the application:
```bash
git pull origin main
pip install -r requirements.txt
```

If installed via pip:
```bash
pip install -e . --upgrade
```
