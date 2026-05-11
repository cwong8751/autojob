from pathlib import Path
from typing import List
from ollama import chat
import json 
import requests 


def read_output_text() -> str:
	return Path(__file__).with_name("output.txt").read_text(encoding="utf-8")


def process_raw_text(raw_text: str) -> List[str]:
	"""Return lines from raw_text that start with 'Message content: ' as a list."""
	return [line for line in raw_text.splitlines() if line.startswith("Message content: ")]


if __name__ == "__main__":
	print("reading raw text from output.txt...")
	raw_text = read_output_text()
	processed_text = process_raw_text(raw_text)
	# print(processed_text)
	print("processing raw text with llm...")

	for text in processed_text:
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

		job posting is as follows: \n{text}
		"""

		llm_response = chat(
			model="qwen2.5:1.5b",
			messages=[{"role": "user", "content": prompt}],
			format="json"
		)

		llm_content = llm_response.message.content
		print(llm_content)

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
			print("Data successfully sent to SheetDB.")
		else:
			print(f"Failed to send data to SheetDB. Status code: {response.status_code}, Response: {response.text}")


		



		


		



	
	
    
	
    

