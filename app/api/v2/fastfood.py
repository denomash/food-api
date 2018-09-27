

tb1 = """CREATE TABLE if not exists users (
    id bigserial UNIQUE PRIMARY KEY,
    email varchar(50) NOT NULL UNIQUE,
    username varchar(12) NOT NULL UNIQUE,
    type varchar(250) NOT NULL,
    password varchar(250) NOT NULL,
    confirm_password varchar(1000) NOT NULL
    );"""


tb2 = """CREATE TABLE if not exists orders (
    order_id serial UNIQUE PRIMARY KEY,
    user_id INT NOT NULL,
    food varchar(50) NOT NULL,
    status text NOT NULL, 
    price real NOT NULL,
    address text NOT NULL ,
    quantity integer NOT NULL,
    description text NOT NULL 
    );"""

tb3 = """CREATE TABLE if not exists meals (
    meal_id serial UNIQUE PRIMARY KEY,
    food varchar(50) NOT NULL,
    price real NOT NULL,
    description text NOT NULL 
    );"""


queries = [tb1, tb2, tb3]
