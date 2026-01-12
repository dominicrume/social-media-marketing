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
        # Or just pick a random one for variety
        r_sim = random.choice(kb.get('reddit_simulations', []))
        viral_report = viral_lab.generate_viral_ideas(r_sim['pain_id'], item['tool_name'], r_sim)
    
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
    
    [LINKEDIN DRAFT]
    Headline: {strategy['hook']} Why {item['pain_point']} is keeping you small.
    
    The giants of the industry are slow. They are expensive.
    You are paying {kb['pricing']['competitor_price']} to fund their overhead.
    
    We built YTubeBooster PRO V2.0 for the builders.
    The {item['tool_name']} isn't just a feature. It's an equalizer.
    
    WHAT IT SOLVES: {item['pain_description']}
    THE FIX: {item['solution_feature']}. 
    
    Join the 10,000 Alpha Leaders.
    {kb['pricing']['price']}. Digital Sovereignty.
    
    #YTBPro #CreatorEconomy
    
    -------------------------------------------------------
    
    [X / TWITTER THREAD]
    1/5
    {strategy['hook']}
    The era of the $50 subscription is over.
    
    2/5
    Legacy tools want you to rent your audience.
    We want you to own your infrastructure.
    
    3/5
    The Pain: {item['pain_point']}
    ("{item['pain_description']}")
    
    4/5
    The Fix: {item['tool_name']}
    {item['solution_feature']}
    
    5/5
    V2.0 is live. Stylish. Futuristic.
    Built for the {strategy['name']} generation.
    Link in bio.
    
    -------------------------------------------------------
    
    [VIDEO SCRIPT CONCEPT]
    Hook: Stare at camera. "{strategy['hook']}"
    Problem: "You are suffering from {item['pain_point']}."
    Agitate: "{item['pain_description']}"
    Solution: Show {item['tool_name']} interface. "This is {item['solution_feature']}."
    CTA: "This is 2.0. {kb['pricing']['price']}."
    
    """
    
    # --- STAGE 2: AI REFINEMENT (The "Rume Dominic" Filter) ---
    print("--- Sending Draft to AI Refiner (OpenAI) ---")
    refined_body = ai_refiner.refine_content(body, strategy['name'], kb)
    
    final_body = f"""
    Rume,
    
    Here is your REFINED "Digital Sovereign" marketing packet.
    (Refined by GPT-4o Persona)
    
    {refined_body}
    
    -------------------------------------------------------
    ORIGINAL DRAFT (For Reference):
    {body}
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
