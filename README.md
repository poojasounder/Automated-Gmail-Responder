# Automated-Gmail-Responder
Application is compatible for both mac and pc

it has been optimized from gemini-pro to gpt-3.5-turbo
## Have a GCP project?
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

## Dependencies
run:
`pip install -r requirements.txt`
`pip install pyhtml2pdf`
`pip install chromadb` 
`pip install pypdf`
`pip install playwright`
`pip install openai`
`pip install langchain-openai`
How to run the project:
first run `python injection.py` this will overwrite any existing scraped and chunked  data
then run `python llm.py`

Tasks:

WUCHANG/ELLA:
- Ask wuchang about publishing the chrome extension: it seems like it takes 24hrs to get approved for 
the chrome extension. OR should he show ella how to upload it from her own local computer? 
- gpt 3.5-turbo works much better but gpt4 will work much better. Is there any way to get to gpt4?
- Ben is working on getting the prompt setup in the front end so that Ella can change the prompt to train the ai.
    - meet with ella to discuss which prompt display she prefers

EDGECASES:
- is it possible to have an option on the extension to add more documents in case the school upgrades their
documents?

BACKEND TEAM:
- organize readme file to guide Ella and her team, and wuchang to use without us successfully.
    - have a step by step guide with screenshots for Ella and her team to set up their environment
    possibly upload updated documents.
    - upload a video on how it works.
- ensure the injection.py and llm.py is working well.
- [PRIORITY] Figure out the docker file to deploy on cloudrun and then update the url to the frontend
- Add comments thoughout the codebase and clean up the codebase. Get rid of whitespace. Make
sure everything is formatted well and follows good coding conventions
- Update the requirements.txt file 

