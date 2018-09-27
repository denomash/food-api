# app/api/v2/resources/food.py

from flask_restful import Resource, reqparse
from ..db import db


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
        'image',
        type=str,
        required=True,
        help="Image is required"
    )

    def get(self):
        """get all foods"""

        try:
            conn = db()
            cur = conn.cursor()
            cur.execute("SELECT * from meals")
            meals = cur.fetchall()

            if not meals:
                return {"Meals": "No meals found"}, 404

            return {"Meals": meals}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

    def post(self):

        data = Menu.parser.parse_args()
        item = data["item"]
        price = data["price"]
        image = data["image"]

        if not item:
            return {'Message': 'Food item field is required'}, 400
        if not price:
            return {'Message': 'Price field is required'}, 400
        if not image:
            return {'Message': 'Image field is required'}, 400

        exist = [food for food in foods if food['item'] == data['item']]

        if (len(exist) != 0):

            return {'Message': 'Food item already exist'}, 400

        _id = len(foods) + 1

        new_food = {
            'id': _id,
            'item': data['item'],
            'price': data['price'],
            'image': data['image']
        }

        foods.append(new_food)

        return {'Order': new_food}, 201
