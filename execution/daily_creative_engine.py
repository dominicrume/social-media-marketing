import argparse
import json
import smtplib
import random
import os
import datetime
import shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import viral_lab
import ai_refiner
import simera_brain
import studio_production

# Manual .env loader
def load_env_manual():
    env_paths = [".env", "../.env", "execution/.env"]
    for env_path in env_paths:
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"): continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        value = value.strip().strip("'").strip('"')
                        os.environ[key.strip()] = value
            break

load_env_manual()

# Load Knowledge Base
def load_knowledge_base(path="execution/ytb_knowledge.json"):
    if not os.path.exists(path) and os.path.exists("execution/ytb_knowledge.json"):
        path = "execution/ytb_knowledge.json"
    elif not os.path.exists(path) and os.path.exists("ytb_knowledge.json"):
        path = "ytb_knowledge.json"
    with open(path, 'r') as f:
        return json.load(f)

# LOGIC: HISTORY TRACKING
HISTORY_FILE = "execution/history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history[-7:], f)

def remix_content(body, strategy_name):
    """
    Locally remixes the content if AI fails, ensuring uniqueness.
    """
    clean_body = body.replace("[AUTO-REFINER FAILED]", "").replace("[AUTO-REFINER SKIPPED]", "")
    
    headers = [
        f"--- TACTICAL BRIEFING: {strategy_name.upper()} ---",
        f"--- INFRASTRUCTURE UPDATE: {datetime.date.today()} ---",
        f"--- MARKET SIGNAL DETECTED: {strategy_name} ---",
        "--- CLASSIFIED STRATEGY PACKET ---"
    ]
    
    closers = [
        "Execute immediately.",
        "The market waits for no one.",
        "Build the engine.",
        "Data over feelings."
    ]
    
    header = random.choice(headers)
    closer = random.choice(closers)
    
    # Substitution
    flavor_map = {
        "Digital Sovereign": ["Digital Warlord", "Niche Architect", "Media Baron"],
        "marketing packet": ["growth protocol", "domination blueprint", "tactical asset"],
        "Rume,": ["Agent Rume,", "Commander,", "Rume (Action Required),"]
    }
    
    remixed = clean_body
    for key, variants in flavor_map.items():
        if key in remixed:
            remixed = remixed.replace(key, random.choice(variants), 1)
            
    return f"{header}\n\n{remixed}\n\n>> COMMAND: {closer}"

def generate_daily_email(kb, force_strategy=None):
    history = load_history()
    recent_strategies = [entry.get('strategy') for entry in history]
    recent_tools = [entry.get('tool') for entry in history]

    # Pick a random tool/pain point
    available_items = [i for i in kb['mappings'] if i['tool_name'] not in recent_tools]
    if not available_items:
        available_items = kb['mappings']
    item = random.choice(available_items)

    # Pick a random strategy
    if force_strategy:
        strategy = next((s for s in kb['strategies'] if s['name'] == force_strategy), None)
    else:
        available_strategies = [s for s in kb['strategies'] if s['name'] not in recent_strategies]
        if not available_strategies:
            available_strategies = kb['strategies']
        strategy = random.choice(available_strategies)
    
    subject = f"DAILY STRATEGY: {strategy['name']} ({datetime.date.today()})"
    
    # Reddit Logic
    viral_report = ""
    if strategy['name'] == "The Reddit Detective":
        real_data_path = "execution/real_reddit_data.json"
        if os.path.exists(real_data_path):
            with open(real_data_path, 'r') as f:
                r_sim = json.load(f)
            print(f"--- USING REAL REDDIT DATA: {r_sim['title']} ---")
            item['pain_point'] = r_sim.get('pain_id', item['pain_point'])
            
            archive_dir = "execution/archive"
            if not os.path.exists(archive_dir): os.makedirs(archive_dir)
            shutil.move(real_data_path, f"{archive_dir}/reddit_{datetime.date.today()}.json")
        else:
            r_sim = random.choice(kb.get('reddit_simulations', []))
        viral_report = viral_lab.generate_viral_ideas(r_sim.get('pain_id', 'trends'), item['tool_name'], r_sim)
    else:
        viral_report = f"VIRAL LABS REPORT:\nFocus: {item['pain_point']}\nTool: {item['tool_name']}"

    # Simera Logic
    simera = simera_brain.SimeraContentMachine()
    details_narrative = simera.generate_narrative(item['tool_name'], item['pain_point'], platform="Reddit")
    linkedin_narrative = simera.generate_narrative(item['tool_name'], item['pain_point'], platform="LinkedIn")
    
    raw_body = f"""
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
    """

    # --- AI REFINEMENT STEP ---
    print("--- REFINING CONTENT WITH AI ---")
    refined_body = ai_refiner.refine_content(raw_body, strategy['name'], kb)
    
    final_body = refined_body
    
    # Check for Failures (Quota or Key)
    if "[AUTO-REFINER" in refined_body:
        print("AI Refiner Failed/Skipped. Engaging Local Remix Protocol.")
        final_body = remix_content(raw_body, strategy['name'])
        
        # Add system note at the very end
        final_body += f"\n\n[SYSTEM ALERT: OpenAI Quota Exceeded or Key Missing. Content generated in Offline Mode.]"

    print("--- Generating Multimedia Assets (Studio Mode) ---")
    production_brief = studio_production.create_production_brief(final_body)
    
    print("--- Dispatching to Flock for Human Review ---")
    studio_production.dispatch_to_flock(production_brief)
    
    email_content = f"""
    Rume,
    
    Here is your "Digital Sovereign" Strategy Packet.
    
    =========================================
    PART 1: STRATEGY & NARRATIVE
    =========================================
    {final_body}
    
    =========================================
    PART 2: STUDIO PRODUCTION BRIEF
    (Generated for Video, Slides, and Design Team)
    =========================================
    {production_brief}
    
    -------------------------------------------------------
    [SYSTEM STATUS]
    - Strategy: {strategy['name']}
    - Narrative Engine: Simera Brain + AI Refiner (Status: {'OFFLINE' if '[AUTO-REFINER' in refined_body else 'ONLINE'})
    - Production Brief: Generated
    - History: Updated
    """
    
    # Update History
    history.append({
        'date': str(datetime.date.today()),
        'strategy': strategy['name'],
        'tool': item['tool_name']
    })
    save_history(history)
    
    return subject, email_content

def send_email(subject, body, recipients):
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
    
    # Save to file for User Review
    with open("today_generated_content.md", "w") as f:
        f.write(f"# {subject}\n\n{body}")
        
    send_email(subject, body, args.email)

if __name__ == "__main__":
    main()
