import os
import json
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

def refine_content(draft_text, strategy_name, knowledge_base):
    """
    Sends the raw draft to OpenAI API to be refined by the 'Rume Dominic' persona.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or "sk-" not in api_key:
        return f"[AUTO-REFINER SKIPPED]: No valid OPENAI_API_KEY found in .env.\n\n{draft_text}"

    if OpenAI is None:
        return f"[AUTO-REFINER SKIPPED]: OpenAI library not installed.\n\n{draft_text}"

    client = OpenAI(api_key=api_key)
    
    # Construct the Rume Dominic Persona from your Knowledge Base
    voice = knowledge_base['voice']
    voice_desc = f"{voice['name']}, who is {voice['tone']}."
    keywords = ", ".join(voice['keywords'])
    
    system_prompt = f"""
    You are {voice_desc}
    
    Your Mission: Transform the user's raw marketing draft into a masterpiece of "Digital Sovereignty".
    
    CORE PHILOSOPHY:
    - You hate "generic" marketing.
    - You believe in "Infrastructure", "Assets", and "Ownership".
    - You speak to the "Global South" and the "Underdog".
    - Use these keywords naturally: {keywords}.
    
    TONE GUIDE:
    - Sentences should be punchy. Short.
    - Use the "Rume Dominic Pause" (visual spacing) to create gravity.
    - Never sound like a corporate robot. Sound like a Niche Warlord.
    
    OUTPUT FORMAT:
    - Reshape the content into a Professional LinkedIn Post and a Viral X Thread.
    - Ensure it feels expensive, premium, and authoritative.
    """

    user_prompt = f"""
    Here is the raw draft strategy based on "{strategy_name}".
    Refine this into high-impact social media assets.
    
    RAW DRAFT:
    {draft_text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Using the latest model for best writing
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[AUTO-REFINER FAILED]: {e}\n\n{draft_text}"
