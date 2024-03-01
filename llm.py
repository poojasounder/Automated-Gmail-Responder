import os
from vertexai.language_models import TextEmbeddingModel, TextGenerationModel
from langchain_google_vertexai import VertexAI
from dotenv import load_dotenv
from google.cloud import aiplatform
from google.auth import default
load_dotenv()

aiplatform.init(project=os.environ['PROJECT_ID'], location=os.environ['LOCATION'])

# model = TextEmbeddingModel(model_name="gemini-pro", location=LOCATION)

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cs470-rag-llm.json"

# model = TextEmbeddingModel(model_name="gemini-pro")
model = TextGenerationModel.from_pretrained("text-bison@001")

model = VertexAI(model_name="text-bison")

message = "What are some of the pros and cons of Python as a programming language?"
model.invoke(message)