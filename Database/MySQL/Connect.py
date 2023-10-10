import dotenv
import pymysql
import os
from typing import Optional

dotenv.load_dotenv()

conn: Optional[pymysql.Connection] = None


def connect():
    global conn
    if conn is None:
        cert_path = os.path.join(os.path.dirname(__file__), 'cacert.pem')

        try:
            conn = pymysql.connect(
                host=os.getenv('DATABASE_HOST'),
                database=os.getenv('DATABASE_NAME'),
                user=os.getenv('DATABASE_USER'),
                password=os.getenv('DATABASE_PASSWORD'),
                ssl_ca=cert_path
            )
            print(f"Connection established to database: {conn}")
        except Exception as e:
            print("Error while connecting to MySQL", e)


def get_connection() -> pymysql.Connection:
    return conn


def close_connection():
    global conn
    if conn is not None:
        conn.close()
        conn = None
