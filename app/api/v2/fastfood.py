# app/api/v2/fastfood.py

tb1 = """CREATE TABLE if not exists users (
    id bigserial UNIQUE PRIMARY KEY,
    email varchar(50) NOT NULL UNIQUE,
    username varchar(12) NOT NULL UNIQUE,
    type varchar(250) NOT NULL,
    password varchar(250) NOT NULL
    );"""


tb2 = """CREATE TABLE if not exists orders (
    order_id serial UNIQUE PRIMARY KEY,
    user_id INT NOT NULL,
    image text NOT NULL,
    meal_id INT NOT NULL,
    status text NOT NULL,
    address text NOT NULL,
    quantity integer NOT NULL
    );"""

tb3 = """CREATE TABLE if not exists meals (
    meal_id serial UNIQUE PRIMARY KEY,
    food varchar(50) NOT NULL,
    price real NOT NULL,
    image text NOT NULL,
    description text NOT NULL 
    );"""

dt1 = """ DROP TABLE IF EXISTS users CASCADE """
dt2 = """ DROP TABLE IF EXISTS orders CASCADE """
dt3 = """ DROP TABLE IF EXISTS meals CASCADE """

queries = [tb1, tb2, tb3]

drop = [dt1, dt2, dt3]