import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
WANDERO_EMAIL = os.getenv('WANDERO_EMAIL')
COMPANY_NAME = os.getenv('COMPANY_NAME')
COMPANY_COUNTRY = os.getenv('COMPANY_COUNTRY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Gmail IMAP/SMTP settings
IMAP_HOST = 'imap.gmail.com'
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

# Debug: Print loaded values
print(f"[DEBUG] Loaded WANDERO_EMAIL: {WANDERO_EMAIL}")
print(f"[DEBUG] Loaded EMAIL_ADDRESS: {EMAIL_ADDRESS}")
print(f"[DEBUG] Loaded COMPANY_NAME: {COMPANY_NAME}")
print(f"[DEBUG] Loaded COMPANY_COUNTRY: {COMPANY_COUNTRY}")

# Initialize OpenAI
import openai
openai.api_key = OPENAI_API_KEY 