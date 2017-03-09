from app import TelemetryApplication
from tornado.httpclient import HTTPRequest
from tornado.testing import gen_test, AsyncHTTPTestCase
from tornado.escape import json_decode, json_encode
from tornado.websocket import websocket_connect
from tornado.httpclient import HTTPError
import json
import mock

MOCK_COOKIE = 'sessionid="2|1:0|10:1488572934|9:sessionid|44:MDFmMjgwODRhZDcwNGQyOWE3OWQ2YjUxOWEwMDFmYzQ=|be1970dc870c9cec700595c5d3a67321d26e1eba13dfc51f7435696ec90ea868"; expires=Sun, 02 Apr 2117 20:28:54 GMT; Path=/'

cookie = {
    'Cookie': MOCK_COOKIE
}


class TestSessionHandler(AsyncHTTPTestCase):
    def get_app(self):
        return TelemetryApplication()

    @mock.patch('mixins.StrictRedis')
    def test_create_session(self, mock_redis):
        response = self.fetch(
            '/session/',
            method='GET'
        )
        self.assertIsNotNone(response.headers['SET-COOKIE'])
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['text'], 'SESSION_START')

    @mock.patch('mixins.StrictRedis')
    def test_reinitialize_session(self, mock_redis):
        response = self.fetch(
            '/session/',
            headers=cookie,
            method='GET'
        )

        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['text'], 'SESSION_INCR')

    @mock.patch('mixins.StrictRedis')
    def test_decrement_session(self, mock_redis):

        mock_redis_instance = mock_redis.return_value
        mock_redis_instance.get.return_value = '2'

        # call delete
        response = self.fetch(
            '/session/',
            headers=cookie,
            method='DELETE'
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['text'], 'SESSION_DECR')

    @mock.patch('mixins.StrictRedis')
    def test_clear_cookie(self, mock_redis):

        mock_redis_instance = mock_redis.return_value
        mock_redis_instance.get.return_value = '1'

        response = self.fetch(
            '/session/',
            method='DELETE',
            headers=cookie
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['text'], 'SESSION_CLEAR')

    @mock.patch('mixins.StrictRedis')
    def test_invalid_operation(self, mock_redis):

        mock_redis_instance = mock_redis.return_value
        mock_redis_instance.get.return_value = None

        response = self.fetch(
            '/session/',
            method='DELETE'
        )
        self.assertEqual(response.code, 400)
        self.assertEqual(json.loads(response.body)['text'], 'INVALID_OPERATION')


class TelemetryAjaxHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return TelemetryApplication()

    @mock.patch('webtelemetry.loggers.ConsoleLogger.write')
    @mock.patch('webtelemetry.loggers.JsonLogger.write')
    @mock.patch(
        'tornado.web.RequestHandler.get_secure_cookie',
        return_value=MOCK_COOKIE
    )
    def test_broadcast_telemetry_event(
        self, mock_console, mock_json, mock_cookie):
        payload = {
            "event": "click",
            "user_ip": "10.0.0.1",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }
        response = self.fetch(
            '/telemetry/events/',
            method='POST',
            body=json_encode(payload)
        )
        self.assertEqual(response.code, 200)
        mock_console.assert_called()
        mock_json.assert_called()

    @mock.patch(
        'tornado.web.RequestHandler.get_secure_cookie',
        return_value=None
    )
    def test_unauthorized_request(self, mock_cookie):
        payload = {
            "event": "click",
            "user_ip": "10.0.0.1",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }
        response = self.fetch(
            '/telemetry/events/',
            method='POST',
            body=json_encode(payload)
        )
        self.assertEqual(response.code, 403)


class TelemetryHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return TelemetryApplication()


    @mock.patch(
        'tornado.websocket.WebSocketHandler.get_secure_cookie',
        return_value=None)
    @gen_test
    def test_unauthorized_request(self, mock_cookie):
        with self.assertRaises(HTTPError) as e:
            client = yield websocket_connect(
                'ws://localhost:{}/telemetry/events/ws/'.format(self.get_http_port()),
                io_loop=self.io_loop
            )


    @mock.patch('webtelemetry.loggers.ConsoleLogger.write')
    @mock.patch('webtelemetry.loggers.JsonLogger.write')
    @mock.patch(
        'tornado.websocket.WebSocketHandler.get_secure_cookie',
        return_value=MOCK_COOKIE)
    @gen_test
    def test_broadcast_message(self, mock_console, mock_json, mock_cookie):
        payload = {
            "event": "click",
            "user_ip": "10.0.0.1",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }

        client = yield websocket_connect(
            'ws://localhost:{}/telemetry/events/ws/'.format(self.get_http_port()),
            io_loop=self.io_loop
        )

        client.write_message(json_encode(payload))
        response = yield client.read_message()

        mock_console.assert_called()
        mock_json.assert_called()
