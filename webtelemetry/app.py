import os
import sys
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
from handlers import SessionHandler, TelemetryEventHandler, TelemetryEventWebsocket

from webtelemetry import settings

class TelemetryApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/telemetry/events/ws/', TelemetryEventWebsocket),
            (r'/session/', SessionHandler),
            (r'/telemetry/events/', TelemetryEventHandler),
        ]

        app_settings = dict(
            cookie_secret=settings.COOKIE_SECRET
        )

        tornado.web.Application.__init__(self, handlers, **app_settings)



def main():
    telemetry_application = TelemetryApplication()
    port = os.environ.get('TELEMETRY_PORT', 8000)
    telemetry_application.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
