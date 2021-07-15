import select
from response import ServerResponse
from socket import socket, AF_INET, SOCK_STREAM
import json
import argparse
# from logger import log, get_logger

DEBUG = False
my_resp = ServerResponse()
# info_logger = get_logger("server", 'server.log')


def create_conn():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', dest='port', default='7777')
    parser.add_argument('-a', '--address', dest='ip', default='localhost')
    args = parser.parse_args()
    return args

def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)

    return responses


# @log("call.log")
def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """
    resp_ok = my_resp.response(200, 'ok')
    for sock in w_clients:
        if sock in requests:
            # try:
                # Подготовить и отправить ответ сервера
            jdata = json.loads(requests[sock])
            # info_logger.info(f'Получено: {jdata}')
            if jdata.get("from") is not None:
                print(f'{jdata.get("from")} написал {jdata.get("message")} ')
                # print(f'Получено: {jdata}')                           #-->> В ЛОГИ
            # print('jdata ', jdata)
            try:
                if jdata.get('user').get('account_name'):
                    # print(resp_ok)
                    # info_logger.info(f"Подключился {jdata.get('user').get('account_name')}")
                    print(f"Подключился {jdata.get('user').get('account_name')}")
                    msg = json.dumps(resp_ok)
                    msg.encode('utf-8')
                    sock.send(msg.encode('utf-8'))
            except AttributeError:
                pass
            if jdata.get('action') == 'quit':
                # info_logger.info(f'Клиент {jdata.get("client_name")} отключился')
                print(f'Клиент {jdata.get("client_name")} отключился')
                sock.close()
                all_clients.remove(sock)
            try:
                msg = json.dumps(resp_ok)
                # info_logger.info(f'Отправлено: {msg}')
                # print(f'Отправлено: {msg}')                        #-->> В ЛОГИ
                sock.send(msg.encode('utf-8'))
            except OSError:
                pass


class MyDescriptor(object):
    """Это класс дескриптора."""

    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner):
        if self.value <= 0:
            AttributeError('Порт должен быть больше 0')
        return self.value

    def __set__(self, instance, value):
        return self.value


class ServerSock():
    port_v = MyDescriptor(7777)


if __name__ == '__main__':
    print('Эхо-сервер запущен!')
    s = ServerSock()

    clients = []
    address = ('localhost', s.port_v)
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)  # Таймаут для операций с сокетом
    while True:
        try:
            conn, addr = s.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            # print(f"Получен запрос на соединение от {str(addr)}")         -->> В ЛОГИ
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 3
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                # print(requests)
                write_responses(requests, w, clients)  # Выполним отправку ответов клиентам
