# app/api/v2/db.py

import psycopg2
import psycopg2.extras
import os
from werkzeug.security import generate_password_hash

# local imports
from .fastfood import queries, drop
from config import configuration


def connect_to(url):
    conn = psycopg2.connect(url)
    return conn


def db():

    url = configuration[os.getenv('APP_CONFIG')].DATABASE_URL

    # connect using psycopg2
    conn = connect_to(url)

    return conn


def init_db():

    try:
        connection = db()
        connection.autocommit = True
        teardown()

        # activate connection cursor
        cur = connection.cursor()

        for query in queries:
            cur.execute(query)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        conn = db()
        cur = conn.cursor()
        print("Database not connected")
        print(error)


def test_db():

    try:
        connection = db()
        connection.autocommit = True
        teardown()

        # activate connection cursor
        cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        for query in queries:
            cur.execute(query)
        hashed_password = generate_password_hash(
            'aA123456', method='sha256')
        cur.execute("INSERT INTO users (email, username, type, password) VALUES (%(email)s, %(username)s, %(type)s, %(password)s);", {
            'email': 'admin@gmail.com', 'username': 'admin', 'type': 'admin', 'password': hashed_password})
        connection.commit()
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        conn = db()
        cur = conn.cursor()
        print("Database not connected")
        print(error)


def teardown():

    try:
        connection = db()
        connection.autocommit = True

        # activate connection cursor
        cur = connection.cursor()
        for table in drop:
            cur.execute(table)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        conn = db()
        cur = conn.cursor()
        print("Database not connected")
        print(error)
