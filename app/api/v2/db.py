# app/api/v2/db.py

import psycopg2
import os

# local imports
from .fastfood import queries

def db():

    url = os.getenv('DATABASE_URL')

    # connect using psycopg2
    conn = psycopg2.connect(url)

    return conn

def init_db():

    try:
        connection = db()
        connection.autocommit = True

        # activate connection cursor
        cur = connection.cursor()
        for query in queries:
            cur.execute(query)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database not connected")
        print(error)
