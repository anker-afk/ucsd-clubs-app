import psycopg2
from psycopg2 import pool
from contextlib import contextmanager

_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=2,
    maxconn=10,
    dbname="ucsd_clubs",
    user="smritiattam",
    password="",
    host="localhost",
    port="5432"
)

@contextmanager
def get_db():
    conn = _pool.getconn()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)
