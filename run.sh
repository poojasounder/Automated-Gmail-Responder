#!/bin/bash

# Run injection.py
python injection.py &

# Start FastAPI with uvicorn
uvicorn llm:app --reload