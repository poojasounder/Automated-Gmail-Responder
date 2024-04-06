from pydantic import BaseModel
from enum import Enum, auto

# class DocumentType(Enum):
#     '''Document type enum'''
#     URL = "URL"
#     PDF = "PDF"
#     TEXT = "TEXT"

class QA(BaseModel):
    '''QnA model'''
    question: str
    answer: str

class Document(BaseModel):
    '''Document model'''
    value: str
    doc_type: str


