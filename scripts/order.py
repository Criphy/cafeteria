from foods import Food


class Order:
    _order: list[Food]

    def __init__(self, *foods):
        self._order = foods

    def getOrder(self, isStr=False):
        if isStr:
            text = ""
            for n, f in enumerate(self._order):
                if n + 1 == len(self._order):
                    text += f"{n + 1}. {f.getName()}."
                else:
                    text += f"{n + 1}. {f.getName()}, "
            return text
        else:
            return self._order

    def removeFood(self, _index):
        del self._order[_index]
