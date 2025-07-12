# 📧 Gmail Interactive Client

A powerful command-line Gmail client with advanced search capabilities, smart sorting, and intuitive interface. Built with Python and designed for productivity.

## ✨ Features

### 🚀 Core Functionality
- **IMAP-based Gmail Access**: Secure connection to Gmail using IMAP protocol
- **Interactive Menu Interface**: User-friendly CLI with numbered menu options
- **Real-time Email Fetching**: Browse recent emails with detailed information
- **Individual Email Viewing**: Read complete email content by UID

### 🔍 Advanced Search
- **Smart Query Search**: Semantic search with WordNet-powered synonym expansion
- **Date-based Search**: Flexible date parsing with multiple format support
- **Multi-level Sorting**: Relevance → Date → Alphabetical → Numerical sorting
- **Relevance Scoring**: Intelligent ranking based on subject and sender matches

### 📅 Date Search Capabilities
- Natural language dates: `"today"`, `"yesterday"`, `"last week"`
- Month/year ranges: `"march 2025"`, `"july"`, `"2024"`
- Specific dates: `"7 july 2025"`, `"10/7/2025"`, `"15-03-2024"`
- Day names: `"monday"`, `"thursday"`
- Numeric shortcuts: `"12"` (December), `"25"` (25th of current month)

### 🎯 Smart Features
- **Email Caching**: Optimized performance with intelligent caching
- **Graceful Error Handling**: Robust error management and user feedback
- **Keyboard Interrupt Support**: Clean exit with Ctrl+C
- **Progress Indicators**: Real-time progress during email fetching

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Gmail account with IMAP enabled
- Gmail App Password (recommended for security)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mailgen
   ```

2. **Run the installation script**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Activate virtual environment and run**:
   ```bash
   source venv/bin/activate
   ./gmail-client
   ```

### Manual Installation

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   # or
   ./gmail-client
   ```

## 🔐 Gmail Setup

### Enable IMAP Access
1. Go to Gmail Settings → Forwarding and POP/IMAP
2. Enable IMAP access
3. Save changes

### Create App Password (Recommended)
1. Go to Google Account Settings → Security
2. Enable 2-Factor Authentication (if not already enabled)
3. Generate an App Password for "Mail"
4. Use this password instead of your regular Gmail password

## 🎮 Usage

### Starting the Application
```bash
source venv/bin/activate
./gmail-client
```

The application will prompt for your Gmail credentials:
- **Email**: Your Gmail address
- **Password**: Your Gmail password or App Password

### Menu Options

#### 1. 📧 Email List (Recent 20)
Fetches and displays the 20 most recent emails with:
- UID (for individual access)
- Sender information
- Subject line
- Date received

#### 2. 🔍 Email by UID (Brief View)
View complete email content by entering the UID:
- Full sender details
- Complete subject
- Email body (truncated if too long)
- Formatted display

#### 3. 🔎 Search Emails by Query
Powerful search with semantic enhancement:
- Enter any search term
- Automatic synonym expansion using WordNet
- Smart sorting with relevance scoring
- Customizable result limit

**Example queries**:
- `"meeting"` → finds emails about meetings, conferences, appointments
- `"invoice"` → finds bills, receipts, payments, invoices
- `"project"` → finds work-related emails, tasks, assignments

#### 4. 📅 Search by Date
Flexible date search with multiple formats:

**Natural Language**:
- `"today"`, `"yesterday"`, `"tomorrow"`
- `"last week"`, `"monday"`, `"friday"`

**Month/Year Ranges**:
- `"march"` → All emails from March (current year)
- `"july 2025"` → All emails from July 2025
- `"2024"` → All emails from 2024

**Specific Dates**:
- `"7 july 2025"` → July 7th, 2025
- `"10/7/2025"` → October 7th, 2025 (US format)
- `"15-03-2024"` → March 15th, 2024

**Numeric Shortcuts**:
- `"12"` → December (current year)
- `"25"` → 25th of current month

#### 5. 🚪 Exit
Gracefully disconnect and exit the application.

## 📁 Project Structure

```
mailgen/
├── main.py              # Main application entry point
├── gmail_client.py      # Gmail IMAP client implementation
├── email_search.py      # Search functionality and algorithms
├── search_utils.py      # Utility functions for search operations
├── display_utils.py     # Email display and formatting
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── install.sh         # Installation script
├── gmail-client       # CLI launcher script
├── .gitignore         # Git ignore rules
└── README.md          # This documentation
```

## ⚙️ Configuration

### Settings (config.py)
- `DEFAULT_EMAIL_LIMIT = 20`: Default number of emails to fetch
- `DEFAULT_DATE_LIMIT = 10`: Default limit for date searches
- `MAX_SUBJECT_LENGTH = 50`: Maximum subject length in display
- `MAX_FROM_LENGTH = 30`: Maximum sender length in display
- `MAX_BODY_PREVIEW = 1000`: Maximum body preview characters

### IMAP Settings
- Server: `imap.gmail.com`
- Port: `993` (SSL)
- Authentication: Username/Password or App Password

## 🚀 Google Cloud Deployment

The project includes deployment capabilities for Google Cloud Platform:

### Quick GCP Deployment
```bash
# Start VM instance
export PATH="/path/to/google-cloud-sdk/bin:$PATH"
gcloud compute instances start gmail-client-vm --zone=us-west1-b

# Run the application on VM
gcloud compute ssh gmail-client-vm --zone=us-west1-b --command="cd /opt/gmail-client && source venv/bin/activate && python3 main.py"

# Stop VM when done
gcloud compute instances stop gmail-client-vm --zone=us-west1-b
```

### VM Management Commands
```bash
# List instances
gcloud compute instances list --filter="name:gmail-client-vm"

# Check instance status
gcloud compute instances describe gmail-client-vm --zone=us-west1-b
```

## 🧪 Dependencies

- **nltk**: Natural Language Toolkit for semantic search
- **python-dateutil**: Advanced date parsing capabilities
- **imaplib**: Built-in Python IMAP client (standard library)
- **email**: Email parsing utilities (standard library)

## 🔒 Security Features

- **No credential storage**: Credentials are entered at runtime
- **App Password support**: Recommended over regular passwords
- **Secure IMAP connection**: SSL/TLS encryption
- **Graceful session management**: Proper connection cleanup
- **Error handling**: Safe handling of authentication failures

## 🛡️ Privacy & Security

- ✅ Credentials are **never stored** on disk
- ✅ All connections use **SSL/TLS encryption**
- ✅ Supports **Gmail App Passwords** for enhanced security
- ✅ **Read-only access** - no email modification capabilities
- ✅ **Local processing** - emails are not sent to external servers

## 🐛 Troubleshooting

### Common Issues

#### "Login failed" Error
- Verify IMAP is enabled in Gmail settings
- Use App Password instead of regular password
- Check username/password for typos

#### "Connection error" 
- Check internet connectivity
- Verify firewall allows IMAP connections (port 993)
- Try different network if on restrictive network

#### Missing Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt

# For NLTK issues
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

#### Permission Denied (gmail-client script)
```bash
chmod +x gmail-client
```

### Debug Mode
For detailed error information, modify `config.py` to enable debug logging.

## 🔄 Version History

### Current Version
- ✅ Interactive CLI interface
- ✅ Advanced search with semantic enhancement
- ✅ Flexible date parsing
- ✅ Smart multi-level sorting
- ✅ Google Cloud deployment support
- ✅ Comprehensive error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is open source. Please ensure compliance with Gmail's Terms of Service when using this client.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Gmail IMAP documentation
3. Ensure all dependencies are properly installed
4. Verify Gmail account settings and permissions

---

**⚡ Quick Start Reminder**:
```bash
./install.sh
source venv/bin/activate
./gmail-client
```

**Happy emailing! 📧✨**
