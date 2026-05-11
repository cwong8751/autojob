## Autojob 

Autojob is a semi-automatic job crawler and applicant system. 

## How does it work
1. you install the autojob chrome extension
2. go on linkedin.com/jobs and look for jobs. 
3. autojob will find job description as well as the apply link (if applicable), save it to a python file, analyze it into a csv file so you can see and apply. 

## Prerequisites 
This project is a complete pipeline that uses javascript, service workers, python, Ollama and Google Sheets to capture linkedin jobs into a presentable google sheets file. 

You need: 

1. This project 
2. Ollama
3. Sheets db 

## Setting up ollama
This project uses the qwen2.5:1.5b model because its small enough and good in terms of context processing and speed. It is mainly used to parse the complex job description scraped from linkedin. 

We will be using the <code>ollama-python</code> library for this. Could be found here: https://github.com/ollama/ollama-python

You also need to install ollama: https://ollama.com/download

After all this, fire up a terminal and type 
```
ollama pull qwen2.5:1.5b
```

then the model should be ready. 

## Setting up sheets db 
Setting up sheets db should be quite simple, first of all you need a sheetsdb account: https://sheetdb.io/

Then head in and create an spreadsheet and link that to sheetsdb. Your spreadsheet should have the following columns for the code to work properly: 

1. id
2. company
3. title
4. location
5. employment_type
6. salary
7. skills
8. benefits
9. remote
10. description_summary
11. job_link 



## installing and Running  
1. download the repo
2. unzip the repo, and rename the bridge.json file to <code>com.autojob.bridge</code> and put it under 
```
/Library/Google/Chrome/NativeMessagingHosts/
```
3. open the bridge.json file and look for this line: 
```
"path": "/Users/carl/Documents/GitHub/autojob/chrome-extension/python-scripts/connector.py",
```
this is supposed to be the path of the ```connector.py``` file under the ```/python-scripts``` folder. Change this to the relevant path on your machine. 

4. open <code>connector.py</code> and find this line: 
```
response = requests.post("https://sheetdb.io/api/v1/t4urmwql3pez7", json=data)
```
replace that sheetdb.io with your own sheetdb.io link. 

3. then open google chrome and go to <code>chrome://extensions</code> and load the "chrome-extension' folder as an extension. 

4. then open linkedin and go search for jobs. 
