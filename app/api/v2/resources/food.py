# app/api/v2/resources/food.py


from flask_restful import Resource, reqparse
import jwt
import psycopg2
import psycopg2.extras
from functools import wraps

# local imports
from ..db import db
from ..checkauth import check_auth


class Menu(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'item',
        type=str,
        required=True,
        help="Food item is required"
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="Price is required"
    )
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help="Description is required"
    )

    def get(self):
        """get all foods"""

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * from meals")
            meals = cur.fetchall()

            if not meals:
                return {"Meals": "No meals found"}, 404

            return {"Meals": meals}
        except (Exception, psycopg2.DatabaseError) as error:
            cur = conn.cursor()
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

    @check_auth
    def post(current_user, self):
        """add a food item"""
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}

        data = Menu.parser.parse_args()
        item = data["item"]
        price = data["price"]
        description = data["description"]

        if not item:
            return {'Message': 'Food item field is required'}, 400
        if not price:
            return {'Message': 'Price field is required'}, 400
        if not description:
            return {'Message': 'Description field is required'}, 400

        try:
            conn = db()
            cur = conn.cursor()

            cur.execute("SELECT * FROM meals WHERE food = %(food)s",
                        {'food': data['item']})

            # check if order exist
            if cur.fetchone() is not None:
                return {'Message': 'Food already exist'}
            cur.execute("INSERT INTO meals (food, price, description) VALUES (%(food)s, %(price)s, %(description)s);", {
                'food': data["item"], 'price': data["price"], 'description': data["description"]})
            conn.commit()
            return {'Message': 'Meal created successfully'}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
