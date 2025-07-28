# Wandero Client Simulator

This tool simulates a realistic client interacting with the Wandero travel planning service via email. It automatically sends and receives emails using Gmail, and generates client responses using OpenAI's LLM.

##  Modular Structure

### `config.py`
- **Purpose**: Configuration and environment variables
- **Contains**: Environment variable loading, email settings, OpenAI API configuration

### `email_client.py`
- **Purpose**: Email handling and communication
- **Contains**: IMAP/SMTP connections, email search and parsing, threading support

### `ai_generator.py`
- **Purpose**: AI-powered response generation
- **Contains**: Initial email, client response, and follow-up email generation

### `analytics.py`
- **Purpose**: Analytics and performance tracking
- **Contains**: Response time tracking, Wandero performance analysis, business metrics

### `simulator.py`
- **Purpose**: Main orchestrator
- **Contains**: Main conversation loop, coordination between modules, error handling

##  Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in the project root with the following content:
   ```env
   EMAIL_ADDRESS=your_gmail_address@gmail.com
   EMAIL_PASSWORD=your_gmail_app_password
   WANDERO_EMAIL=hello@wandero.ai
   COMPANY_NAME=Your Company Name
   COMPANY_COUNTRY=Your Country
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```
   - For Gmail, you must use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if 2FA is enabled.

##  Usage

Run the simulator:
```bash
python simulator.py
```

The simulator will:
- Send an initial email to Wandero
- Wait for replies from Wandero
- Generate realistic client responses using AI
- Track Wandero's performance metrics
- Provide detailed analytics at the end

##  Analytics Features

The simulator tracks Wandero's performance including:
- **Response Speed**: How fast Wandero responds
- **Response Quality**: How comprehensive their answers are
- **Question Handling**: Whether they answer all client questions
- **Personalization**: How well they customize responses
- **Professional Communication**: Tone and professionalism
- **Business Acumen**: Budget consideration, upsell attempts, local knowledge

##  Realistic Client Behavior

The simulated client:
- Makes occasional typos and uses informal language
- Forgets important details and sends follow-up emails
- Asks clarifying questions
- Shows genuine interest in travel planning
- Uses casual, human-like communication


##  Performance Testing

The simulator provides comprehensive analytics to test Wandero's:
- Customer service quality
- Response times
- Personalization capabilities
- Business acumen
- Local knowledge
- Professional communication