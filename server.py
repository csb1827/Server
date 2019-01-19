import asyncio

host = '127.0.0.1'
port = 8888

metrics = {}

def run_server(host, port):

    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

def process_data(data):
    data = data[0:-1]
    text = data.split()
    command = text[0]
    if command == 'put':
        info = text[1]+' '+text[2]+' '+text[3]
        result = put(info)
        return result
    elif command == 'get':
        info = text[1]
        result = get(info)
        return result
    else:
        return 'error\nwrong command\n\n'

def put(info):
    split_info = info.split()
    name_metric = split_info[0]
    value_metric = split_info[1]
    timestamp = split_info[2]
    if name_metric in metrics:
        for i in metrics[name_metric]:
            if i[1] == timestamp:
                i[0] = value_metric
                return 'ok\n\n'
        metrics[name_metric].append([value_metric, timestamp])
        return 'ok\n\n'
    else:
        metrics[name_metric] = [[value_metric, timestamp]]
        return 'ok\n\n'


def get(info):
    key = info
    if key == '*':
        keys = list(metrics.keys())
        text = 'ok\n'
        for i in keys:
            for j in metrics[i]:
                text = text+str(i)+' '+str(j[0])+' '+str(j[1])+'\n'
        text_end = text+'\n'
        return text_end
    else:
        keys = list(metrics.keys())
        text = 'ok\n'
        if key in keys:
            for i in metrics[key]:
                text = text+str(key)+' '+str(i[0])+' '+str(i[1])+'\n'
        text_end = text+'\n'
        return text_end


class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


run_server(host, port)
