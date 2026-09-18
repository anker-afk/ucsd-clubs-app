import psycopg2
import os

def get_connection():
    database_url = os.getenv("postgresql://database_zfnc_user:FJpcdf17vVUEesh758yion3f2vUPz7sI@dpg-dam7p6rm8hqs73cqp1l0-a/database_zfnc")
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
