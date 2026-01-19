import os
import tweepy
from instagrapi import Client as InstaClient
import requests

class SocialDispatcher:
    def __init__(self):
        self.load_credentials()
        self.x_client = None
        self.insta_client = None
        
    def load_credentials(self):
        # Twitter
        self.x_api_key = os.getenv("X_API_KEY")
        self.x_api_secret = os.getenv("X_API_SECRET")
        self.x_access_token = os.getenv("X_ACCESS_TOKEN")
        self.x_access_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        
        # Instagram
        self.insta_user = os.getenv("INSTA_USERNAME")
        self.insta_pass = os.getenv("INSTA_PASSWORD")
        
        # LinkedIn
        self.linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")

    def connect_x(self):
        """Connects to X (Twitter) API v2"""
        try:
            if not self.x_api_key: return False
            self.x_client = tweepy.Client(
                consumer_key=self.x_api_key,
                consumer_secret=self.x_api_secret,
                access_token=self.x_access_token,
                access_token_secret=self.x_access_secret
            )
            return True
        except Exception as e:
            print(f"X Connection Error: {e}")
            return False

    def post_to_x(self, text):
        """Posts a tweet"""
        if not self.x_client and not self.connect_x():
            return "X: Skipped (No Auth)"
        
        try:
            # Split text if longer than 280 chars
            if len(text) > 280:
                text = text[:277] + "..."
            response = self.x_client.create_tweet(text=text)
            return f"X: Success (ID: {response.data['id']})"
        except Exception as e:
            return f"X: Failed ({e})"

    def post_to_linkedin(self, text):
        """Posts to LinkedIn"""
        if not self.linkedin_token: return "LinkedIn: Skipped (No Token)"
        
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self.linkedin_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "author": f"urn:li:person:{self.get_linkedin_id()}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            r = requests.post(url, headers=headers, json=payload)
            if r.status_code == 201:
                return "LinkedIn: Success"
            else:
                return f"LinkedIn: Failed ({r.status_code} - {r.text})"
        except Exception as e:
            return f"LinkedIn: Failed ({e})"

    def get_linkedin_id(self):
        """Helper to get LinkedIn Person ID"""
        url = "https://api.linkedin.com/v2/me"
        headers = {"Authorization": f"Bearer {self.linkedin_token}"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()['id']
        return None

    def dispatch_all(self, content_packet):
        """
        Takes the generated content packet and posts to all connected platforms.
        """
        report = []
        
        # Extract X content (simple logic for now)
        x_content = "Digital Sovereignty. The Wall has Fallen. #YTBPro" # Placeholder extraction
        if "[X / TWITTER THREAD]" in content_packet:
            # Simple extraction logic (improvement needed for robust parsing)
            pass 

        # Extract LinkedIn content
        linkedin_content = "Stop Building on Sand. Build Infrastructure. #YTBPro" # Placeholder
        
        # Execute Posts
        # report.append(self.post_to_x(x_content))
        # report.append(self.post_to_linkedin(linkedin_content))
        
        return "\n".join(report)
