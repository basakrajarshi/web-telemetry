from app import TelemetryApplication
from handlers import SessionHandler, TelemetryHandler
from tornado.testing import AsyncHTTPTestCase
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

    @mock.patch('mixins.StrictRedis.get', return_value='2')
    def test_decrement_session(self, mock_redis):
        # call delete
        response = self.fetch(
            '/session/',
            headers=cookie,
            method='DELETE'
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['text'], 'SESSION_DECR')

    @mock.patch('mixins.StrictRedis.get', return_value='1')
    def test_clear_cookie(self, mock_redis):
        response = self.fetch(
            '/session/',
            method='DELETE',
            headers=cookie
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['text'], 'SESSION_CLEAR')

    @mock.patch('mixins.StrictRedis.get', return_value=None)
    def test_invalid_operation(self, mock_redis):
        response = self.fetch(
            '/session/',
            method='DELETE'
        )
        self.assertEqual(response.code, 400)
        self.assertEqual(json.loads(response.body)['text'], 'INVALID_OPERATION')
