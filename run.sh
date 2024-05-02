#!/bin/bash

# Run injection.py
python ingestion.py &

# Start FastAPI with uvicorn
uvicorn llm:app --host 0.0.0.0 --port 8080 --reload