# core/state.py
class OrderState:
    def __init__(self):
        self.last_order_ids = set()

    def update(self, orders):
        new_ids = {order['adv']['advNo'] for order in orders}
        added = new_ids - self.last_order_ids
        self.last_order_ids = new_ids
        return added
