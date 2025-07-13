from datetime import datetime, timedelta
import calendar
from search_utils import get_related_words, parse_date_query, sort_by_relevance

class EmailSearch:
    def __init__(self, gmail_client):
        self.gmail_client = gmail_client
    
    def search_emails_by_date(self, date_query, limit=50):
        """Enhanced date search with month/year range support"""
        parsed_date, date_type = parse_date_query(date_query)
        print("🔍 Parsing date query: '{date_query}' → Parsed: {parsed_date} (Type: {date_type}")
        
        if not parsed_date:
            print(f"❌ Could not parse date: '{date_query}'")
            print("💡 Try formats like: 'july 7', '7 july 2025', '7/10/2025', 'march 2025', 'thursday', 'today', 'yesterday'")
            print("💡 Or just enter a number: '12' (for December), '3' (for March), '25' (for 25th of current month)")
            return []
        
        try:
            if date_type == "single_date":
                print(f"🔍 Searching for emails on: {parsed_date}")
                result, data = self.gmail_client.imap.search(None, f'(ON "{parsed_date}")')
                
            elif date_type == "month_range":
                month, year = parsed_date
                # Get first and last day of the month
                first_day = datetime(year, month, 1)
                last_day = datetime(year, month, calendar.monthrange(year, month)[1])
                
                first_day_str = first_day.strftime("%d-%b-%Y")
                last_day_str = last_day.strftime("%d-%b-%Y")
                
                print(f"🔍 Searching for emails in {calendar.month_name[month]} {year} ({first_day_str} to {last_day_str})")
                result, data = self.gmail_client.imap.search(None, f'(SINCE "{first_day_str}" BEFORE "{(last_day + timedelta(days=1)).strftime("%d-%b-%Y")}")')
                
            elif date_type == "year_range":
                year = parsed_date
                first_day = datetime(year, 1, 1)
                last_day = datetime(year, 12, 31)
                
                first_day_str = first_day.strftime("%d-%b-%Y")
                last_day_str = last_day.strftime("%d-%b-%Y")
                
                print(f"🔍 Searching for emails in {year} ({first_day_str} to {last_day_str})")
                result, data = self.gmail_client.imap.search(None, f'(SINCE "{first_day_str}" BEFORE "{(last_day + timedelta(days=1)).strftime("%d-%b-%Y")}")')
            
            if result == 'OK' and data[0]:
                email_numbers = data[0].split()
                
                # Sort by most recent first (newest to oldest)
                email_numbers = sorted(email_numbers, key=int, reverse=True)
                
                if limit and len(email_numbers) > limit:
                    email_numbers = email_numbers[:limit]
                    print(f"📧 Found {len(data[0].split())} emails, showing first {limit}")
                else:
                    print(f"📧 Found {len(email_numbers)} emails")
                
                return self.gmail_client.fetch_email_list(email_numbers)
            else:
                print(f"❌ No emails found for the specified date range")
                return []
                
        except Exception as e:
            print(f"❌ Date search error: {str(e)}")
            return []
    
    def search_emails_by_query(self, query, limit=50, sort_by="date"):
        """Search emails by query with improved sorting options"""
        related_words = get_related_words(query)
        print(f"🔍 Search terms: {related_words}")
        
        # Build IMAP search query
        if len(related_words) == 1:
            search_query = f'(OR (BODY "{related_words[0]}") (SUBJECT "{related_words[0]}"))'
        else:
            conditions = []
            for word in related_words:
                conditions.append(f'(OR (BODY "{word}") (SUBJECT "{word}"))')
            
            search_query = conditions[0]
            for condition in conditions[1:]:
                search_query = f'(OR {search_query} {condition})'
        
        try:
            result, data = self.gmail_client.imap.search(None, search_query)
            
            if result == 'OK' and data[0]:
                email_numbers = data[0].split()
                
                if limit and len(email_numbers) > limit:
                    email_numbers = email_numbers[:limit]
                    print(f"📧 Found {len(data[0].split())} emails, showing first {limit}")
                else:
                    print(f"📧 Found {len(email_numbers)} emails")
                
                emails = self.gmail_client.fetch_email_list(email_numbers)
                
                # Sort emails based on the sort_by parameter
                if sort_by == "date":
                    # Sort by date (newest first)
                    emails.sort(key=lambda x: x['parsed_date'], reverse=True)
                elif sort_by == "subject":
                    # Sort by subject alphabetically
                    emails.sort(key=lambda x: x['subject'].lower())
                elif sort_by == "sender":
                    # Sort by sender alphabetically
                    emails.sort(key=lambda x: x['from'].lower())
                elif sort_by == "relevance":
                    # Sort by relevance (based on how many related words match)
                    emails = sort_by_relevance(emails, related_words)
                elif sort_by == "smart":
                    # Smart sorting: relevance → date → alphabetical → numerical
                    emails = self.smart_sort_emails(emails, related_words)
                
                return emails
            else:
                print("❌ No emails found for the search query")
                return []
                
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return []
    
    def smart_sort_emails(self, emails, related_words):
        """Smart sorting: relevance → date → alphabetical → numerical"""
        import re
        
        for email in emails:
            # Calculate relevance score
            score = 0
            subject = email['subject'].lower()
            from_addr = email['from'].lower()
            
            for word in related_words:
                # Subject matches get highest priority
                if word in subject:
                    score += 10
                # From address matches get medium priority
                if word in from_addr:
                    score += 5
            
            email['relevance_score'] = score
            
            # Extract numbers from subject for numerical sorting
            numbers = re.findall(r'\d+', email['subject'])
            email['numeric_value'] = int(numbers[0]) if numbers else 0
            
            # Clean subject for alphabetical sorting
            email['clean_subject'] = re.sub(r'[^a-zA-Z\s]', '', email['subject']).strip().lower()
        
        # Multi-level sorting:
        # 1. Relevance score (highest first)
        # 2. Date (newest first)
        # 3. Alphabetical (A-Z)
        # 4. Numerical (lowest first)
        emails.sort(key=lambda x: (
            -x['relevance_score'],  # Negative for descending order
            -x['parsed_date'].timestamp(),  # Negative for newest first
            x['clean_subject'],  # Alphabetical A-Z
            x['numeric_value']  # Numerical ascending
        ))
        
        return emails
    
    def search_emails_by_date_range(self, start_date, end_date, limit=50):
        """Search emails within a specific date range"""
        try:
            # Convert dates to strings for IMAP search
            start_date_str = start_date.strftime("%d-%b-%Y")
            end_date_str = end_date.strftime("%d-%b-%Y")
            
            print(f"🔍 Searching for emails from {start_date_str} to {end_date_str}")
            
            # Add one day to end_date for BEFORE search (IMAP BEFORE is exclusive)
            end_date_plus_one = end_date + datetime.timedelta(days=1)
            end_date_plus_one_str = end_date_plus_one.strftime("%d-%b-%Y")
            
            result, data = self.gmail_client.imap.search(None, 
                f'(SINCE "{start_date_str}" BEFORE "{end_date_plus_one_str}")')
            
            if result == 'OK' and data[0]:
                email_numbers = data[0].split()
                
                # Sort by most recent first (newest to oldest)
                email_numbers = sorted(email_numbers, key=int, reverse=True)
                
                if limit and len(email_numbers) > limit:
                    email_numbers = email_numbers[:limit]
                    print(f"📧 Found {len(data[0].split())} emails, showing first {limit}")
                else:
                    print(f"📧 Found {len(email_numbers)} emails")
                
                return self.gmail_client.fetch_email_list(email_numbers)
            else:
                print(f"❌ No emails found for the specified date range")
                return []
                
        except Exception as e:
            print(f"❌ Date range search error: {str(e)}")
            return []
