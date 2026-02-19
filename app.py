import argparse
import sys
import os
from execution import daily_creative_engine, scheduler_daemon

def print_banner():
    print("""
    ===================================================
       DIGITAL SOVEREIGN AGENT | V2.0 "BILLION DOLLAR"
       -----------------------------------------------
       The Infrastructure for the 100,000,000x Creator
    ===================================================
    """)

def run_daily_cycle(email, strategy=None):
    print(">>> INVOKING DAILY CREATIVE ENGINE...")
    kb = daily_creative_engine.load_knowledge_base()
    subject, body = daily_creative_engine.generate_daily_email(kb, force_strategy=strategy)
    daily_creative_engine.send_email(subject, body, email)
    print(">>> CRITICAL CYCLE COMPLETE.")

def start_daemon():
    print(">>> STARTING PERPETUAL SCHEDULER (24/7)...")
    print(">>> The Agent is now alive. Ctrl+C to stop.")
    scheduler_daemon.start_scheduler()

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Digital Sovereign Marketing App")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: Run Once
    run_parser = subparsers.add_parser("run", help="Run a single marketing cycle instantly")
    run_parser.add_argument("--email", default="dominicrume@gmail.com", help="Target email for the report")
    run_parser.add_argument("--strategy", help="Force a specific strategy (e.g., 'The Apple Store Standard')")

    # Command: Daemon
    daemon_parser = subparsers.add_parser("daemon", help="Start the always-on scheduler")

    args = parser.parse_args()

    if args.command == "run":
        run_daily_cycle(args.email, args.strategy)
    elif args.command == "daemon":
        start_daemon()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
