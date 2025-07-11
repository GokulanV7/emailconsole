# Gmail Interactive Client

A modular Python application for interacting with Gmail via IMAP, featuring email search, date-based filtering, and advanced sorting capabilities.

## Project Structure

```
mailgen/
├── main.py              # Main application entry point with user interface
├── gmail_client.py      # Core Gmail IMAP client class
├── email_search.py      # Email search operations (date, query-based)
├── search_utils.py      # Search utilities (date parsing, WordNet synonyms)
├── display_utils.py     # Email display and formatting utilities
├── config.py            # Configuration settings and credentials
└── README.md            # This file
```

## Features

1. **Email List View**: Display recent emails in a formatted table
2. **Email Details**: View full email content by UID
3. **Smart Search by Query**: Search emails using keywords with intelligent multi-level sorting
4. **Date-based Search**: Search emails by specific dates, months, or years
5. **Configurable Settings**: Centralized configuration for limits and display options

## Installation  Setup

### Quick Installation
```bash
# Clone or download the project
cd mailgen

# Run the installation script
./install.sh
```

### Manual Installation
1. Install required dependencies via pip:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```
   Use Gmail App Passwords for enhanced security.

### System-wide CLI Installation
```bash
pip install -e .
# Then run from anywhere:
gmail-client
```

## Usage

The application provides an interactive menu:
1. **Email List**: View recent emails (default: 20)
2. **Email by UID**: View detailed email content
3. **Smart Search by Query**: Search emails with intelligent multi-level sorting
4. **Search by Date**: Enhanced date search with flexible date format support
5. **Exit**: Close the application

## Security Notes

- Store credentials securely
- Use Gmail App Passwords for authentication
- Consider using environment variables for sensitive data
- Never commit credentials to version control

## Hosting  Distribution

- **GitHub Repository**: Share code via Git
- **Docker Container**: Use the `Dockerfile` for container setup
- **Executable Binary**: Use PyInstaller for standalone distribution

## Customization

Modify `config.py` to adjust:
- Default email fetch limits
- Display formatting settings
- IMAP server settings
