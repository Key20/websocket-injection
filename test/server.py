import MySQLdb
import json
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.websocket


class Storage(dict):
    def __getitem__(self, item):
        return self[item]

    def __setitem__(self, key, value):
        self[key] = value


class BaseSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def __init__(self, application, request, **kwargs):
        self.session = Storage()
        db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test", charset="utf8")
        self.db = db.cursor()

        tornado.websocket.WebSocketHandler.__init__(self,application, request, **kwargs)

    @staticmethod
    def send_message(message):
        print 'Send: %s' % message
        for client in BaseSocketHandler.clients:
            client.write_message(json.dumps(message))


class WebSocketHandler(BaseSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        self.session.id = str(id(self))
        print 'Request: %s' % self.session.id
        self.clients.add(self)

    def on_close(self):
        print 'Close: %s' % self.session.id
        self.clients.remove(self)

    def on_message(self, message):
        print 'Recv: %s' % message
        try:
            self.db.execute("select table_name from information_schema.tables where table_schema='%s'" % message)
            data = self.db.fetchall()[0]
            self.send_message({'text': data[0]})
        except Exception, e:
            self.send_message({'text': str(e)})


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', WebSocketHandler),
        ]
        settings = dict(debug=True,)
        tornado.web.Application.__init__(self, handlers=handlers, **settings)


if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)

    tornado.ioloop.IOLoop.instance().start()
