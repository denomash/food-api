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

    def get(current_user, self):
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
