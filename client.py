import socket
import time


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, name_metric, metric_value, timestamp=str(int(time.time()))):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            message = 'put {} {} {}\n'.format(name_metric, metric_value, timestamp)

            try:
                sock.sendall(message.encode('utf8'))
            except socket.error:
                raise ClientError

    def get(self, name_metric):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            message = 'get {}\n'.format(name_metric)

            try:
                sock.sendall(message.encode('utf8'))
            except socket.error:
                raise ClientError

            text = sock.recv(1024)
            text_metrics = text.decode("utf8")

            if text_metrics == 'ok\n\n':
                return {}
            elif text_metrics == 'error\nwrong command\n\n':
                raise ClientError
            else:
                text_metrics = text_metrics.replace('ok\n', '')
                text_metrics = text_metrics.replace('\n\n', '')
                text_metrics = text_metrics.replace('\n', '/')
                list_metrics = text_metrics.split('/')

                for i in range(len(list_metrics)):
                    list_metrics[i] = list_metrics[i].split()

                dict_metrics = {}
                keys = set()

                for i in list_metrics:
                    keys.add(i[0])

                for i in keys:
                    value_list = []
                    for j in list_metrics:
                        if i == j[0]:
                            if len(j) == 3:
                                value_list.append((int(j[2]), float(j[1])))
                    value_list = sorted(value_list)
                    dict_metrics[i] = value_list

        if name_metric == '*':
            return dict_metrics
        else:
            if name_metric in dict_metrics:
                return {name_metric: dict_metrics[name_metric]}
            else:
                return {}


class ClientError(socket.error):
    pass
