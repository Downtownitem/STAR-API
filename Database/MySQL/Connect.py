import json

import pymysql
import dotenv
import os
from typing import Optional

dotenv.load_dotenv()

conn: Optional[pymysql.Connection] = None


def connect():
    global conn
    if conn is None:
        cert_path = os.path.join(os.path.dirname(__file__), 'cacert.pem')
        keys_path = os.path.join(os.path.dirname(__file__), 'keys.json')

        with open(keys_path, 'r') as f:
            keys = json.load(f)

        try:
            conn = pymysql.connect(
                host=keys['DATABASE_HOST'],
                database=keys['DATABASE_NAME'],
                user=keys['DATABASE_USER'],
                password=keys['DATABASE_PASSWORD'],
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
