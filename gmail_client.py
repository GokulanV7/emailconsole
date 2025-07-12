import imaplib
import email
import re
from nltk.corpus import wordnet
import nltk
from datetime import datetime, timedelta
import dateutil.parser
from collections import defaultdict
import calendar
from config import IMAP_SERVER

try:
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
except:
    pass

class GmailClient:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.imap = None
        self.email_cache = {}
        
    def connect(self):
        """Connect to Gmail IMAP server"""
        try:
            self.imap = imaplib.IMAP4_SSL(IMAP_SERVER)
            result, login_data = self.imap.login(self.email_address, self.password)
            if result != 'OK':
                print("❌ Login failed!")
                return False
            else:
                print("✅ Connected to Gmail successfully!")
                self.imap.select("inbox")
                return True
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from Gmail"""
        if self.imap:
            try:
                self.imap.logout()
                print("✅ Disconnected from Gmail")
            except:
                pass
    
    def fetch_email_list(self, email_numbers=None, limit=50):
        """Fetch email list with basic info"""
        if email_numbers is None:
            # Get emails with a default limit
            result, data = self.imap.search(None, 'ALL')
            if result == 'OK' and data[0]:
                email_numbers = data[0].split()
                # Sort by most recent first
                email_numbers = sorted(email_numbers, key=int, reverse=True)
                # Apply default limit of 50
                email_numbers = email_numbers[:limit]
        
        emails = []
        total = len(email_numbers)
        
        print(f"📥 Fetching {total} emails...")
        
        for i, num in enumerate(email_numbers, 1):
            print(f"\rProgress: {i}/{total}", end="", flush=True)
            
            try:
                res, msg_data = self.imap.fetch(num, "(BODY[HEADER])")
                if res == 'OK':
                    raw_header = msg_data[0][1]
                    msg = email.message_from_bytes(raw_header)
                    
                    # Parse date for proper sorting
                    date_str = msg.get("date", "Unknown Date")
                    parsed_date = None
                    try:
                        parsed_date = dateutil.parser.parse(date_str)
                    except:
                        parsed_date = datetime.now()
                    
                    # Cache basic info
                    email_info = {
                        'uid': num.decode() if isinstance(num, bytes) else str(num),
                        'from': msg.get("from", "Unknown Sender"),
                        'subject': msg.get("subject", "No Subject"),
                        'date': msg.get("date", "Unknown Date"),
                        'parsed_date': parsed_date,
                        'size': len(raw_header)
                    }
                    
                    emails.append(email_info)
                    self.email_cache[email_info['uid']] = email_info
                    
            except Exception as e:
                continue
        
        print(f"\n✅ Fetched {len(emails)} emails")
        return emails
    
    def fetch_email_by_uid(self, uid):
        """Fetch complete email by UID"""
        try:
            res, msg_data = self.imap.fetch(uid, "(RFC822)")
            if res == 'OK':
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # Extract body
                body = ""
                html_body = ""
                
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        
                        if "attachment" in content_disposition:
                            continue
                            
                        if content_type == "text/plain":
                            try:
                                body = part.get_payload(decode=True).decode('utf-8')
                            except:
                                try:
                                    body = part.get_payload(decode=True).decode('latin-1')
                                except:
                                    body = str(part.get_payload())
                        elif content_type == "text/html":
                            try:
                                html_body = part.get_payload(decode=True).decode('utf-8')
                            except:
                                try:
                                    html_body = part.get_payload(decode=True).decode('latin-1')
                                except:
                                    html_body = str(part.get_payload())
                else:
                    try:
                        body = msg.get_payload(decode=True).decode('utf-8')
                    except:
                        try:
                            body = msg.get_payload(decode=True).decode('latin-1')
                        except:
                            body = str(msg.get_payload())
                
                if not body and html_body:
                    body = re.sub(r'<[^>]+>', '', html_body)
                
                return {
                    'uid': uid,
                    'from': msg.get("from", "Unknown Sender"),
                    'subject': msg.get("subject", "No Subject"),
                    'date': msg.get("date", "Unknown Date"),
                    'body': body.strip()
                }
                
        except Exception as e:
            print(f"❌ Error fetching email {uid}: {str(e)}")
            return None
