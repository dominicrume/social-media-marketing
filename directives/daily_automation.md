# Directive: Daily 6AM Automated Workflow

**Objective**: Ensure fresh, strategic marketing copies are generated and sent to `rumedominic@gmail.com` every day at 6:00 AM.

## Setup
1. **Install Dependencies**:
   You need the `schedule` library for the 24/7 timing.
   `pip install schedule`

2. **Configure Email**:
   Open `.env` and add your sender details (Gmail App Password recommended):
   ```
   SMTP_EMAIL=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

## Running the Agent
1. **Start the Scheduler**:
   Run the following command in a persistent terminal (or on a server):
   `python3 execution/scheduler_daemon.py`

2. **Process**:
   - The script runs indefinitely.
   - At **06:00 AM**, it triggers `execution/daily_creative_engine.py`.
   - The engine picks a **random strategy** (David vs Goliath, Global South, etc.).
   - It drafts an email with LinkedIn, X, and Video scripts.
   - It sends the email to you.

## Maintenance
- **Adding Fresh Ideas**: Edit `execution/ytb_knowledge.json` and add new entries to the `"strategies"` list. The agent will automatically start using them.
