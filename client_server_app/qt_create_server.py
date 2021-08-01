import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from client_server_app import qt_server_app
import socket
import threading
import json
from client_server_app.response import ServerResponse


connections = []
total_connections = 0
my_resp = ServerResponse()
resp_ok = my_resp.response(200, 'ok')
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + ' ' + str(self.address)

    # Попытка получить данные от клиента
    # Если это невозможно, предположите, что клиент отключился, и удалите его из данных сервера
    # Если это возможно, и мы получим данные обратно, распечатайте их на сервере и отправьте обратно каждому
    # клиент, кроме клиента, который его отправил
    # .декодирование используется для преобразования байтовых данных в строку для печати
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
            #Получаем от клиента
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
                if jdata.get("from") is not None:
                    print(f'{jdata.get("from")} написал {jdata.get("message")} ')

                for client in connections:
                    # if client.name == msg.get('name'):
                    msg_to_client = json.dumps(resp_ok)
                    msg_to_client.encode('utf-8')
                    # client.socket.sendall(msg.encode('utf-8'))

                    to = jdata.get("to")
                    if to == client.name:                                       #Отправка конкретному пользователю
                        client.socket.sendall(msg_to_client.encode('utf-8'))
                        msg_to_client_1 =  f'{jdata.get("from")} написал {jdata.get("message")}'
                        print(msg_to_client_1)
                        client.socket.sendall(msg_to_client_1.encode('utf-8'))
                        continue

                    if client.name == jdata.get("from"):
                        client.socket.sendall(msg_to_client.encode('utf-8'))

                    if client.id != self.id:
                        client.socket.sendall((f'{jdata.get("from")} написал1 {jdata.get("message")}').encode('utf-8'))

class ExampleApp(QtWidgets.QMainWindow, qt_server_app.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.my_resp = ServerResponse()
        self.setupUi(self)
        self.pushOk.clicked.connect(self.my_func)
        self.pushButton.clicked.connect(self.start_server)
        self.pushExit.clicked.connect(QtWidgets.qApp.quit)


    def my_func(self):
        self.listWidget.clear()
        self.listWidget.addItem('sds')
        print(self.lineEdit.text())
        # if directory:
        #     for file_name in os.listdir(directory):
        #         self.listWidget.addItem(file_name)

    def newConnections(self,socket):
        while True:
            sock, address = socket.accept()
            global total_connections
            connections.append(
                Client(sock, address, total_connections, 'Name', True))
            connections[len(connections) - 1].start()
            print('New connection at ID ' + str(connections[len(connections) - 1]))
            total_connections += 1


    def start_server(self):
        # Get host and port
        host = 'localhost'
        port = 7777

        # Create new server socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)

        # Create new thread to wait for connections
        newConnectionsThread = threading.Thread(
            target=self.newConnections, args=(sock,))
        newConnectionsThread.start()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()