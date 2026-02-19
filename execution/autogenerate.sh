#!/bin/bash

# Navigate to the project directory
cd "/Users/user/Downloads/social media marketing"

# Log the execution time
echo "Starting Daily Content Generation at $(date)" >> execution/cron_log.txt

# Activate the virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "Warning: .venv not found, using system python" >> execution/cron_log.txt
fi

# Run the script
python3 execution/daily_creative_engine.py >> execution/cron_log.txt 2>&1

echo "Finished at $(date)" >> execution/cron_log.txt
echo "---------------------------------------------------" >> execution/cron_log.txt
