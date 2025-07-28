import time
import random
import uuid
from config import *
from email_client import *
from ai_generator import *
from analytics import ConversationAnalytics

# Main conversation loop
def main():
    print("=== Wandero Client Simulator ===")
    print(f"Starting conversation with {WANDERO_EMAIL}")
    print(f"Company: {COMPANY_NAME} in {COMPANY_COUNTRY}")
    print("=" * 40)
    
    # Check if we should send initial email or continue existing conversation
    initial_email_sent = False
    last_uid = None
    conversation_rounds = 0
    max_rounds = 50  # Increased for continuous operation
    check_interval = 120  # Check every 2 minutes (120 seconds)
    
    # Initialize analytics
    analytics = ConversationAnalytics()
    
    while conversation_rounds < max_rounds:
        conversation_rounds += 1
        print(f"\n--- Round {conversation_rounds} ---")
        
        # Send initial email if not sent yet
        if not initial_email_sent:
            print("\n[CLIENT] Sending initial email...")
            initial_email = generate_initial_email()
            subject = "Trip Planning Request"
            print(f"Subject: {subject}")
            print(f"Body: {initial_email}")
            
            if send_email(subject, initial_email):
                conversation_history.append(("Client", initial_email))
                # Generate a Message-ID for threading
                message_id = f"<{uuid.uuid4()}@wandero-simulator>"
                analytics.record_email_sent(message_id)
                print("\n[CLIENT] Initial email sent successfully!")
                
                # Show real-time analytics
                print(f"\n[ANALYTICS] Round {conversation_rounds} Stats:")
                print(f"  - Emails sent: {analytics.emails_sent}")
                print(f"  - Emails received: {analytics.emails_received}")
                
                initial_email_sent = True
                # Wait before checking for response
                print(f"\n[CLIENT] Waiting {check_interval//60} minutes before checking for response...")
                time.sleep(check_interval)
                continue
            else:
                print("\n[ERROR] Failed to send initial email. Retrying in 5 minutes...")
                time.sleep(check_interval)
                continue
        
        # Wait for Wandero's response
        print(f"\n[CLIENT] Checking for Wandero's response (checking every {check_interval//60} minutes)...")
        wandero_response, new_uid = check_for_new_email(last_uid, wait_time=check_interval)
        
        if wandero_response:
            print(f"\n[WANDERO] Response received:")
            print(f"Body: {wandero_response}")
            conversation_history.append(("Wandero", wandero_response))
            analytics.record_email_received()
            
            # Calculate response time AFTER recording email received
            response_time = analytics.record_response_time()
            if response_time:
                print(f"\n[ANALYTICS] Wandero responded in {response_time/60:.1f} minutes")
            
            # Analyze Wandero's performance
            client_questions = None
            if conversation_history and conversation_history[-2][0] == "Client":
                client_questions = conversation_history[-2][1]  # Get the last client message
            analytics.analyze_wandero_response(wandero_response, client_questions)
            
            last_uid = new_uid
            
            # Show basic real-time stats only
            print(f"\n[ANALYTICS] Round {conversation_rounds} - Basic Stats:")
            print(f"  Emails sent: {analytics.emails_sent} | Received: {analytics.emails_received}")
            if analytics.response_times:
                avg_time = sum(analytics.response_times) / len(analytics.response_times)
                print(f"  Average response time: {avg_time/60:.1f} minutes")
                print(f"  Current score: {analytics.calculate_wandero_performance_score():.1f}/100")
            
            # Generate client response
            print("\n[CLIENT] Generating response...")
            client_response = generate_client_response(conversation_history, wandero_response)
            
            # Use consistent subject line
            subject = "Trip Planning Request"
            
            print(f"\n[CLIENT] Sending response...")
            print(f"Subject: {subject}")
            print(f"Body: {client_response}")
            
            # Prepare threading headers
            in_reply_to, references = analytics.get_threading_headers()
            
            if send_email(subject, client_response, in_reply_to=in_reply_to, references=references):
                conversation_history.append(("Client", client_response))
                # Generate a Message-ID for threading
                message_id = f"<{uuid.uuid4()}@wandero-simulator>"
                analytics.record_email_sent(message_id)
                print("\n[CLIENT] Response sent successfully!")
                
                # Show basic stats after client response
                print(f"\n[ANALYTICS] Round {conversation_rounds} - Client response sent")
                print(f"  Total emails: {analytics.emails_sent} sent | {analytics.emails_received} received")
                if analytics.response_times:
                    avg_time = sum(analytics.response_times) / len(analytics.response_times)
                    print(f"  Avg response time: {avg_time/60:.1f} min | Score: {analytics.calculate_wandero_performance_score():.1f}/100")
                
                # Wait before checking for next response
                print(f"\n[CLIENT] Waiting {check_interval//60} minutes before checking for response...")
                time.sleep(check_interval)
                continue
                
                # Occasionally send a follow-up email with forgotten details (more realistic frequency)
                if random.random() < 0.15 and conversation_rounds > 2:  # 15% chance after round 2
                    time.sleep(random.randint(60, 180))  # Wait 1-3 minutes
                    follow_up = generate_follow_up_email(conversation_history)
                    if follow_up:
                        print(f"\n[CLIENT] Sending follow-up email...")
                        follow_up_subject = "Trip Planning Request"
                        print(f"Subject: {follow_up_subject}")
                        print(f"Body: {follow_up}")
                        
                        # Prepare threading headers for follow-up
                        in_reply_to, references = analytics.get_threading_headers()
                        
                        if send_email(follow_up_subject, follow_up, in_reply_to=in_reply_to, references=references):
                            conversation_history.append(("Client", follow_up))
                            # Generate a Message-ID for threading
                            message_id = f"<{uuid.uuid4()}@wandero-simulator>"
                            analytics.record_email_sent(message_id)
                            print("\n[CLIENT] Follow-up sent successfully!")
            else:
                print("\n[ERROR] Failed to send response. Will retry in 5 minutes...")
                time.sleep(check_interval)
                continue
        else:
            print(f"\n[CLIENT] No new response from Wandero. Checking again in {check_interval//60} minutes...")
            time.sleep(check_interval)
            continue
    
    # Print analytics summary
    print(f"\n=== Conversation completed after {conversation_rounds} rounds ===")
    analytics.print_summary()
    print("Conversation history saved.")

if __name__ == "__main__":
    main() 