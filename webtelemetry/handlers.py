import tornado.websocket

class TelemetryHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'WebSocket opened'
        #TODO if session id is valid, increment count
        #TODO if session id is not valid, create a session

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        print 'WebSocket closed'
        # TODO check for session id count
        # TODO if session id count is 0, delete session cookie
