import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession
from langchain_google_vertexai import VertexAI  # type: ignore



# TODO(developer): Update and un-comment below lines
project_id = "cs470-rag-llm"
location = "us-central1"
vertexai.init(project=project_id, location=location)

model = VertexAI(model_name="gemini-pro")

message = "What are some of the pros and cons of Python as a programming language?"
#model.invoke(message)

print(model.invoke(message))
''' chat = model.start_chat()

def get_chat_response(chat: ChatSession, prompt: str):
    response = chat.send_message(prompt)
    return response.text

prompt = "Hello."
print(get_chat_response(chat, prompt))

prompt = "What are all the colors in a rainbow?"
print(get_chat_response(chat, prompt))

prompt = "Why does it appear when it rains?"
print(get_chat_response(chat, prompt)) '''