import openai
import random
from config import *

# Generate client response using LLM
def generate_client_response(conversation_history, latest_wandero_email):
    try:
        # Build conversation context
        conversation_text = ""
        for i, (sender, message) in enumerate(conversation_history):
            conversation_text += f"{sender}: {message}\n\n"
        
        # Create realistic client prompt
        prompt = f"""You are a realistic client planning a trip to {COMPANY_COUNTRY}. You are communicating with Wandero, a travel planning service.

Company Context: {COMPANY_NAME} in {COMPANY_COUNTRY}

Previous conversation:
{conversation_text}

Latest email from Wandero:
{latest_wandero_email}

Instructions:
1. Act as a natural, realistic client who might:
   - Provide requested information (but sometimes forget details)
   - Ask clarifying questions
   - Request changes to proposals
   - Confirm plans
   - Send follow-up emails with forgotten details
   - Show excitement or concern about travel plans
   - Ask about specific details (prices, dates, locations, etc.)

2. Be conversational and natural - use casual language, ask questions, show personality
3. If Wandero asks for information, provide realistic details about {COMPANY_COUNTRY} travel
4. If Wandero sends a proposal, either confirm it or request specific changes
5. Occasionally add forgotten details in follow-up messages
6. Keep responses concise but informative
7. Show genuine interest in the travel planning process
8. Always focus on {COMPANY_COUNTRY} - ask about specific cities, regions, or attractions in {COMPANY_COUNTRY}
9. DO NOT include "Subject:" or any email headers in the body - just write the email content directly
10. Be human-like: occasionally make small typos, use informal language, forget to mention some details, and be a bit scattered in your thoughts
11. Don't be too perfect - be realistic about what a real person would write in an email

Generate a natural client response to Wandero's latest email:"""

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a realistic client planning a trip. Be natural, conversational, and authentic in your responses."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.8
        )
        
        client_response = response.choices[0].message.content.strip()
        return client_response
        
    except Exception as e:
        print(f"[LLM] Error generating response: {e}")
        return "Thank you for your email. I'll get back to you soon with more details."

# Generate initial client email using LLM
def generate_initial_email():
    try:
        prompt = f"""You are a client planning a trip to {COMPANY_COUNTRY}. Generate an initial email to Wandero (a travel planning service) requesting help with trip planning.

Company Context: {COMPANY_NAME} in {COMPANY_COUNTRY}

Instructions:
1. Write a natural, realistic initial email
2. Include basic trip information (number of travelers, dates, destination preferences)
3. Ask for help with planning a trip to {COMPANY_COUNTRY} specifically
4. Be friendly and conversational
5. Show excitement about the trip to {COMPANY_COUNTRY}
6. Keep it concise but informative
7. Use a realistic name (like "Sarah", "Michael", "Emma", "David", etc.) - DO NOT use placeholder text like [Your Name]
8. Make it specific to {COMPANY_COUNTRY} travel - mention specific cities, regions, or attractions in {COMPANY_COUNTRY}
9. DO NOT include "Subject:" or any email headers in the body - just write the email content directly
10. Be human-like: occasionally make small typos, use informal language, forget to mention some details, and be a bit scattered in your thoughts
11. Don't be too perfect - be realistic about what a real person would write in an email
12. Use casual language like "hey", "thanks so much", "that sounds great", etc.

Generate the initial email:"""

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a realistic client planning a trip. Write natural, conversational emails with real names (never use placeholders like [Your Name]). Be specific and authentic."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"[LLM] Error generating initial email: {e}")
        return f"Hello! I'm planning a trip and would love your help with organizing everything. We're a group of 4 people looking to visit {COMPANY_COUNTRY} next month. Could you help us plan the perfect itinerary?"

# Generate follow-up email with forgotten details using LLM
def generate_follow_up_email(conversation_history):
    try:
        prompt = f"""Based on the conversation history, generate a realistic follow-up email where the client remembers something they forgot to mention.

Previous conversation:
{chr(10).join([f"{sender}: {message}" for sender, message in conversation_history[-4:]])}

Instructions:
1. Write a natural follow-up email starting with something like "Oops, I forgot to mention..." or "By the way..."
2. Add a realistic forgotten detail (dietary restrictions, accessibility needs, special requests, etc.)
3. Keep it brief and casual
4. Make it sound like a real person remembering something
5. Be human-like: occasionally make small typos, use informal language, and be a bit scattered
6. Use casual language like "hey", "btw", "thanks", etc.
7. Don't be too perfect - be realistic about what a real person would write in a quick follow-up

Generate the follow-up email:"""

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a client who forgot to mention something important. Write a natural follow-up email."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"[LLM] Error generating follow-up: {e}")
        return None 