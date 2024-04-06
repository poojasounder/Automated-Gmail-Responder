from fastapi import APIRouter, status
from api.models import QA, Document
from services.llm import answer_question, add_embeddings

router = APIRouter(prefix="/api", tags=["v1"])

@router.get("", status_code=status.HTTP_200_OK)
def get_answer(question: QA):
    question.answer = answer_question(question.question)
    return question

@router.post("", status_code=status.HTTP_201_CREATED)
def create_embeddings(document: Document):
    add_embeddings(document)
    return document


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_vector_store():
    # TODO: Implement feature to remove all data from vector store
    pass