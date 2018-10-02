# app/api/v2/db.py

import psycopg2
import os

# local imports
from .fastfood import queries, drop

def connect_to(url):
    conn = psycopg2.connect(url)
    return conn

def db():

    url = os.getenv('DATABASE_URL')

    # connect using psycopg2
    conn = connect_to(url)

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

def testdb():

    url = os.getenv('TEST_DB_URL')

    # connect using psycopg2
    conn = connect_to(url)

    return conn

def test_db():

    try:
        connection = testdb()
        connection.autocommit = True
        teardown()

        # activate connection cursor
        cur = connection.cursor()
        for query in queries:
            cur.execute(query)
        connection.commit()
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database not connected")
        print(error)

def teardown():

    try:
        connection = testdb()
        connection.autocommit = True

        # activate connection cursor
        cur = connection.cursor()
        for table in drop:
            cur.execute(table)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database not connected")
        print(error)