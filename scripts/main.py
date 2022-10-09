#!usr/bin/python
import os
import random
import sys
import time
from psycopg2 import connect
from threading import Thread
from cafe import Cafe
from worker import Worker
from foods import Foods
from order import Order
from guest import Guest
from rich import console

# База данных
connector = connect(host="ec2-52-4-87-74.compute-1.amazonaws.com",
                    port=5432,
                    dbname="d6u1t52riap10s",
                    user="ypqjpfarvdrnyx",
                    password="c1a2429d0b66635c565704de1a3e7a4b0553ba0d1cea64f0455b50cc4947cf21")
connector.autocommit = True
cursor = connector.cursor()

# Консоль
_console = console.Console()
__version__ = "1.0.0"
__system__ = sys.platform

# Пользовательские параметры
pid: str = ""
_cafe: Cafe = None
_foods = Foods().get
_guests = []
isCafeClosed = True


def __credits__():
    _console.clear()
    _console.print("ОБ ИГРЕ", style="green bold", justify="center")
    _console.print("Эта \"игра\" была создана одним человеком под ником Cr1phy. Первоначально, я создал эту игру на языке программирования Python. Чтобы выглядело красиво (извиняюсь за выражение, \"ах*енно\"), мне пришлось установить библиотеку [code]rich[/code]. Логотип я делал с помощью сайта, который делает баннеры (забыл название). Присутствует многопоточность (библиотека [code]threading[/code])",
                   style="cyan")
    _console.print("\n«Мне было нехер делать, так как идей было мало. Вот и решил я это сделать.» - Cr1phy.", style="cyan bold", justify="center")
    _console.input()


def guests():
    global isCafeClosed
    while not isCafeClosed:
        time.sleep(5)
        if len(_guests) <= 5:
            _console.bell()
            _order = Order(random.choice(_foods), random.choice(_foods))
            _guest = Guest("Алексей", _order)
            _guests.append(_guest)
            _console.set_window_title(f"Cafeteria {__version__} ({len(_guests)} клиент.)")


def createCafe():
    title = input("Дайте название своему заведению: ")
    cafe = Cafe()
    cafe.setTitle(title)
    firstworker = Worker()
    cafe.addWorker(firstworker)
    _console.print(f"Хорошо. Теперь у вас есть рабочий.\n- Данные: {firstworker.__str__()}", style="green")
    return cafe


def loadCafe(data):
    _title = data["title"]
    _level = data["level"]
    _workers = [w for w in data["workers"]]
    _workers = [Worker(w[0], w[1]) for w in _workers]
    cafe = Cafe()
    cafe.__from_json__(_title, _level, _workers)
    return cafe


def getInfo():
    _console.clear()
    c = _cafe.__data__()
    title, level, workers = c

    info = f"Название -> \"{title}\"\nУровень -> {level}\nВсего работников -> {len(workers)}"
    _console.print(info, style="cyan")
    _console.input()


def _cooking(num: int):
    if 1 <= num <= len(_foods):
        food = _foods[num - 1]
        print(food)
    else:
        raise IndexError("Не существует такой еды!")


def cook():
    while True:
        _console.print("Что вы хотите приготовить?", style="green bold")
        for x, f in enumerate(_foods):
            _console.print(f"{x + 1}. {f.getName} ({f.getPrice} руб.)", style="cyan")
        _console.print("0. Выйти", style="cyan")
        answer = input(">>> ")
        try:
            if answer == "0":
                break
            _cooking(int(answer))
        except Exception as e:
            _console.print(f"Произошла ошибка. ({e})", style="red bold")


def addWorkers():
    _ws = []
    for x in range(10):
        _w = Worker()
        _ws.append(_w)

    while True:
        _console.clear()
        _console.print("Cписок людей, которые хотят обустроиться на работу.", style="green bold", justify="center")
        if len(_ws) < 1:
            _console.print("Все были приняты на работу.", style="red")
        else:
            for y, w in enumerate(_ws):
                _console.print(f"{y + 1}. {w.__str__()}", style="cyan")
        _console.print("0. Назад", style="cyan")
        answer = _console.input(">>> ")
        try:
            if answer == "0":
                break
            _cafe.addWorker(_ws[int(answer) - 1])
            del _ws[int(answer) - 1]
        except Exception as e:
            _console.print(f"Произошла ошибка. ({e})", style="red bold")


def upgradeCafe():
    cursor.execute("""
    SELECT money FROM players
    WHERE id = %s
    """, (pid,))
    money = cursor.fetchone()[0]
    if money >= 50000 * _cafe.level // 2:
        _console.print("Вы можете улучшить своё заведение.", style="cyan")
        _console.bell()
        answer = _console.input("Улучшить? [1 / y - да; 0 / n - нет] > ")
        if answer == "1" or answer == "y":
            cursor.execute("""
            UPDATE players
            SET money = %s
            WHERE id = %s
            """, (money - 50000, pid))
            _cafe.level += 1


async def shop():
    pass


def play():
    """
    "Играть"
    """
    global _cafe, isCafeClosed
    cursor.execute("""
    SELECT data FROM players
    WHERE id = %s
    """, (pid,))
    res = cursor.fetchone()[0]
    if res is None:
        _cafe = createCafe()
    else:
        _cafe = loadCafe(res)

    while True:
        _console.clear()
        _cafe.save(cursor, pid)
        _console.print(
            f'Добро пожаловать в кафе "{_cafe.title}", здесь работает {len(_cafe.workers)} чел.\nЧто же вы хотите сделать?',
            style="cyan")
        _console.print(
            f"1. Приготовить клиенту блюдо.\n2. Пойти нанимать рабочих.\n3. Улучшить кафешку (-{50000 * _cafe.level // 2} мон.)\n4. Магазин\n5. Сведения\n0. Выйти",
            style="cyan")
        answer = input(">>> ")
        if answer == "1":
            cook()
        elif answer == "2":
            addWorkers()
        elif answer == "3":
            upgradeCafe()
        elif answer == "4":
            shop()
        elif answer == "5":
            getInfo()
        elif answer == "0":
            isCafeClosed = True
            break
        else:
            _console.print("Команда не распознана.", style="red bold")


def settings():
    pass


def createId():
    """
    Создание файла с идентификатором игрока, если не присутствует
    """
    _id: str = ""

    _id += str(random.randint(100000000, 999999999)) + ":"
    for x in range(40):
        _id += random.choice("abcdeABCDE12345")

    try:
        file = open("id", "w")
        file.write(_id)
        file.close()
    except Exception as e:
        _console.print(f"Ошибка: {e}", style="red")
        exit(-1)

    return _id


def getId():
    """
    Получение идентификатора игрока из файла
    """
    _id: str = ""

    try:
        file = open("id", "r")
        _id = file.read()
        file.close()
    except FileNotFoundError:
        _id = createId()

    return _id


def regestration():
    """
    Регистрация
    """
    login, password = "", ""
    while login == "" or password == "":
        _console.print("Регистрация.")
        login = _console.input("Введите логин: ", markup=False, emoji=False)
        password = _console.input("Введите пароль: ", markup=False, emoji=False)
    cursor.execute("""
    INSERT INTO players (id, nick, password)
    VALUES (%s, %s, %s)
    """, (pid, login, password))


def login(nick, pwd):
    """
    Вход в аккаунт
    """
    login, password = "", ""
    while login != nick or password != pwd:
        _console.clear()
        _console.print("Вход в аккаунт.")
        login = _console.input("Введите логин: ", markup=False, emoji=False)
        password = _console.input("Введите пароль: ", markup=False, emoji=False, password=True)


def menu():
    """
    Меню
    """
    global isCafeClosed
    while True:
        _console.clear()
        _console.print("""

     @@@@@    @@@   @@@@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@   @@@@@    @@@@
    @@   @@ @@@@@@@ @@       @@          @@    @@@      @@   @@@   @@@   @@@  @@@
   @@      @@   @@ @@@@@@   @@@@@@      @@    @@@@@@@  @@   @@@   @@@   @@    @@
 @@   @@ @@@@@@@ @@       @@          @@    @@@      @@@@@@@    @@@   @@@@@@@@
@@@@@  @@   @@ @@       @@@@@@@@    @@    @@@@@@@@ @@@  @@@  @@@@@  @@    @@

""", style="#ffd700", justify="center")
        _console.print("Меню.", justify="center", style="green bold")
        _console.print("1. Играть\n2. Настройки\n3. Об игре\n0. Выход", style="cyan")
        answer = input(">>> ")
        if answer == "1":
            try:
                isCafeClosed = False
                p = Thread(target=play)
                g = Thread(target=guests)
                g.start(), p.run()
                p.join(), g.join()
            except Exception as e:
                isCafeClosed = True
                _console.print(f"{e.__class__.__name__}: {e}", style="red bold")
        elif answer == "2":
            settings()
        elif answer == "3":
            __credits__()
        elif answer == "0":
            cursor.close()
            connector.close()
            break
        else:
            _console.print("Команда не распознана.", style="red bold")


if __name__ == '__main__':
    _console.set_window_title(f"Cafeteria ({__version__})")
    pid = getId()
    cursor.execute("""
    SELECT nick, password FROM players
    WHERE id = %s 
    """, (pid,))
    try:
        nick, password = cursor.fetchone()
        login(nick, password)
    except TypeError:
        regestration()
    menu()
    _console.print("Пока! ;)", style="green bold")
    time.sleep(0.5)
    os.system("cls" if __system__ == "win32" else "clear")
    sys.exit(1)
