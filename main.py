import sys
import signal
from gmail_client import GmailClient
from email_search import EmailSearch
from display_utils import display_email_list, display_email_brief
from config import EMAIL, PASSWORD, DEFAULT_EMAIL_LIMIT, DEFAULT_DATE_LIMIT
from date_range_picker import get_date_range

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
            print("1. 📧 Email List (Recent 50)")
            print("2. 🔍 Email by UID (Brief View)")
            print("3. 🔎 Search Emails by Query")
            print("4. 📅 Search by Date")
            print("5. 📅 Date Range Picker (GUI)")
            print("6. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
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
            # Date Range Picker GUI
            try:
                print("\n📅 Opening Date Range Picker...")
                print("💡 Use the GUI to select your date range!")
                
                date_range = get_date_range()
                
                if date_range['confirmed']:
                    print("\n🔄 Searching emails in selected date range...")
                    current_emails = email_search.search_emails_by_date_range(
                        date_range['start_date'], 
                        date_range['end_date'], 
                        date_range['limit']
                    )
                    
                    # Prompt user for additional query
                    query = input("\nEnter additional query for this range (or press Enter to skip): ").strip()
                    if query:
                        print(f"\n🔄 Filtering for: {query} (within selected date range)")
                        # Filter the already fetched emails from the date range
                        from search_utils import get_related_words
                        related_words = get_related_words(query)
                        print(f"🔍 Filter terms: {related_words}")
                        
                        filtered_emails = []
                        for email in current_emails:
                            email_text = (email['subject'] + ' ' + email['from'] + ' ' + email.get('body', '')).lower()
                            # Check if any of the related words are in the email
                            if any(word.lower() in email_text for word in related_words):
                                filtered_emails.append(email)
                        
                        current_emails = filtered_emails
                        print(f"📧 Found {len(current_emails)} emails matching '{query}' in the selected date range")
                    
                    if current_emails:
                        display_email_list(current_emails)
                    else:
                        print("❌ No emails found containing the query within the selected range")
                else:
                    print("❌ Date range selection cancelled")
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled")
                continue
            except Exception as e:
                print(f"❌ Error with date range picker: {str(e)}")
                continue
                
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
            
        else:
            print(f"❌ Invalid choice: '{choice}'. Please enter 1-6")
    
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
