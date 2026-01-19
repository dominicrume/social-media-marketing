import os
import json
import requests
import ai_refiner

def create_production_brief(narrative_text):
    """
    Uses the AI Brain to convert a text narrative into a full Multi-Media Production Brief.
    Returns: JSON/Dict containing Video Script, Slide Content, and Infographic Prompt.
    """
    prompt = f"""
    ROLE: You are the 'Simera Studio Director'.
    INPUT: A marketing narrative.
    
    TASK: Convert the input into three production assets:
    1. [VIDEO SCRIPT]: 60-second vertical video (Reels/Shorts). visual descriptions + dialogue.
    2. [SLIDE DECK]: 5-Slide Carousel text (Headline + Body for each slide).
    3. [INFOGRAPHIC]: A detailed prompt for a designer/AI to create a viral infographic.
    
    INPUT NARRATIVE:
    {narrative_text}
    
    OUTPUT FORMAT:
    Please provide the output clearly separated by headers:
    === VIDEO SCRIPT ===
    ...
    === SLIDE DECK ===
    ...
    === INFOGRAPHIC ===
    ...
    """
    
    # Reuse the existing AI Refiner's connection to the LLM
    # We pass a 'dummy' strategy name because we just want the raw LLM capability
    print("--- contacting AI Studio Director ---")
    production_assets = ai_refiner.refine_content(narrative_text, "Studio Production Mode", {"voice": {"name": "Studio", "tone": "Visual", "keywords": []}})
    
    return production_assets

def dispatch_to_flock(assets):
    """
    Sends the production brief to a Flock Webhook for human review.
    """
    webhook_url = os.getenv("FLOCK_WEBHOOK_URL")
    
    if not webhook_url:
        print("[WARNING] No FLOCK_WEBHOOK_URL found in .env. Skipping Flock notification.")
        return False
        
    payload = {
        "text": "🚨 **New Simera Production Brief Ready for Review**",
        "attachments": [
            {
                "title": "Production Assets",
                "description": assets,
                "color": "#00FF00"
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Successfully sent to Flock.")
            return True
        else:
            print(f"Failed to send to Flock: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error sending to Flock: {e}")
        return False
