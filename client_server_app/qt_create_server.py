import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from client_server_app import qt_server_app
import socket
import threading
import json
from client_server_app.response import ServerResponse

class ExampleApp(QtWidgets.QMainWindow, qt_server_app.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.total_connections = 0
        self.my_resp = ServerResponse()
        self.setupUi(self)
        self.pushOk.clicked.connect(self.my_func)
        self.pushStart.clicked.connect(self.start_server)
        self.pushExit.clicked.connect(QtWidgets.qApp.quit)

    def my_func(self):
        self.listWidget.clear()
        self.listWidget.addItem('sds')
        # if directory:
        #     for file_name in os.listdir(directory):
        #         self.listWidget.addItem(file_name)



    def server(self,socket, address, id, name, signal):
        resp_ok = self.my_resp.response(200, 'ok')
        while True:
            try:
                data = socket.recv(1024)
                print(data)
            except:
                print('Client ' + str(address) + ' has disconnected')
                signal = False
                self.connections.remove(address)
                break
            # Получаем от клиента
            if data != '':
                msg = data.decode('utf-8')
                jdata = json.loads(msg)
                try:
                    if jdata.get('user').get('account_name') is not None:
                        account_name = jdata.get('user').get('account_name')
                        name = account_name
                        print(f'Подключился {account_name}')
                except AttributeError:
                    pass
                if jdata.get('from') is not None:
                    print(f'{jdata.get("from")} написал {jdata.get("message")} ')

                for client in self.connections:
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

                    if client.id != id:
                        client.socket.sendall(
                            (f'{jdata.get("from")} написал1 {jdata.get("message")}').encode('utf-8'))



    def new_connections(self, socket):
        while True:
            sock, address = socket.accept()
            self.connections.append(
                self.server(sock, address, self.total_connections, 'Name', True))
            self.connections[len(self.connections) - 1].start()
            print('New connection at ID ' + str(self.connections[len(self.connections) - 1]))
            self.total_connections += 1


    def start_server(self):
        host = 'localhost'
        port = 7777

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)

        newConnectionsThread = threading.Thread(target=self.new_connections, args=(sock,))
        newConnectionsThread.start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()