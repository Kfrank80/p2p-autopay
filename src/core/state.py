import json
import os

class OrderState:
    def __init__(self, key_func=lambda o: o['adv']['advNo'], persist_path=None):
        self.key_func = key_func
        self.persist_path = persist_path
        self.last_ids = set()

        if self.persist_path and os.path.exists(self.persist_path):
            try:
                with open(self.persist_path, 'r', encoding='utf-8') as f:
                    self.last_ids = set(json.load(f))
            except Exception:
                self.last_ids = set()

    def update(self, orders):
        new_ids = {self.key_func(order) for order in orders}
        added = new_ids - self.last_ids
        self.last_ids = new_ids
        if self.persist_path:
            self._persist()
        return added

    def _persist(self):
        try:
            with open(self.persist_path, 'w', encoding='utf-8') as f:
                json.dump(list(self.last_ids), f, ensure_ascii=False, indent=2)
        except Exception:
            pass