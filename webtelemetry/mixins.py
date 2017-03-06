from redis import StrictRedis
from settings import REDIS_HOST, REDIS_PORT
import tornado.web

class RedisMixin(tornado.web.RequestHandler):
    """
    Handles writing to redis
    """

    def initialize(self):
        self.redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
