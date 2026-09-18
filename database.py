import psycopg2
import os

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        conn = psycopg2.connect(database_url)
    else:
        conn = psycopg2.connect(
            dbname="ucsd_clubs",
            user="smritiattam",
            password="",
            host="localhost",
            port="5432"
        )
    return conn
