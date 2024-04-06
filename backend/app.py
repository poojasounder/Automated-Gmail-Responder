import os
from fastapi import FastAPI
from api.routes import router
from services.llm import add_embeddings, answer_question
from dataclasses import dataclass
from dotenv import load_dotenv


app = FastAPI()
app.include_router(router)
