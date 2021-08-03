import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from client_server_app import qt_client_form_app
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




class ExampleApp(QtWidgets.QMainWindow, qt_client_form_app.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.my_resp = ServerResponse()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.start_client)
        self.msg = self.pushButton.clicked.connect(self.send_message)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.pushOk.clicked.connect(self.get_contacts)
        # self.pushButton.clicked.connect(self.start_server)
        # self.pushExit.clicked.connect(QtWidgets.qApp.quit)

    def receive(self,socket, signal):
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

    def send_message(self):
        if self.lineEdit.text() !='':
            message = str(self.lineEdit.text())

            # Отправка конкретному пользователю
            if message.startswith('#'):
                to = message.split()[0][1:]
                message = ' '.join(message.split()[1:])
                msg_server = self.my_resp.msg(current_time(), to, self.login, message)
            elif message[0:11] == 'getcontacts':
                msg_server = self.my_resp.getcontacts(current_time(), self.login)
            else:
                msg_server = self.my_resp.msg(current_time(), 'all', self.login, message)

            to_server = send_json(msg_server)
            print(to_server)
            self.sock.sendall(to_server)

    def start_client(self):
        host = str(self.lineEdit_2.text())
        port = int(self.lineEdit_3.text())
        self.sock.connect((host, port))
        my_resp = ServerResponse()
        self.login = 'comrad'
        # Попытка подключения к серверу
        # try:
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.connect((host, port))
        # except:
        #     print('Could not make a connection to the server')
        #     input('Press enter to quit')
        #     sys.exit(0)
        msg = send_json(my_resp.presence(self.login, current_time()))
        self.sock.sendall(msg)
        # Создаем новый поток для ожидания данных
        receiveThread = threading.Thread(target=self.receive, args=(self.sock, True))
        receiveThread.start()
        # msg = self.msg
        # sock.sendall(msg)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()