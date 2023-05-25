import asyncio
from collections import UserDict
from typing import Any
from typing import ItemsView
from typing import Mapping
from typing import Optional

from ..interfaces import IPlugin
from ..interfaces import IPluginsManager

__all__ = [
    'PluginsManager',
    'plugins_manager',
]


class PluginsStore(UserDict[str, IPlugin]):

    def __setitem__(self, key: str, item: IPlugin) -> None:
        super().__setitem__(key, item)

    def __getitem__(self, item: str) -> IPlugin:
        return super().__getitem__(item)


class PluginsManager(IPluginsManager):
    __slots__ = (
        '__plugins_store',
    )

    def __init__(self) -> None:
        self.__plugins_store = PluginsStore()

    def list(self) -> ItemsView[str, IPlugin]:
        return self.__plugins_store.items()

    def add(self, plugin: IPlugin) -> None:
        self.__plugins_store[plugin.name] = plugin

    def get(self, plugin_name: str) -> IPlugin:
        return self.__plugins_store[plugin_name]

    async def loads(self, plugins_settings: Optional[Mapping[str, Any]] = None) -> None:
        _ = []
        for plugin in self.__plugins_store.values():
            if plugins_settings:
                if settings := plugins_settings.get(plugin.name, None):
                    await plugin.load(settings)
                    continue
            _.append(plugin.load())
        await asyncio.gather(*_)

    async def unloads(self) -> None:
        await asyncio.gather(*[plugin.unload() for plugin in self.__plugins_store.values()])

    async def reloads(self) -> None:
        await asyncio.gather(*[plugin.reload() for plugin in self.__plugins_store.values()])


plugins_manager = PluginsManager()
