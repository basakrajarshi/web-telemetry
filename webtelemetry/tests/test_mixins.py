import unittest
from webtelemetry.mixins import LoggerMixin, get_module_and_class
from webtelemetry import settings
from webtelemetry.loggers import ConsoleLogger, JsonLogger
import mock
from tornado.escape import json_encode

LOGGERS = {
    'JsonLogger': {
        'module_path': 'webtelemetry.loggers.JsonLogger',
        'config': {
            'filename': 'output.json'
        }
    },
    'ConsoleLogger': {
        'module_path': 'webtelemetry.loggers.ConsoleLogger',
        'config': {}
    }
}

class LoggerMixinTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = LoggerMixin()

    def test_get_module_and_class_name(self):
        test_string = 'webtelemetry.loggers.JsonLogger'
        module_name, classname = get_module_and_class(test_string)

        self.assertEqual(module_name, 'webtelemetry.loggers')
        self.assertEqual(classname, 'JsonLogger')

    @mock.patch('webtelemetry.loggers.settings.LOGGERS', LOGGERS)
    @mock.patch('webtelemetry.loggers.ConsoleLogger.write')
    @mock.patch('webtelemetry.loggers.JsonLogger.write')
    def test_broadcast(self, mock_console, mock_json):
        message = {
            'event': 'click',
            'user_ip': '10.0.0.1',
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }
        self.logger.log_event(json_encode(message))
        mock_console.assert_called()
        mock_json.assert_called()
