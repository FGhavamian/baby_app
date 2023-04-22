import time

import psycopg2
from psycopg2.extras import RealDictCursor

from .config import settings


while True:
    try:
        conn = psycopg2.connect(
            dbname=settings.database_name,
            user=settings.database_username,
            password=settings.database_password,
            host=settings.database_hostname,
            cursor_factory=RealDictCursor,
        )
        cur = conn.cursor()
        print("Successfully connected to baby")
        break
    except Exception as error:
        print("Failed to connect to baby")
        print("Error:", error)
        time.sleep(2)
