# fast-food-fast api

[![Build Status](https://travis-ci.org/denomash/food-api.svg?branch=ft-place-new-order-route-%23160364056)](https://travis-ci.org/denomash/food-api) [![Coverage Status](https://coveralls.io/repos/github/denomash/food-api/badge.svg?branch=ft-login-endpoint-%23160611196)](https://coveralls.io/github/denomash/food-api?branch=ft-login-endpoint-%23160611196) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/e0132b28a0ae4584af6057af6a8abd08)](https://www.codacy.com/app/denomash/food-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=denomash/food-api&amp;utm_campaign=Badge_Grade)


## About fast-food-fast api
This is an api for ordering fast food.

**Requirements**
* python 3.6
* pip
* virtualenv
* virtualenvwrapper
* postman

 
# How to install and use the api

## Installation
From the reminal clone the repository by running:


`git clone https://github.com/denomash/food-api.git`

Switch to the develop branch and run:


`git fetch origin develop`

Navigate into the folder by running:


`cd food-api`

create a virtual environment by running:


`mkvirtualenv env`

then run:


`workon env`

Install required packages:


`pip install -r requirements.txt`

Then run(each at a time):


`export APP_CONFIG=development`
`export FLASK_APP=run.py`
`flask run`

How to test:


RUN `pytest --cov=app/tests/`

Then use postman to test the following endpoints:

|   # Endpoint       |  # Methods | # Description       |
| -------------      |----------- | ------------------  | 
|`/api/v1/orders`    |   GET      |  gets all orders    |
| ------------       | ---------- | -----------------   |
|`/api/v1/orders`    |   POST     | posts a new order   |
|--------------      |----------- | -----------------   |
|`/api/v1/order/<id>`|   GET      |gets an order by id  |
|--------------      |----------- | -----------------   |
|`/api/v1/order/<id>`|   PUT      |updates order by id  |
|--------------      |----------- | -----------------   |
|`/api/v1/order/<id>`|   DELETE   |deletes order by id  |
|--------------      |----------- | -----------------   |
|`/api/v1/signup`    |   POST     |signs up a user      |
|--------------      |----------- | -----------------   |
|`/api/v1/login`     |   POST     |logs in a user       |