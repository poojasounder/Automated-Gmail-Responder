#!/bin/bash

# Run injection.py
python ingestion.py &

# Start FastAPI with uvicorn
uvicorn llm:app --reload