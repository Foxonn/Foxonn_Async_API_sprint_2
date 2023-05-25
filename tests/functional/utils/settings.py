from pathlib import Path

from dynaconf import Dynaconf

__all__ = ['settings']

settings = Dynaconf(
    lowercase_read=True,
    settings_files=[str(Path(__file__).parent.parent / 'configs' / 'settings.toml')],
)
