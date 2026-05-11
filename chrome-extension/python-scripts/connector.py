#! /opt/miniconda3/bin/python3
import sys
import json
import struct
import os
import requests 

from ollama import chat 
# we are using qwen2.5 1.5b in this case because its good to use

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

def process_message(message): 
    # feed job into llm 
    log("processing raw job text with llm")
    
    prompt = f"""
Extract this job posting into valid JSON.

Fields:
- company
- title
- location
- employment_type
- salary
- skills
- benefits
- remote
- description_summary
- job_link (should be a linkedin job post url or a similar url)

Return ONLY valid JSON in text form, do not return markdown, do not return any text other than the JSON.
If missing, use null.

job posting is as follows: \n{message}
"""

    llm_response = chat(
        model="qwen2.5:1.5b",
        messages=[{"role": "user", "content": prompt}],
        format="json"
    )
    
    llm_content = llm_response.message.content
    log(llm_content)
 
    llm_content_json = json.loads(llm_content)
 
    data = {
        "data": {
            "id": "INCREMENT",
            "company": llm_content_json.get("company"),
            "title": llm_content_json.get("title"),
            "location": llm_content_json.get("location"),
            "employment_type": llm_content_json.get("employment_type"),
            "salary": llm_content_json.get("salary"),
            "skills": llm_content_json.get("skills"),
            "benefits": llm_content_json.get("benefits"),
            "remote": llm_content_json.get("remote"),
            "description_summary": llm_content_json.get("description_summary"),
            "job_link": llm_content_json.get("job_link")
        }
    }

    response = requests.post("https://sheetdb.io/api/v1/t4urmwql3pez7", json=data)

    if response.status_code == 201:
        log("Data successfully sent to SheetDB.")
    else:
        log(f"Failed to send data to SheetDB. Status code: {response.status_code}, Response: {response.text}")


    # log(f"LLM response: {llm_response}")


log("--- Script Started ---")

try:
    while True:
        # Wait for message from Chrome
        msg = get_message()
        log(f"Received message of length: {len(str(msg))}")
        log(f"---NEW JOB---")
        log(f"Message content: {msg}")
        log(f"---END OF JOB---")

        # process the message 
        process_message(msg)

        # Simple response back to Chrome
        send_message({"status": "success", "received_len": len(str(msg))})
        log("Response sent to Chrome.")

except Exception as e:
    log(f"CRASH: {str(e)}")
    sys.exit(1)