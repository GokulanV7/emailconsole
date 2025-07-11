import sys
import signal
from gmail_client import GmailClient
from email_search import EmailSearch
from display_utils import display_email_list, display_email_brief
from config import EMAIL, PASSWORD, DEFAULT_EMAIL_LIMIT, DEFAULT_DATE_LIMIT

def signal_handler(sig, frame):
    """Handle keyboard interrupt (Ctrl+C) gracefully"""
    print("\n\n👋 Goodbye! Exiting Gmail Client...")
    sys.exit(0)

def get_credentials():
    """Prompt user for email credentials and store them for the session."""
    global EMAIL, PASSWORD
    try:
        EMAIL = input("Enter your Gmail address: ").strip()
        PASSWORD = input("Enter your Gmail password or app password: ").strip()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Exiting...")
        sys.exit(0)

def main():
    """Main user loop"""
    
    # Get credentials
    get_credentials()

    # Create Gmail client
    gmail = GmailClient(EMAIL, PASSWORD)
    
    if not gmail.connect():
        return
    
    # Create email search instance
    email_search = EmailSearch(gmail)
    
    current_emails = []
    
    print("\n🚀 Enhanced Gmail Interactive Client")
    print("=" * 50)
    
    while True:
        try:
            print("\n📋 MENU:")
            print("1. 📧 Email List (Recent 20)")
            print("2. 🔍 Email by UID (Brief View)")
            print("3. 🔎 Search Emails by Query")
            print("4. 📅 Search by Date")
            print("5. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Exiting Gmail Client...")
            break
        
        if choice == '1':
            print("\n🔄 Fetching recent emails...")
            current_emails = gmail.fetch_email_list(limit=DEFAULT_EMAIL_LIMIT)
            display_email_list(current_emails)
            
        elif choice == '2':
            try:
                uid = input("\nEnter email UID: ").strip()
                if uid:
                    print(f"\n🔄 Fetching email {uid}...")
                    email_data = gmail.fetch_email_by_uid(uid)
                    display_email_brief(email_data)
                else:
                    print("❌ Please enter a valid UID")
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled")
                continue
                
        elif choice == '3':
            try:
                query = input("\nEnter search query: ").strip()
                if query:
                    limit_input = input(f"How many emails to fetch? (default: {DEFAULT_EMAIL_LIMIT}): ").strip()
                    limit = int(limit_input) if limit_input.isdigit() else DEFAULT_EMAIL_LIMIT
                    
                    print(f"\n🔄 Searching for: {query} (smart sorting: relevance → date → alphabetical)")
                    current_emails = email_search.search_emails_by_query(query, limit, "smart")
                    display_email_list(current_emails, show_scores=True)
                else:
                    print("❌ Please enter a search query")
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled")
                continue
                
        elif choice == '4':
            try:
                date_query = input("\nEnter date/time (e.g., 'yesterday', 'today', '12', 'march', '7 july 2025', '10/7/2025'): ").strip()
                if date_query:
                    limit_input = input(f"How many emails to fetch? (default: {DEFAULT_DATE_LIMIT}): ").strip()
                    limit = int(limit_input) if limit_input.isdigit() else DEFAULT_DATE_LIMIT
                    
                    print(f"\n🔄 Searching emails for: {date_query}")
                    current_emails = email_search.search_emails_by_date(date_query, limit)
                    display_email_list(current_emails)
                else:
                    print("❌ Please enter a date query")
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled")
                continue
                
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
            
        else:
            print(f"❌ Invalid choice: '{choice}'. Please enter 1-5")
    
    gmail.disconnect()

if __name__ == "__main__":
    # Register signal handler for graceful exit
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Exiting Gmail Client...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
        sys.exit(1)
