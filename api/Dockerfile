FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose whatever port is defined by PORT env variable (optional, just for docs)
EXPOSE ${PORT}

# Use shell form so environment variables are expanded at runtime
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}