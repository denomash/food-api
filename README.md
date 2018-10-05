# fast-food-fast api

[![Build Status](https://travis-ci.org/denomash/food-api.svg?branch=ft-place-new-order-route-%23160364056)](https://travis-ci.org/denomash/food-api) [![Coverage Status](https://coveralls.io/repos/github/denomash/food-api/badge.svg?branch=ch-add-tests-160767809)](https://coveralls.io/github/denomash/food-api?branch=ch-add-tests-160767809) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/e0132b28a0ae4584af6057af6a8abd08)](https://www.codacy.com/app/denomash/food-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=denomash/food-api&amp;utm_campaign=Badge_Grade)


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

# VERSION 1

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


# VERSION 2

## Auth

|   # Endpoint          |  # Methods | # Description       |
| -------------         |----------- | ------------------  | 
|`/api/v2/auth/signup`  |   POST     |  registers a user   |
| ------------          | ---------- | -----------------   |
|`/api/v2/auth/login`   |   POST     |  signs in a user    |
|--------------         |----------- | -----------------   |

## Endpoints

|      # Endpoint              | # Methods  |  # Description      | #  Auth type      |
| ------------------------     |----------- | ------------------  | ----------------- | 
|   `/api/v2/menu`             |   GET      |  gets all meals     |     Public        |
| ------------------------     | ---------- | -----------------   | ----------------- |
|   `/api/v2/menu`             |   POST     | posts a new meal    |     Admin         |
| ------------------------     |----------- | -----------------   | ----------------- |
|  `/api/v2/users/orders`      |   POST     | user posts an order |     Client        |
| ------------------------     |----------- | -----------------   | ----------------- |
|  `/api/v2/users/orders`      |   GET      | get user history    |     Client        |
| ------------------------     |----------- | -----------------   | ----------------- |
| `/api/v2/orders/<orderId>`   |   GET      | get user order by id|     Admin         |
| ------------------------     |----------- | -----------------   | ----------------- |
| `/api/v2/orders/<orderId>`   |   PUT      | edit order status   |     Admin         |
| ------------------------     |----------- | -----------------   | ----------------- |
| `/api/v2/orders`             |   Get      | get all orders      |     Admin         |
| ------------------------     |----------- | -----------------   | ----------------- |
| `/api/v2/promote/<orderId>`  |   PUT      | edit user role      |     Admin         |
| ------------------------     |----------- | -----------------   | ----------------- |
| `/api/v2/api/v2/users`       |   GET      | get all users       |     Admin         |

## API DOCUMENTATION

[Apiary Docs](https://foodapiv2.docs.apiary.io/#)

## HEROKU LINK

[Heroku Api](https://fast-food--app-v2.herokuapp.com)

## Author

Dennis Macharia