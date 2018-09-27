# initialize data structure for users
users = list()

# initialize data structure for users
foods = list()

def get_by_id(order_id):
    for order in order_data:
        if order['id'] == order_id:
            return order


def is_empty(value):
    if value:
        return False
    else:
        return True