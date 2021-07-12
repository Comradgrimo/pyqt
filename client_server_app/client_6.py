from socket import *
import json
from datetime import datetime
from response import ServerResponse
# from logger import log, get_logger
# info_logger = get_logger("client", 'client.log')
#
# @log("client.log")
def authorized(user: str, pswrd: str, openfile: list) -> str:
    for i in openfile:
        if user in i:
            return user
    open_file('user.json', 'w', {user: pswrd})  # Здесь должно быть добавление в базу


def open_file(name: str, flag: str, info=None) -> list:           # Здесь должно быть чтение из базы
    if flag != "w":
        with open(f'{name}', f'r', encoding='utf-8') as f_n:
            objs = json.load(f_n)
        return objs
    else:
        with open(f'{name}', 'r', encoding='utf-8') as f_n:
            objs = json.load(f_n)
            objs.append(dict(info))
        # print(objs)
        with open(f'{name}', 'w', encoding='utf-8') as f_n:
            json.dump(objs, f_n)
        return objs


def send_json(arg: dict) -> bytes:
    return json.dumps(arg).encode('utf-8')


def current_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def echo_client():
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect(ADDRESS)  # Соединиться с сервером
        # Готовим приветствие
        msg = send_json(my_resp.presence(login, current_time()))
        # Отсылаем приветствие
        sock.send(msg)
        # Получаем ответ на приветствие
        data = sock.recv(1024).decode('utf-8')
        # print('data ', data)                          --> В ЛОГИ
        # foo = json.loads(data)
        # print('foo ', foo)
        # if foo['response'] == 200:  # ДОДЕЛАТЬ ВОЗМОЖНЫЕ КОДЫ ОШИБОК
        #     print(f'Добро пожаловать {login}')

        while True:
            msg = input('Ваше сообщение: ')
            if msg == '_exit':
                sock.send(send_json(my_resp.exit(login)))
                print('exit')
                # logger.info('Выход')
                break
            msg_server = my_resp.msg(current_time(), 'all', aut, msg)
            # print(msg_server, type(msg_server))
            to_server = send_json(msg_server)
            sock.send(to_server)
            # print(f'Вы отправили:{msg}')                      -->> В ЛОГИ

            # sock.send(msg.encode('utf-8'))  # Отправить!
            # data = sock.recv(1024).decode('utf-8')
            # print('Ответ:', data)


if __name__ == '__main__':

    ADDRESS = ('localhost', 7777)
    my_resp = ServerResponse()
    login = 'Comrad'
    while True:  # ДОДЕЛАТЬ ОБРАБОТКУ ВВОДА
        # login = input('Введите новый логин: ')
        login = 'Comrad'
        # pswrd = input('Введите новый пароль: ')
        pwd = '123'
        break
    foo = open_file('user.json', 'r')
    aut = authorized(login, pwd, foo)
    echo_client()
