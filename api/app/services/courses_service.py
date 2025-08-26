import psycopg2
import os
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_all_courses():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM "Course";')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
