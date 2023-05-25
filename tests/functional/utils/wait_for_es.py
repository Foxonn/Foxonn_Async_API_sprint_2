import time

from elasticsearch import Elasticsearch

from tests.functional.utils.settings import settings

if __name__ == '__main__':
    es_settings = settings.plugins.elastic
    es_client = Elasticsearch(hosts=f'{es_settings.host}:{es_settings.port}')
    while True:
        if es_client.ping():
            break
        time.sleep(1)
