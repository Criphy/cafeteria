class Foods:
    FirstFood = (
        ("Шашлык", "barbeque", 275),
        ("Шавуха", "shaurma", 380),
        ("Суши", "sushi", 460)
    )

    Drinks = (
        ("Кола", "cola", 70),
        ("Апельсиновый сок", "orange_juice", 65),
        ("Кофе", "cofe", 50),
        ("Чай", "tea", 50)
    )

    @property
    def get(self):
        __foods = []
        _foods = []
        for f in [self.FirstFood, self.Drinks]:
            for _f in f:
                __foods.append(_f)

        for f in __foods:
            _foods.append(Food(*f))
        return _foods


class Food:
    name: str
    id: str
    price: int

    def __init__(self, _name, _id, _price):
        self.name = _name
        self.id = _id
        self.price = _price

    @property
    def getName(self):
        return self.name

    @property
    def getId(self):
        return self.id

    @property
    def getPrice(self):
        return self.price
