import json
import argparse
import sys
import os

def load_knowledge_base(path="execution/ytb_knowledge.json"):
    with open(path, 'r') as f:
        return json.load(f)

def get_mapping(kb, query):
    query = query.lower()
    for item in kb['mappings']:
        if item['pain_point'].lower() in query or item['tool_name'].lower() in query or item['id'] in query:
            return item
    return None

def generate_linkedin(kb, item):
    return f"""
[LINKEDIN POST]
Headline: The Infrastructure of Attention: Why {item['pain_point']} is Costing You Relevance.

We are watching a Digital Dark Age. Creators with gold-standard ideas are being silenced by {kb['pricing']['competitor_price']} walls. 

The industry calls it "{item['pain_point']}". I call it a structural failure.
You are flying without instruments.

The Fix: YTubeBooster PRO {item['tool_name']}.
It is not just a tool; it is your commercial engine. 
Stop guessing. Start dominating.

Version 2.0 is here. Stylish. Futuristic.
Your Digital Passport for {kb['pricing']['price']}.

Join the 10,000 Alpha Leaders.
#YTBPro #DigitalSovereign #CreatorEconomy
"""

def generate_twitter(kb, item):
    return f"""
[X THREAD]
1/5
The $50 wall is crumbling.
Your content isn't bad. Your infrastructure is broken.
You are suffering from "{item['pain_point']}".

2/5
This is the silent killer of the $180B economy.
Legacy tools gatekeep the solution. They want you to pay a premium for basic visibility.

3/5
Enter YTubeBooster PRO V2.0.
The {item['tool_name']} solves this instantly.
{item['solution_feature']}.

4/5
We rebuilt the UI. Stylish. Futuristic. High-speed.
This is the engine for the Global South.

5/5
Claim your Digital Sovereign status.
$9.99 for the entire suite.
Join the 10,000 Alpha Leaders here: [LINK]
"""

def generate_video_script(kb, item):
    return f"""
[VIDEO SCRIPT]
(Scene: Minimalist, high-end studio / Dark mode UI on screen)
(Tone: Rume Dominic - Authoritative, Slow, Intense)

[HOOK]
(Camera zooms in slowly)
Rume: "There is a reason... nobody is watching."
(Pause)
Rume: "It’s not your talent. It’s your {item['pain_point']}."

[WHY]
Rume: "You are trying to win a Formula 1 race... on a bicycle. The $50 tools have priced you out. They created a Digital Dark Age."

[REVEAL]
(Cut to B-Roll of YTB Pro V2.0 Dashboard - Smooth animations)
Rume: "This... is YTubeBooster PRO Version 2.0. Stylish. Futuristic."
Rume: "Use the {item['tool_name']}. Fix the leak. Own the data."

[CTA]
(Rume looks deep into lens)
Rume: "This is your Digital Passport. $9.99."
Rume: "Become a Digital Sovereign. Join the Alpha Leaders."
"""

def main():
    parser = argparse.ArgumentParser(description="Generate YTB Pro 'Digital Sovereign' content.")
    parser.add_argument("--topic", type=str, required=True, help="Tool name, Pain point, or ID (thumbnails, data, seo)")
    args = parser.parse_args()

    kb = load_knowledge_base()
    item = get_mapping(kb, args.topic)

    if not item:
        print(f"Error: Could not find mapping for '{args.topic}'. Available IDs: thumbnails, data, seo", file=sys.stderr)
        sys.exit(1)

    print(f"--- GENERATING CAMPAIGN FOR: {item['pain_point']} / {item['tool_name']} ---\n")
    print(generate_linkedin(kb, item))
    print("-" * 40)
    print(generate_twitter(kb, item))
    print("-" * 40)
    print(generate_video_script(kb, item))

if __name__ == "__main__":
    main()
