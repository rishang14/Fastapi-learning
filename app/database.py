import os
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

DB_URL = (
    f"host={os.getenv('DB_HOST', 'localhost')} "
    f"dbname={os.getenv('DB_NAME', 'fastapi')} "
    f"user={os.getenv('DB_USER', 'postgres')} "
    f"password={os.getenv('DB_PASSWORD', 'password')}"
)

# Created once at startup — like Prisma's PrismaClient()
# minconn=2: keeps 2 connections always open
# maxconn=10: never opens more than 10 at once
connection_pool: pool.ThreadedConnectionPool = None


def init_pool():
    global connection_pool
    connection_pool = pool.ThreadedConnectionPool(minconn=2, maxconn=10, dsn=DB_URL, cursor_factory=RealDictCursor)


def init_db():
    conn = connection_pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
            """
        )
        conn.commit()
        cur.close()
    finally:
        connection_pool.putconn(conn)


def get_db():
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)
