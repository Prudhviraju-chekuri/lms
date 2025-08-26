from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, psycopg2

app = FastAPI()

# Allow only your frontend origin
origins = [
    "http://20.66.106.206",  # React frontend LB
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # or ["*"] to allow all (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE...
    allow_headers=["*"],        # Authorization, Content-Type...
)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

@app.get("/")
def root():
    return {"message": "Python backend running!"}

@app.get("/health")
def health():
    try:
        conn = get_connection(); conn.close()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
