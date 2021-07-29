import socket
import threading
import sys
import json
from datetime import datetime
from client_server_app.response import ServerResponse


# Ожидание входящих данных от сервера
def send_json(arg: dict) -> bytes:
    return json.dumps(arg).encode('utf-8')


def current_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def receive(socket, signal):
    """Ожидание входящих данных от сервера."""
    while signal:
        try:
            data = socket.recv(1024)
            msg = str(data.decode('utf-8'))
            if msg[0:4] != 'None':
                print(msg)
        except:
            print('You have been disconnected from the server')
            signal = False
            break


# Get host and port
host = 'localhost'
port = 7777
my_resp = ServerResponse()
login = 'comrad'
# Попытка подключения к серверу
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print('Could not make a connection to the server')
    input('Press enter to quit')
    sys.exit(0)
msg = send_json(my_resp.presence(login, current_time()))
sock.sendall(msg)
# Создаем новый поток для ожидания данных
receiveThread = threading.Thread(target=receive, args=(sock, True))
receiveThread.start()

while True:
    message = input('Введите сообщение: \n')

    # Отправка конкретному пользователю
    if message.startswith('#'):
        to = message.split()[0][1:]
        message = ' '.join(message.split()[1:])
        msg_server = my_resp.msg(current_time(), to, login, message)
    else:
        msg_server = my_resp.msg(current_time(), 'all', login, message)

    to_server = send_json(msg_server)
    sock.sendall(to_server)
