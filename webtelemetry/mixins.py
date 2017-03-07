from redis import StrictRedis
from webtelemetry import settings
import tornado.web

class RedisMixin(tornado.web.RequestHandler):
    """
    Handles writing to redis
    """

    def initialize(self):
        self.redis = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
