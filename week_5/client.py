# task 1, week 5

import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, server_host, server_port, timeout=None):
        self.server_host = server_host
        self.server_port = server_port
        self.timeout = timeout

    def _format_sending_data(self, call, key, value=None, timestamp=None):
        """
        This method creates data for sending
        :param call: name of function ('put' or 'get')
        :param key: key for sending
        :param value: has 'Nony' by default
        :param timestamp: (has 'None' by default)
        :return: string
        """
        data = ''
        if call == 'put':
            value = float(value)
            data = str(call) + ' ' + str(key) + ' ' + str(value) + ' ' + str(timestamp) + '\n'
        else:
            data = str(call) + ' ' + str(key) + '\n'
        return data

    def _format_responsing_data(self, response):
        data = response.decode('utf-8')
        data = data.split('\n')[1:]

        rsp_dist = {}

        for str in data:
            if str == '':
                continue
            str_list = str.split()
            key = str_list[0]
            value = float(str_list[1])
            timestamp = int(str_list[2])

            if key in rsp_dist:
                rsp_dist[key].append((timestamp, value))
            else:
                rsp_dist[key] = [(timestamp, value)]
        return rsp_dist

    def _do_request(self, data):
        """
        This method do requests to the server.
        :param data: data in string-format
        :return: the answer from the server at byteformat
        """
        with socket.create_connection((self.server_host, self.server_port), self.timeout) as sock:
            sock.send(data.encode('utf-8'))
            return sock.recv(1024)


    def put(self, key, value, timestamp=None):
        if not timestamp:
            timestamp = str(int(time.time()))
        sending_data = self._format_sending_data('put', key, value, timestamp)
        print(sending_data.encode())
        response = self._do_request(sending_data)
        if 'ok' in response.decode('utf-8'):
            return
        else:
            raise ClientError


    def get(self, key='*'):
        sending_data = self._format_sending_data('get', key)
        response = self._do_request(sending_data)
        if 'error' in response.decode('utf-8'):
            raise ClientError
        if len(response) == 4:
            return {}
        else:
            response_dict = self._format_responsing_data(response)
            for key in response_dict.keys():
                response_dict[key] = sorted(response_dict[key], key=lambda item: item[0])
        return response_dict

# client = Client("127.0.0.1", 8888, timeout=15)

# client.put("palm.cpu", 0.5, timestamp=1150864247)
# client.put("palm.cpu", 2.0, timestamp=1150864248)
# client.put("palm.cpu", 0.5, timestamp=1150864248)
#
# client.put("eardrum.cpu", 3, timestamp=1150864250)
# client.put("eardrum.cpu", 4, timestamp=1150864251)
# client.put("eardrum.memory", 4200000)

# print(client.get("*"))