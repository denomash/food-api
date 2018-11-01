# app/api/v2/resources/food.py


from flask_restful import Resource, reqparse
import jwt
import re
import psycopg2
import psycopg2.extras
from functools import wraps

# local imports
from ..db import db
from ..checkauth import check_auth


class Menu(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'image',
        type=str,
        required=True,
        help="Image is required"
    )
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

            return {"Meals": meals}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

    @check_auth
    def post(current_user, self):
        """add a food item"""
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}, 401

        data = Menu.parser.parse_args()
        image = data["image"]
        item = data["item"]
        price = data["price"]
        description = data["description"]

        if not image:
            return {'Message': 'Image field is required'}, 400
        if not item:
            return {'Message': 'Food item field is required'}, 400
        if not price:
            return {'Message': 'Price field is required'}, 400
        if not description:
            return {'Message': 'Description field is required'}, 400

        while True:
            if not re.match(r"(^[A-Za-z]+$)", item):
                return {"Message": "Food item must be an alphabet"}, 400
            if not re.match(r"(^[A-Za-z]+$)", description):
                return {"Message": "Food item must be an alphabet"}, 400
            else:
                break
        if type(price) != float:
            return {'Message': 'Price must be an float'}, 400
        if price < 1:
            return{'Message': 'Price must must be more than one'}, 400

        try:
            conn = db()
            cur = conn.cursor()

            cur.execute("SELECT * FROM meals WHERE food = %(food)s",
                        {'food': data['item']})

            # check if order exist
            if cur.fetchone() is not None:
                return {'Message': 'Food already exist'}, 400
            cur.execute("INSERT INTO meals (food, image, price, description) VALUES (%(food)s, %(image)s, %(price)s, %(description)s);", {
                'food': data["item"], 'price': data["price"], 'image': data["image"], 'description': data["description"]})
            conn.commit()
            return {'Message': 'Meal created successfully'}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

class EditMenu(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'image',
        type=str,
        required=True,
        help="Image is required"
    )
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

    @check_auth
    def get(current_user, self, meal_id):
        """get meal by id"""

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * from meals WHERE meal_id = %(meal_id)s",
                        {'meal_id': meal_id})
            meals = cur.fetchall()

            if not meals:
                return {"Meals": "Meal with id does not exist"}, 404

            return {"Meals": meals}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


    @check_auth
    def put(current_user, self, meal_id):
        """add a food item"""
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}, 401

        data = EditMenu.parser.parse_args()
        image = data["image"]
        item = data["item"]
        price = data["price"]
        description = data["description"]

        if not image:
            return {'Message': 'Image field is required'}, 400
        if not item:
            return {'Message': 'Food item field is required'}, 400
        if not price:
            return {'Message': 'Price field is required'}, 400
        if not description:
            return {'Message': 'Description field is required'}, 400

        try:
            conn = db()
            cur = conn.cursor()

            cur.execute("SELECT * FROM meals WHERE meal_id = %(meal_id)s",
                        {'meal_id': meal_id})

            # check if order exist
            if cur.fetchone() is None:
                return {'Message': 'Invalid mealId'}, 400

            cur.execute("UPDATE  meals SET food=%(food)s, image=%(image)s, price=%(price)s, description=%(description)s WHERE meal_id=%(meal_id)s",
                        {'food': item, 'price': price, 'image': image, 'description': description, 'meal_id': meal_id})

            conn.commit()
            return {'Message': 'Meal updated successfully'}, 204
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

    @check_auth
    def delete(current_user, self, meal_id):
        """add a food item"""
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}, 401

        try:
            conn = db()
            cur = conn.cursor()

            cur.execute("SELECT * FROM meals WHERE meal_id = %(meal_id)s",
                        {'meal_id': meal_id})

            # check if order exist
            if cur.fetchone() is None:
                return {'Message': 'Invalid mealId'}, 400

            cur.execute("DELETE FROM meals WHERE meal_id=%(meal_id)s", {
                        'meal_id': meal_id})

            conn.commit()
            return {'Message': 'Meal Deleted successfully'}, 204
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
