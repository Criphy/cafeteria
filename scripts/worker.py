import random


class Worker:
    name: str
    category: str

    def __init__(self, _name=None, _category=None):
        self.name = _name if _name else random.choice(["Андрей", "Станислав", "Ярослав", "Анатолий", "Василий"])
        self.category = _category if _category else random.choice(["Помощник", "Шеф-повар", "Повар", "Бармен", "Курьер"])

    def __data__(self):
        return self.name, self.category

    def __str__(self):
        return f"Имя: {self.name}, категория: {self.category}"
