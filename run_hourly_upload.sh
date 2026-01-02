#!/bin/bash
# run_hourly_upload.sh
# Safe cron wrapper to run AI reel generator once every 3 days

# -----------------------------------
# ENVIRONMENT FIXES (cron-safe)
# -----------------------------------

# Ensure Homebrew tools (ffmpeg, imagemagick) are found
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Ensure HOME is set
export HOME="/Users/navneetkumar"

PROJECT_DIR="/Users/navneetkumar/ai_reels_generator"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/hourly_upload.out.log"

# -----------------------------------
# SAFETY GUARD: run once every 3 days
# -----------------------------------

STAMP_FILE="$PROJECT_DIR/.last_run"
NOW=$(date +%s)
LAST_RUN=0

if [ -f "$STAMP_FILE" ]; then
  LAST_RUN=$(cat "$STAMP_FILE")
fi

# 3 days = 259200 seconds
if [ $((NOW - LAST_RUN)) -lt 259200 ]; then
  exit 0
fi

# Record new run timestamp
echo $NOW > "$STAMP_FILE"

# -----------------------------------
# SETUP
# -----------------------------------

# Ensure logs directory exists
mkdir -p "$LOG_DIR"

# Move to project directory
cd "$PROJECT_DIR" || exit 1

# Activate virtualenv
source "$PROJECT_DIR/venv/bin/activate"

# -----------------------------------
# RUN PIPELINE
# -----------------------------------

echo "======================================" >> "$LOG_FILE"
echo "Run started at: $(date)" >> "$LOG_FILE"

python3 main.py >> "$LOG_FILE" 2>&1

echo "Run finished at: $(date)" >> "$LOG_FILE"
echo "======================================" >> "$LOG_FILE"
