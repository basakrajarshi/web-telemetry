import json
from webtelemetry import settings

class LoggerBase(object):
    """
    Base class for all loggers
    """

    def __init__(self, logger_name):
        self.logger_name = logger_name

    class LoggerException(Exception):
        pass

    def write(self, msg):
        raise NotImplementedError()


class ConsoleLogger(LoggerBase):
    """
    Outputs the Telemetry Event to stdout
    """

    def write(self, msg):
        print msg.__str__()


class JsonLogger(LoggerBase):
    """
    Outputs the Telemetry Event to a JSON file
    """

    def __init__(self, logger_name):
        super(JsonLogger, self).__init__(logger_name)
        self._json_file = settings.LOGGERS[self.logger_name]['config']['filename']

    def write(self, msg):
        # open the file in append mode
        with open(self._json_file, 'a') as json_file:
            # write out the json message to file
            json_file.write(json.dumps(msg))
            json_file.write('\n')
