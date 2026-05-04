import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="ucsd_clubs",
        user="smritiattam",
        password="",
        host="localhost",
        port="5432"
    )
    return conn