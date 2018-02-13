# final project, week_6

import socket
import threading
import time


def run_server(host, port):
    server = Server('127.0.0.1', 8888)
    server.run()

class Server:
    def __init__(self, host, port, timeout=0, number_client=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.number_client = number_client

        self.shutdown_flag = False

        self.mutex = threading.Lock()

        self.start_time = 0

        self.clients = []
        self.storage = {}

        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = socket.socket()
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.number_client)

    def run(self):
        self.start_time = time.time()
        print("Running server...")
        while not self._shutdown():
            (client, address) = self.sock.accept()
            client.settimeout(5)
            if len(self.clients) > self.number_client:
                client.close()
            else:
                client_thread = threading.Thread(target=self._handle_client, args=(client, address,))
                client_thread.start()
                self.clients.append(client_thread)

    def shutdown_server(self):
        self.shutdown_flag = True
        self._shutdown()

    def _shutdown(self):
        if self.shutdown_flag:
            for connection in self.clients:
                connection.join()
            return True
        elif self.timeout == 0:
            return False
        elif time.time() - self.start_time >= self.timeout:
            return True

        return False

    def _handle_client(self, connection, address):
        start_time = time.time()
        while time.time() - start_time < connection.timeout:
            data = b''
            while not data.endswith(b'\n'):
                data += connection.recv(1024)

            status, data = self._parse_data(data)

            if status == 'put':
                if self._put(data):
                    self._send_data(connection, 'ok\n\n')
                else:
                    self._send_error(connection)
            elif status == 'get':
                data = self._get(data)
                self._send_data(connection, data)
            else:
                self._send_error(connection)
        connection.close()

    def _send_data(self, connection, data):
        connection.sendall(data.encode())

    def _send_error(self, connection):
        connection.sendall(b'error\nwrong command\n\n')

    def _parse_data(self, data):
        decoded_data = data.decode('utf-8')
        status, data = decoded_data.split(maxsplit=1)
        return status, data

    def _put(self, data):
        """
        This method put data to storage of the server.
        If command is wrong for protocol, this method return False, otherwise True
        :param data: expected in string format '<key> <value> <timestamp>'
        :return: bool
        """

        data = data.split()
        if len(data) > 3:
            return False
        key = data[0]
        data = data[1] + ' ' + data[2] + '\n'
        with self.mutex:
            if key not in self.storage:
                # create new note in the storage
                self.storage[key] = [data]
            elif data in self.storage[key]:
                pass
            else:
                # append new note to the storage
                self.storage[key].append(data)
        return True

    def _get(self, key):
        """
        This method extract data from the storage.
        If data exists for key, return in string format according the protocol.
        Else return 'ok\n\n'
        :param key: string
        :return: string
        """
        key = key.split()
        key = key[0]
        data = ''
        with self.mutex:
            if '*' in key:
                # return all data
                data += 'ok\n'
                for key in self.storage.keys():
                    for item in self.storage[key]:
                        data += key + ' '
                        data += item
                data += '\n'
            elif key in self.storage:
                data += 'ok\n'
                for item in self.storage[key]:
                    data += key + ' '
                    data += item
                data += '\n'
            else:
                data += 'ok\n\n'
        return data

