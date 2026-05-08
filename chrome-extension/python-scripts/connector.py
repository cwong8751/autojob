#! /opt/miniconda3/bin/python3
import sys
import json
import struct
import os

# Set up absolute path for logging so you can actually see what's happening
DEBUG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(DEBUG_DIR, "output.txt")

sys.stderr = open(os.path.join(os.path.dirname(__file__), 'stderr.txt'), 'w')

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")

def get_message():
    # Read the first 4 bytes (the length of the message)
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        log("No raw length received. Exiting.")
        sys.exit(0)
    
    message_length = struct.unpack('@I', raw_length)[0]
    
    # Read the actual JSON message
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

def send_message(message_content):
    encoded_content = json.dumps(message_content).encode('utf-8')
    encoded_length = struct.pack('@I', len(encoded_content))
    sys.stdout.buffer.write(encoded_length)
    sys.stdout.buffer.write(encoded_content)
    sys.stdout.buffer.flush()

log("--- Script Started ---")

try:
    while True:
        # Wait for message from Chrome
        msg = get_message()
        log(f"Received message of length: {len(str(msg))}")
        log(f"---NEW JOB---")
        log(f"Message content: {msg}")
        log(f"---END OF JOB---")
        # Simple response back to Chrome
        send_message({"status": "success", "received_len": len(str(msg))})
        log("Response sent to Chrome.")

except Exception as e:
    log(f"CRASH: {str(e)}")
    sys.exit(1)