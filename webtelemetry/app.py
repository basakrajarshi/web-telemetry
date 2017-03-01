import os
import sys
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
from handlers import TelemetryHandler

class TelemetryApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/telemetry/add/', TelemetryHandler),
        ]

        app_settings = dict()

        tornado.web.Application.__init__(self, handlers, **app_settings)



def main():
    telemetry_application = TelemetryApplication()
    port = os.environ.get('TELEMETRY_PORT', 8888)
    telemetry_application.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
