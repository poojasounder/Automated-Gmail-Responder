# Automated Gmail Responder

## Overview
This project aims to automate responses to Gmail emails using Langchain. It utilizes the OpenAI API to generate relevant responses to incoming emails.

## Developers
- Pooja Sounder Rajan
- Ana Macavei
- Josh Li
- Seymour Roberts
- Joseph Nguyen
- Julie Nguyen
- Hilliard Domangue
- Israel Ayala

## Getting Started
To run the project after uploading new documents, follow these steps:

1. Run `python3 ingestion.py`. 
You will be prompted to enter your OpenAI API key.

2. Build the Docker image:
   ```bash
   gcloud builds submit --timeout=900 --tag gcr.io/cs470-rag-llm/capstone
   ```

3. Deploy the Docker image:
    ```bash
    gcloud run deploy capstone <br>   
    --image gcr.io/cs470-rag-llm/capstone</br>
    --min-instances=1</br>
    --memory=1Gi</br> --set-env-vars=OPENAI_API_KEY='YOUR_OPENAI_API_KEY'</br>
    --region=us-west1</br>
    --allow-unauthenticated</br>
    --port=8000
    ```




