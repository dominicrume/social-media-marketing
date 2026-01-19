import datetime

class SimeraContentMachine:
    def __init__(self):
        self.brand_voice = "Elite British-Nigerian / Rume Dominic"
        self.price_point = "$9.99"
        self.competitor_price = "$50.00"
        self.target_market = "Global South / Africa & Asia"
        
    def get_market_context(self):
        """Identifies the 'Data Insight' pain points."""
        return {
            "pain": "Growth without data is just gambling. It's risky.",
            "transformation": "Turn your intuition into precision.",
            "v2_update": "Strategic. Intelligent. Risk-Averse Growth."
        }

    def generate_narrative(self, tool_name, problem_type, platform="Reddit"):
        """
        Generates a narrative based on Strategic Excellence, Data Empathy, and Rapid (Safe) Growth.
        """
        context = self.get_market_context()
        
        # Story Logic: The Empathetic Strategist (Understanding the User)
        story = f"""
        TITLE: Stop Gambling with Your Career. Start Engineering It.
        
        NARRATIVE:
        We don't believe in "hustle". We believe in intelligence.
        The biggest risk to your channel isn't "bad content"—it's blindness.
        
        You are trying to thrive, but you are flying without instruments. 
        That isn't brave. It's dangerous.
        
        The {tool_name} was built because we understand that fear.
        We analyzed the data. We saw where you were crashing.
        
        This isn't just a tool; it is your safety net.
        It allows you to fail rapidly in simulation, so you succeed publicly in reality.
        
        {context['v2_update']}
        Understand your audience before you even hit record.
        Grow strategically. Remove the risk.
        """
        
        if platform == "LinkedIn":
             story = f"""
             HEADLINE: Excellence is not an accident. It is a system.
             
             Most creators think growth is luck.
             We know it is data.
             
             We see you trying to scale, but you are carrying the weight of uncertainty.
             "Will this video flop?"
             "Is this title right?"
             
             We built the {tool_name} to answer those questions for you.
             To remove the risk. To let you thrive without the anxiety of guessing.
             
             True strategy is risk-averse. It is calculated.
             
             Use our data to understand your audience deeper than they understand themselves.
             That is how you win. Rapidly.
             
             YTB Pro V2.0.
             Strategic Infrastructure for the Serious Creator.
             """
             
        return story
