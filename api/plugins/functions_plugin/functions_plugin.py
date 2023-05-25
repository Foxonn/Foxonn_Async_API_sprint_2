from typing import Any
from typing import Mapping
from typing import Optional

from elasticsearch import AsyncElasticsearch

from api.plugins.functions_plugin.impl.query import FilmByIdQuery
from api.plugins.functions_plugin.impl.query import FilmsPersonByIdQuery
from api.plugins.functions_plugin.impl.query import GenreByIdQuery
from api.plugins.functions_plugin.impl.query import GenresQuery
from api.plugins.functions_plugin.impl.query import PersonByIdQuery
from api.plugins.functions_plugin.impl.query import SearchFilmsQuery
from api.plugins.functions_plugin.impl.query import SearchPersonsQuery
from api.plugins.functions_plugin.impl.query import FilmsQuery
from api.plugins.functions_plugin.impl.query import PersonsQuery
from api.plugins.functions_plugin.interfaces.query import IFilmByIdQuery
from api.plugins.functions_plugin.interfaces.query import IFilmsPersonByIdQuery
from api.plugins.functions_plugin.interfaces.query import IGenreByIdQuery
from api.plugins.functions_plugin.interfaces.query import IGenresQuery
from api.plugins.functions_plugin.interfaces.query import IPersonByIdQuery
from api.plugins.functions_plugin.interfaces.query import ISearchFilmsQuery
from api.plugins.functions_plugin.interfaces.query import ISearchPersonsQuery
from api.plugins.functions_plugin.interfaces.query import IFilmsQuery
from api.plugins.functions_plugin.interfaces.query import IPersonsQuery
from api.utils.ioc import ioc
from api.utils.plugins_manager import IPlugin

__all__ = ['FunctionsPlugin']


class FunctionsPlugin(IPlugin):
    __slots__ = ()

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        return 'functions'

    async def load(self, plugins_settings: Optional[Mapping[str, Any]] = None) -> None:
        elastic = await ioc.get(AsyncElasticsearch)
        ioc.set(IFilmByIdQuery, FilmByIdQuery(elastic=elastic))
        ioc.set(IFilmsQuery, FilmsQuery(elastic=elastic))
        ioc.set(ISearchFilmsQuery, SearchFilmsQuery(elastic=elastic))
        ioc.set(IGenresQuery, GenresQuery(elastic=elastic))
        ioc.set(IGenreByIdQuery, GenreByIdQuery(elastic=elastic))
        ioc.set(ISearchPersonsQuery, SearchPersonsQuery(elastic=elastic))
        ioc.set(IPersonByIdQuery, PersonByIdQuery(elastic=elastic))
        ioc.set(IFilmsPersonByIdQuery, FilmsPersonByIdQuery(elastic=elastic))
        ioc.set(IPersonsQuery, PersonsQuery(elastic=elastic))

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass
