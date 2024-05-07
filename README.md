# Automated-Gmail-Responder

To run the project after uploading new documents,

1) python3 ingestion.py
* ## will prompt you for OPENAI API KEY
2) gcloud builds submit --timeout=900 --tag gcr.io/cs470-rag-llm/capstone
3) gcloud run deploy capstone   --image gcr.io/cs470-rag-llm/capstone --min-instances=1 --memory=1Gi --set-env-vars=OPENAI_API_KEY='YOUR_OPENAI_API_KEY' --region=us-west1 --allow-unauthenticated --port=8000




