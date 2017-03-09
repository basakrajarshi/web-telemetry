from redis import StrictRedis
from webtelemetry import settings
import tornado.web

class RedisMixin(tornado.web.RequestHandler):
    """
    Handles writing to redis
    """

    def initialize(self):
        self.redis = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)



def get_module_and_class(module_string):
    parts = module_string.split('.')
    return (
        '.'.join(parts[:-1]),
        parts[-1]
    )

def populate_loggers():
    loggers = []
    for k in settings.LOGGERS.keys():
        module_name, class_name = get_module_and_class(
            settings.LOGGERS[k]['module_path']
        )
        mod = __import__(module_name)
        logger = getattr(mod.loggers, class_name)

        logger_instance = logger(logger_name=k)
        loggers.append(logger_instance)
    return loggers


class LoggerMixin(object):
    loggers = populate_loggers()

    def log_event(self, message):
        """
        Log event to all configured loggers
        """
        for logger in self.loggers:
            logger.write(message)


class CorsMixin(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', settings.CORS_ORIGIN)
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with,Access-Control-Allow-Origin')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Methods', 'GET,DELETE,OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()
