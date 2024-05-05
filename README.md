# Automated-Gmail-Responder

## Have a GCP project?
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

gcloud builds submit --timeout=900 --tag gcr.io/cs470-rag-llm/capstone
gcloud run deploy capstone   --image gcr.io/cs470-rag-llm/capstone   --service-account pdx-askcs-website@cs470-rag-llm.iam.gserviceaccount.com --set-env-vars OPENAI_API_KEY=sk-proj-qNNVaH64tadkLv5LPaMgT3BlbkFJaxHh3EboeB99Xjc6BTcj

