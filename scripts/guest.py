from order import Order


class Guest:
    name: str
    order: Order

    def __init__(self, _name, _order):
        self.name = _name
        self.order = _order

    def getFood(self, _food):
        fids = [f.getOrder() for f in self.order]
        fids = [f.getId() for f in fids]

        for f in range(len(fids)):
            if _food.getId() == fids[f]:
                self.order.removeFood(f)
                return "Блюдо было отдано"
            else:
                return "Это не то блюдо! (нужно: " + self.order.getOrder(True) + ")"
