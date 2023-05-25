import logging

import uvicorn
from dynaconf import Dynaconf
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio.client import Redis

from api import PROJECT_DIR
from api.config import logger
from api.config.appconfig import AppConfig
from api.middleware import RedisCacheFastApiMiddleware
from api.plugins.api_plugin.v1 import ApiV1Plugin
from api.plugins.elastic_plugin import ElasticPlugin
from api.plugins.functions_plugin import FunctionsPlugin
from api.plugins.redis_plugin import RedisPlugin
from api.utils.ioc import ioc
from api.utils.plugins_manager import plugins_manager

app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0"
)
app.add_middleware(RedisCacheFastApiMiddleware, ioc=ioc, cache_expiration=60)
SERVICE_API_DIR = PROJECT_DIR / 'services' / 'api'


@app.on_event('startup')
async def startup():
    settings = Dynaconf(
        lowercase_read=True,
        root_path=str(SERVICE_API_DIR),
        settings_files=["settings.toml"],
    )
    app_settings = AppConfig(
        app=settings.app,
        plugins=settings.plugins,
    )
    ioc.set(FastAPI, app)

    plugins_manager.add(RedisPlugin())
    plugins_manager.add(ElasticPlugin())
    plugins_manager.add(FunctionsPlugin())
    plugins_manager.add(ApiV1Plugin())

    await plugins_manager.loads(plugins_settings=app_settings.plugins)


@app.on_event('shutdown')
async def shutdown():
    await plugins_manager.unloads()


if __name__ == '__main__':
    uvicorn.run(
        '__main__:app',
        host='0.0.0.0',
        log_level=logging.DEBUG,
        log_config=logger.LOGGING,
    )
