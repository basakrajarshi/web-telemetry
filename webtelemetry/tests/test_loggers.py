import json
import sys
from StringIO import StringIO
import tempfile
import unittest
import os
import mock

from webtelemetry.loggers import ConsoleLogger, JsonLogger
from webtelemetry import settings

JSONLOGGER_NAME = 'JsonLogger'

LOGGERS = {
    JSONLOGGER_NAME: {
        'module_path': 'webtelemetry.loggers.JsonLogger',
        'config': {
            'filename': None
        }
    },
    'ConsoleLogger': {
        'module_path': 'webtelemetry.loggers.ConsoleLogger',
        'config': {}
    }
}


class ConsoleLoggerTestCase(unittest.TestCase):
    def test_console_logger_output(self):
        # change the standard output
        out = StringIO()
        sys.stdout = out

        logger = ConsoleLogger()
        msg = {
            'event': 'click',
            'user_ip': '10.0.0.1',
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }
        logger.write(msg)
        self.assertEqual(out.getvalue().strip(), msg.__str__())

class JsonLoggerTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_json_file = tempfile.mkstemp()
        LOGGERS[JSONLOGGER_NAME]['config']['filename'] = self.mock_json_file[1]

    def tearDown(self):
        os.remove(self.mock_json_file[1])

    @mock.patch('webtelemetry.loggers.settings.LOGGERS', LOGGERS)
    def test_json_logger_output(self):
        logger = JsonLogger(logger_name=JSONLOGGER_NAME)
        msg = {
            'event': 'click',
            'user_ip': '10.0.0.1',
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        logger.write(msg)

        with open(self.mock_json_file[1]) as test_json_output:
            output = test_json_output.read()
            self.assertEqual(output, json.dumps(msg))
