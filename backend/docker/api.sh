#!/bin/bash

# Wait for PostgreSQL to be ready
python docker/wait_postgres.py

# Run database migrations
alembic upgrade head

# Start the bot
PYTHONPATH=/app
uvicorn src.main:app --reload --host 0.0.0.0 --port 8080