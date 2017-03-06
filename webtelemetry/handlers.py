import tornado.web
import tornado.websocket
import uuid
import json

from mixins import RedisMixin

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


class SessionHandler(RedisMixin):
    """
    Checks if the session exists or not.
    If the session exists, increment the count in Redis
    Else, create and return a session
    """
    def get(self):
        # Handle session
        session_id = self.get_secure_cookie('sessionid')
        if not session_id:
            # create session
            session_id = uuid.uuid4().hex
            self.set_secure_cookie('sessionid', session_id)
            # set cookie count to redis
            self.redis.set(session_id, 1)
            response = json.dumps({
                'text': 'SESSION_START'
            })
        else:
            # The session exists. New tab
            # increment the session value
            self.redis.incr(session_id)
            response = json.dumps({
                'text': 'SESSION_INCR'
            })
        self.write(response)

    def delete(self):
        session_id = self.get_secure_cookie('sessionid')
        if not session_id:
            response = json.dumps({
                'text': 'INVALID_OPERATION'
            })
            self.set_status(400)
            self.write(response)
            self.finish()
            return
        count = self.redis.get(session_id)

        if int(count) == 1:
            # delete the key from redis
            self.redis.delete(session_id)
            # clear the cookie
            self.clear_cookie(session_id)
            response = json.dumps({
                'text': 'SESSION_CLEAR'
            })
        elif int(count) > 1:
            # decrement the key in redis
            self.redis.decr(session_id)
            response = json.dumps({
                'text': 'SESSION_DECR'
            })
        self.write(response)
