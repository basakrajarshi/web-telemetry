from app import TelemetryApplication
from handlers import SessionHandler, TelemetryEventHandler, TelemetryEventWebsocket
import unittest
import mock

class TestTelemetryApplication(unittest.TestCase):
    def setUp(self):
        self.app = TelemetryApplication()

    def test_app_handlers(self):
        handlers = self.app.handlers[0][1]
        hpaths = [h._path for h in handlers]

        self.assertEqual(handlers[0]._path, '/telemetry/events/ws/')
        self.assertTrue(issubclass(handlers[0].handler_class, TelemetryEventWebsocket))

        self.assertEqual(handlers[1]._path, '/session/')
        self.assertTrue(issubclass(handlers[1].handler_class, SessionHandler))

        self.assertEqual(handlers[2]._path, '/telemetry/events/')
        self.assertTrue(issubclass(handlers[2].handler_class, TelemetryEventHandler))
