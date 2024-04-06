import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERVER = os.getenv("SERVER")


def post_request(doc_name: str, doc_type):
    payload = dict({"value": doc_name, "doc_type": doc_type})
    response = requests.post(SERVER, json=payload)
    return response.json()

def get_request(question: str):
    payload = {"question": question, "answer": ""}
    response = requests.get(SERVER, json=payload)
    return response.json()

if __name__ == "__main__":
    # Note: cannot add same document twice to the vector store so 
    # comment this part out the post request once you already have
    # the vector store initialized
    doc_name = "FAQ.pdf"
    doc_type = "PDF"
    response = post_request(doc_name, doc_type)
    print(response)

    # change the question to ask the API different questions
    question = "I submitted the application when can I expect to receive a decision?"
    response = get_request(question)
    print(response)