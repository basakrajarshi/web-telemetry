import tornado.web
import tornado.websocket
from tornado.escape import json_decode
import uuid
import json

from webtelemetry import settings

from mixins import CorsMixin, LoggerMixin, RedisMixin

class TelemetryEventWebsocket(tornado.websocket.WebSocketHandler, LoggerMixin):
    def check_origin(self, origin):
        return True

    def get(self, *args, **kwargs):
        sessionid = self.get_secure_cookie('sessionid')
        if not sessionid:
            self.set_status(403)
            self.finish()
        else:
            super(TelemetryEventWebsocket, self).get(*args, **kwargs)

    def on_message(self, message):
        json_message = json_decode(message)
        json_message['ip'] = self.request.remote_ip
        self.log_event(json_message)
        self.write_message({})


class TelemetryEventHandler(CorsMixin, LoggerMixin):
    def post(self):
        # check auth cookie
        sessionid = self.get_secure_cookie('sessionid')
        if sessionid:
            # get message
            message = self.request.body
            json_message = json_decode(message)
            json_message['ip'] = self.request.remote_ip
            json_message['sessionid'] = sessionid
            self.log_event(json_message)
            self.finish()
        else:
            self.set_status(403)
            self.finish()


class SessionHandler(CorsMixin, RedisMixin):
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
