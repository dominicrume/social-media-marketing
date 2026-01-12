import time
import schedule
import subprocess
import sys
from datetime import datetime

def job():
    print(f"[{datetime.now()}] Waking up Rume's Agent...")
    print(f"[{datetime.now()}] Generating Daily Marketing Packet...")
    
    # Run the generation email script
    try:
        subprocess.run([sys.executable, "execution/daily_creative_engine.py"], check=True)
        print(f"[{datetime.now()}] Packet Delivered.")
    except subprocess.CalledProcessError as e:
        print(f"Error running job: {e}")

def main():
    print("Starting YTB Pro 'Digital Sovereign' Scheduler 24/7...")
    print("Target Time: 06:00 AM daily.")
    
    # Schedule the job for 6:00 AM everyday
    schedule.every().day.at("06:00").do(job)
    
    # ALSO RUN ONCE IMMEDIATELY FOR TESTING
    print("Running immediate test batch...")
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
