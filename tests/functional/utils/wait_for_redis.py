import time

from redis.client import Redis

from tests.functional.utils.settings import settings

if __name__ == '__main__':
    redis_settings = settings.plugins.redis
    redis_client = Redis(host=redis_settings.host, port=redis_settings.port)
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
