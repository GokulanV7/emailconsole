from config import MAX_SUBJECT_LENGTH, MAX_FROM_LENGTH, MAX_BODY_PREVIEW

def display_email_list(emails, show_scores=False):
    """Display email list in table format with optional relevance scores"""
    if not emails:
        print("📭 No emails to display")
        return
    
    print("\n📧 EMAIL LIST")
    print("=" * 130)
    
    if show_scores:
        print(f"{'#':<3} {'UID':<8} {'SCORE':<6} {'FROM':<30} {'SUBJECT':<45} {'DATE':<25}")
    else:
        print(f"{'#':<3} {'UID':<8} {'FROM':<30} {'SUBJECT':<50} {'DATE':<25}")
    print("-" * 130)
    
    for i, email in enumerate(emails, 1):
        uid = email['uid']
        from_addr = email['from'][:MAX_FROM_LENGTH-2] + "..." if len(email['from']) > MAX_FROM_LENGTH else email['from']
        
        if show_scores:
            subject = email['subject'][:43] + "..." if len(email['subject']) > 45 else email['subject']
            score = email.get('relevance_score', 0)
            print(f"{i:<3} {uid:<8} {score:<6} {from_addr:<30} {subject:<45} {email['date'][:25]}")
        else:
            subject = email['subject'][:MAX_SUBJECT_LENGTH-2] + "..." if len(email['subject']) > MAX_SUBJECT_LENGTH else email['subject']
            print(f"{i:<3} {uid:<8} {from_addr:<30} {subject:<50} {email['date'][:25]}")
    
    print("=" * 130)

def display_email_brief(email_data):
    """Display email in brief format"""
    if not email_data:
        print("❌ Email not found")
        return
    
    print("\n📧 EMAIL DETAILS")
    print("=" * 100)
    print(f"UID: {email_data['uid']}")
    print(f"FROM: {email_data['from']}")
    print(f"SUBJECT: {email_data['subject']}")
    print(f"DATE: {email_data['date']}")
    print("\nBODY:")
    
    body = email_data['body']
    if body:
        # Clean and format body
        body_lines = [line.strip() for line in body.split('\n') if line.strip()]
        body_text = '\n'.join(body_lines)
        
        if len(body_text) > MAX_BODY_PREVIEW:
            body_text = body_text[:MAX_BODY_PREVIEW] + "\n... [CONTENT TRUNCATED]"
        
        formatted_body = '\n'.join([f"    {line}" for line in body_text.split('\n')])
        print(formatted_body)
    else:
        print("    [NO BODY CONTENT]")
    
    print("=" * 100)
