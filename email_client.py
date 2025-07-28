from imapclient import IMAPClient
import smtplib
from email.message import EmailMessage
from email import message_from_bytes
from email.header import decode_header
from config import *

# Conversation history
conversation_history = []

# Connect to IMAP (for receiving emails)
def connect_imap():
    try:
        server = IMAPClient(IMAP_HOST, ssl=True)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.select_folder('INBOX')
        return server
    except Exception as e:
        print(f"[IMAP] Connection error: {e}")
        return None

# Connect to SMTP (for sending emails)
def connect_smtp():
    try:
        smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        return smtp
    except Exception as e:
        print(f"[SMTP] Connection error: {e}")
        return None

# Send email via Gmail SMTP
def send_email(subject, body, to_email=WANDERO_EMAIL, in_reply_to=None, references=None):
    smtp = connect_smtp()
    if not smtp:
        print("[SMTP] Could not send email: SMTP connection failed.")
        return False
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add threading headers for proper email threading
    if in_reply_to:
        msg['In-Reply-To'] = in_reply_to
    if references:
        msg['References'] = references
    
    msg.set_content(body)
    try:
        smtp.send_message(msg)
        print(f"[SMTP] Email sent to {to_email} with subject: {subject}")
        smtp.quit()
        return True
    except Exception as e:
        print(f"[SMTP] Failed to send email: {e}")
        return False

# Check for new emails from Wandero (returns latest email text or None)
def check_for_new_email(last_uid=None, from_email=WANDERO_EMAIL, wait_time=10):
    server = connect_imap()
    if not server:
        print("[IMAP] Could not check email: IMAP connection failed.")
        return None, None
    try:
        # Search for unseen emails from Wandero
        print(f"[IMAP] Searching for new emails from: {from_email}")
        print(f"[IMAP] Your email: {EMAIL_ADDRESS}")
        print(f"[IMAP] Wandero email: {WANDERO_EMAIL}")
        print(f"[IMAP] Last processed UID: {last_uid}")
        
        # Try different search approaches
        try:
            # Search for unseen emails from the specific sender
            search_criteria = ['UNSEEN', 'FROM', from_email]
            print(f"[IMAP] Search criteria: {search_criteria}")
            messages = server.search(search_criteria)
            print(f"[IMAP] Found {len(messages)} unseen messages from {from_email}")
            
            # If we have a last_uid, only look for newer messages
            if last_uid and messages:
                # Filter for messages newer than last_uid
                newer_messages = [msg for msg in messages if msg > last_uid]
                print(f"[IMAP] Found {len(newer_messages)} newer messages")
                messages = newer_messages
            
            if messages:
                # Get the newest message
                latest_msg_id = max(messages)
                print(f"[IMAP] Processing message {latest_msg_id}")
                
                try:
                    raw_msg = server.fetch([latest_msg_id], ['RFC822'])[latest_msg_id][b'RFC822']
                    msg = message_from_bytes(raw_msg)
                    sender = msg['From']
                    print(f"[IMAP] Message {latest_msg_id} from: {sender}")
                    
                    subject, encoding = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or 'utf-8')
                    
                    # Get email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                try:
                                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                                    break
                                except:
                                    continue
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')
                        except:
                            body = msg.get_payload()
                    
                    print(f"[IMAP] New email with subject: {subject}")
                    server.logout()
                    return body, latest_msg_id
                except Exception as fetch_error:
                    print(f"[IMAP] Error fetching message {latest_msg_id}: {fetch_error}")
                    server.logout()
                    return None, None
            else:
                print(f"[IMAP] No new emails from {from_email} found")
                server.logout()
                return None, None
                
        except Exception as search_error:
            print(f"[IMAP] Search error: {search_error}")
            server.logout()
            return None, None
    except Exception as e:
        print(f"[IMAP] Error checking for new email: {e}")
        server.logout()
        return None, None 