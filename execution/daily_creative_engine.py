import argparse
import json
import smtplib
import random
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import viral_lab
import ai_refiner
import simera_brain
import studio_production

# Manual .env loader to avoid dependency issues
def load_env_manual():
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    # Remove quotes if present
                    value = value.strip().strip("'").strip('"')
                    os.environ[key.strip()] = value

load_env_manual()

# Load Knowledge Base
def load_knowledge_base(path="execution/ytb_knowledge.json"):
    with open(path, 'r') as f:
        return json.load(f)

# Content Generation Logic (Expanded for Email)
def generate_daily_email(kb, force_strategy=None):
    # Pick a random tool/pain point
    item = random.choice(kb['mappings'])
    # Pick a random strategy or use forced one
    if force_strategy:
        strategy = next((s for s in kb['strategies'] if s['name'] == force_strategy), None)
        if not strategy:
            print(f"Warning: Strategy '{force_strategy}' not found. Using random.")
            strategy = random.choice(kb['strategies'])
    else:
        strategy = random.choice(kb['strategies'])
    
    subject = f"DAILY STRATEGY: {strategy['name']} ({datetime.date.today()})"
    
    # SPECIAL REPORT: REDDIT DETECTIVE
    viral_report = ""
    if strategy['name'] == "The Reddit Detective":
        # Find a reddit simulation that matches the current pain point if possible
        r_sim = random.choice(kb.get('reddit_simulations', []))
        viral_report = viral_lab.generate_viral_ideas(r_sim['pain_id'], item['tool_name'], r_sim)

    # SIMERA NARRATIVE ENGINE
    simera = simera_brain.SimeraContentMachine()
    details_narrative = simera.generate_narrative(item['tool_name'], item['pain_point'], platform="Reddit")
    linkedin_narrative = simera.generate_narrative(item['tool_name'], item['pain_point'], platform="LinkedIn")
    
    body = f"""
    Rume,
    
    Here is your daily "Digital Sovereign" generated marketing packet.
    
    TODAY'S STRATEGY: {strategy['name']}
    FOCUS TOOL: {item['tool_name']}
    PAIN POINT: {item['pain_point']}
    
    {viral_report}
    
    ---
    PSYCHOLOGICAL ANGLE:
    "{strategy['hook']}"
    {strategy['angle']}
    ---
    
    [LINKEDIN DRAFT - ELITE NARRATIVE]
    {linkedin_narrative}
    
    [REDDIT / STORY DRAFT]
    {details_narrative}
    
    -------------------------------------------------------
    
    [X / TWITTER THREAD]
    1/5
    The $50 wall is crumbling.
    You are suffering from "{item['pain_point']}".
    
    2/5
    The "Ghost Note" you are missing isn't effort. It's infrastructure.
    Legacy tools charge you tax. We give you a passport.
    
    3/5
    The Fix: {item['tool_name']}.
    {item['solution_feature']}.
    
    4/5
    V2.0 is visually stunning. Futuristic. 
    A dashboard for the Niche Warlord.
    
    5/5
    {kb['pricing']['price']}.
    Join the Alpha Leaders.
    
    -------------------------------------------------------
    
    [VIDEO SCRIPT CONCEPT]
    Hook: Stare at camera. "You are flying blind."
    Problem: "This is the Digital Dark Age. {item['pain_point']}."
    Solution: Show V2.0 Dashboard. "This is {item['tool_name']}."
    Payoff: "Stylish. Futuristic. {kb['pricing']['price']}."
    """
    
    # --- STAGE 2: STUDIO PRODUCTION (Video/Slides/Infographics) ---
    print("--- Generating Multimedia Assets (Studio Mode) ---")
    production_brief = studio_production.create_production_brief(body)
    
    # --- STAGE 3: FLOCK NOTIFICATION ---
    print("--- Dispatching to Flock for Human Review ---")
    studio_production.dispatch_to_flock(production_brief)
    
    final_body = f"""
    Rume,
    
    Here is your "Digital Sovereign" Strategy Packet.
    
    =========================================
    PART 1: STRATEGY & NARRATIVE
    =========================================
    {body}
    
    =========================================
    PART 2: STUDIO PRODUCTION BRIEF
    (Generated for Video, Slides, and Design Team)
    =========================================
    {production_brief}
    
    -------------------------------------------------------
    [SYSTEM STATUS]
    - Strategy: {strategy['name']}
    - Narrative Engine: Simera Brain (Active)
    - Production Brief: Generated
    - Flock Notification: Attempted
    """
    
    return subject, final_body

def send_email(subject, body, recipients):
    # Load credentials from environment or .env file
    sender_email = os.getenv("SMTP_EMAIL", "agent@ytbpro.com")
    sender_password = os.getenv("SMTP_PASSWORD", "password")
    
    recipient_list = [r.strip() for r in recipients.split(',')]
    
    for recipient_email in recipient_list:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        print(f"--- SIMULATING EMAIL SEND to {recipient_email} ---")
        print(f"Subject: {subject}")
        print("Body preview:")
        print(body[:200] + "...")
        print("--------------------------------------------------")
        
        # REAL EMAIL SENDING LOGIC
        try:
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", 587))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            print(f"Email sent successfully to {recipient_email}!")
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", default="dominicrume@gmail.com,rume@ytubebooster.app", help="Comma-separated emails to send the report to")
    parser.add_argument("--strategy", help="Force a specific strategy by name")
    args = parser.parse_args()
    
    kb = load_knowledge_base()
    subject, body = generate_daily_email(kb, force_strategy=args.strategy)
    send_email(subject, body, args.email)

if __name__ == "__main__":
    main()
