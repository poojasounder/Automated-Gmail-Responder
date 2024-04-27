# Automated-Gmail-Responder

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
- Ask wuchang about publishing the chrom extension: it seems like it take 24hrs to get approved for 
the chrom extension. OR should he show ella how to upload it from her own local computer.
- gpt 3.5-turbo works much better but gpt4 will work much better.
- Ben is working on getting the prompt setup in the front end so that Ella can change the prompt to train the ai.
    - meet with ella to discuss which prompt display she prefers

EDGECASES:
- is it possible to have an option on the extension to add more documents in case the school upgrades their
documents?

BACKEND TEAM:
- organize readme file to guide Ella and her team, and wuchang to use without us successfully.
- ensure the injection.py and llm.py is working well.
- add what's in ana_chroma branch to the main. DO NOT MERGE. Just add the necessary code.
- get code from data branch to update the scraping of the bulletin 
- update the code to get all the urls (Pooja just needs to push up her branch)
- figure out the docker file to deploy on cloudrun and then update the url to the frontend
- Add comments thoughout the codebase and clean up the codebase. Get rid of whitespace. Make
sure everything is formatted well and follows good coding conventions
- Update the requirements.txt file 

