import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'

COOKIE_SECRET = 'SOME_RANDOM_COOKIE_SECRET'

LOGGERS = {
    'JsonLogger': {
        'module_path': 'webtelemetry.loggers.JsonLogger',
        'config': {
            'filename': os.path.join(BASE_DIR, 'output.json')
        }
    },
    'ConsoleLogger': {
        'module_path': 'webtelemetry.loggers.ConsoleLogger',
        'config': {}
    }
}
