import websocket
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        url = self.get_argument('url', default=None)
        data = self.get_argument('data', default=None)
        if not url or not data:
            raise Exception('Usage: sqlmap.py -u "http://%s/?url=[target]&data=[sql'
                       'i] -p data"' % self.request.host)
            self.finish()
        if not url.startswith('ws://') and not url.startswith('wss://'):
            raise Exception('Invaild WebSocket Url, example: ws://127.0.0.1/chat')

        print 'Request Payload: %s' % data
        ws = websocket.WebSocket()
        ws.connect(url)
        ws.send(data)
        self.write(ws.recv())
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', MainHandler),
        ]
        settings = dict(debug=True,)
        tornado.web.Application.__init__(self, handlers=handlers, **settings)


if __name__ == '__main__':
    define('port', default=8888, help='Port listened')
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    print 'WebSocket Injection Server Listenning on %d' % options.port
    tornado.ioloop.IOLoop.instance().start()
