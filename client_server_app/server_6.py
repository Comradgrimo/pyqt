import socket
import threading
import json
from client_server_app.response import ServerResponse
import dis
import inspect

connections = []
total_connections = 0
my_resp = ServerResponse()
resp_ok = my_resp.response(200, 'ok')


class PortValidator:

    def __init__(self, default=7777):
        self.default = default
        self.value = None

    def __get__(self, instance, owner):

        return self.value or self.default

    def __set__(self, instance, value):
        print('qqq')
        if type(value) != type(1):
            raise TypeError('Порт должен быть целым числом')
        if value <= 0:
            raise AttributeError('Порт должен быть больше 0')


def find_forbidden_methods_call(func, method_names):
    for instr in dis.get_instructions(func):
        if instr.opname == 'LOAD_METHOD' and instr.argval in method_names:
            return instr.argval


class ClientMeta(type):
    port = PortValidator()
    forbidden_method_names = ('bind', 'AF_INET')

    def __new__(cls, name, bases, class_dict):
        for _, value in class_dict.items():
            if inspect.isfunction(value):
                method_name = find_forbidden_methods_call(
                    value, cls.forbidden_method_names)
                if method_name:
                    raise ValueError(
                        f'called forbidden method "{method_name}"')
            elif isinstance(value, socket.socket):
                raise ValueError(
                    'Socket object cannot be defined in class definition')
            return type.__new__(cls, name, bases, class_dict)


class Server(threading.Thread, metaclass=ClientMeta):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + ' ' + str(self.address)

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(1024)
                print(data)
            except:
                print('Client ' + str(self.address) + ' has disconnected')
                self.signal = False
                connections.remove(self)
                break
            # Получаем от клиента
            if data != '':
                msg = data.decode('utf-8')
                jdata = json.loads(msg)
                try:
                    if jdata.get('user').get('account_name') is not None:
                        account_name = jdata.get('user').get('account_name')
                        self.name = account_name
                        print(f'Подключился {account_name}')
                except AttributeError:
                    pass
                if jdata.get('from') is not None:
                    print(f'{jdata.get("from")} написал {jdata.get("message")} ')

                for client in connections:
                    msg_to_client = json.dumps(resp_ok)
                    msg_to_client.encode('utf-8')

                    to = jdata.get('to')
                    if to == client.name:  # Отправка конкретному пользователю
                        client.socket.sendall(msg_to_client.encode('utf-8'))
                        msg_to_client_1 = f'{jdata.get("from")} написал {jdata.get("message")}'
                        print(msg_to_client_1)
                        client.socket.sendall(msg_to_client_1.encode('utf-8'))
                        continue

                    if client.name == jdata.get('from'):
                        client.socket.sendall(msg_to_client.encode('utf-8'))

                    if client.id != self.id:
                        client.socket.sendall(
                            (f'{jdata.get("from")} написал1 {jdata.get("message")}').encode('utf-8'))

    def main():
        # Get host and port
        host = 'localhost'
        port = Server.port

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)
        return sock


def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(
            Server(sock, address, total_connections, 'Name', True))
        connections[len(connections) - 1].start()
        print('New connection at ID ' + str(connections[len(connections) - 1]))
        total_connections += 1


newConnectionsThread = threading.Thread(
    target=newConnections, args=(Server.main(),))
newConnectionsThread.start()
