#app/api/v2/models.py

def get_by_id(order_id):
    for order in order_data:
        if order['id'] == order_id:
            return order


def is_empty(value):
    if value:
        return False
    else:
        return True