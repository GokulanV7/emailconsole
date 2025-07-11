import re
from nltk.corpus import wordnet
from datetime import datetime, timedelta
import dateutil.parser
import calendar

def get_related_words(query):
    """Get related words using WordNet"""
    synonyms = set()
    try:
        for syn in wordnet.synsets(query):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower().replace("_", " "))
    except:
        pass
    synonyms.add(query.lower())
    return sorted(list(synonyms))  # Sort alphabetically

def parse_date_query(date_query):
    """Enhanced date parsing with month/year support"""
    date_query = date_query.lower().strip()
    today = datetime.now()
    
    # Handle number-only inputs (for month or day)
    if date_query.isdigit():
        num = int(date_query)
        if 1 <= num <= 12:
            # Treat as month number
            year = today.year
            return (num, year), "month_range"
        elif 1 <= num <= 31:
            # Treat as day in current month
            try:
                target_date = datetime(today.year, today.month, num)
                return target_date.strftime("%d-%b-%Y"), "single_date"
            except:
                # If day doesn't exist in current month, try as month
                if num <= 12:
                    return (num, today.year), "month_range"
                pass
    
    # Handle specific date formats
    if re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', date_query):
        try:
            parsed_date = dateutil.parser.parse(date_query)
            return parsed_date.strftime("%d-%b-%Y"), "single_date"
        except:
            pass
    
    # Handle month and year patterns (e.g., "march 2025", "march", "2025")
    month_patterns = {
        'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
        'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6,
        'jul': 7, 'july': 7, 'aug': 8, 'august': 8, 'sep': 9, 'september': 9,
        'oct': 10, 'october': 10, 'nov': 11, 'november': 11, 'dec': 12, 'december': 12
    }
    
    # Extract year first
    year_match = re.search(r'\b(20\d{2})\b', date_query)
    year = int(year_match.group(1)) if year_match else today.year
    
    # Check for month-year pattern
    for month_name, month_num in month_patterns.items():
        if month_name in date_query:
            # Check if there's a specific day
            day_match = re.search(r'\b(\d{1,2})\b', date_query)
            if day_match and int(day_match.group(1)) <= 31:
                day = int(day_match.group(1))
                try:
                    target_date = datetime(year, month_num, day)
                    return target_date.strftime("%d-%b-%Y"), "single_date"
                except:
                    pass
            else:
                # Return month range for entire month
                return (month_num, year), "month_range"
    
    # Handle year only
    if re.search(r'\b(20\d{2})\b', date_query) and len(date_query.split()) == 1:
        return year, "year_range"
    
    # Handle specific date formats with month names
    if re.search(r'\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', date_query):
        try:
            parsed_date = dateutil.parser.parse(date_query)
            return parsed_date.strftime("%d-%b-%Y"), "single_date"
        except:
            pass
    
    # Handle day-month-year format (e.g., "7 july 2025", "15 march 2024")
    day_month_year_pattern = r'\b(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})\b'
    match = re.search(day_month_year_pattern, date_query)
    if match:
        try:
            parsed_date = dateutil.parser.parse(date_query)
            return parsed_date.strftime("%d-%b-%Y"), "single_date"
        except:
            pass
    
    # Handle month-day-year format (e.g., "july 7 2025", "march 15 2024")
    month_day_year_pattern = r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})\s+(\d{4})\b'
    match = re.search(month_day_year_pattern, date_query)
    if match:
        try:
            parsed_date = dateutil.parser.parse(date_query)
            return parsed_date.strftime("%d-%b-%Y"), "single_date"
        except:
            pass
    
    # Handle relative dates
    if 'today' in date_query:
        return today.strftime("%d-%b-%Y"), "single_date"
    elif 'yesterday' in date_query:
        return (today - timedelta(days=1)).strftime("%d-%b-%Y"), "single_date"
    elif 'tomorrow' in date_query:
        return (today + timedelta(days=1)).strftime("%d-%b-%Y"), "single_date"
    elif 'last week' in date_query:
        return (today - timedelta(days=7)).strftime("%d-%b-%Y"), "single_date"
    
    # Handle day names
    day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for i, day_name in enumerate(day_names):
        if day_name in date_query:
            days_back = (today.weekday() - i) % 7
            if days_back == 0:
                days_back = 7
            target_date = today - timedelta(days=days_back)
            return target_date.strftime("%d-%b-%Y"), "single_date"
    
    return None, None

def sort_by_relevance(emails, related_words):
    """Sort emails by relevance score based on related words"""
    for email in emails:
        score = 0
        subject = email['subject'].lower()
        from_addr = email['from'].lower()
        
        for word in related_words:
            # Subject matches get higher score
            if word in subject:
                score += 3
            # From address matches get medium score
            if word in from_addr:
                score += 2
        
        email['relevance_score'] = score
    
    # Sort by relevance score (highest first), then by date
    emails.sort(key=lambda x: (x['relevance_score'], x['parsed_date']), reverse=True)
    return emails
