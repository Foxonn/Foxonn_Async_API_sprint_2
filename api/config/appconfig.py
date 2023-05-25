from pathlib import Path
from typing import Any
from typing import Mapping

from pydantic import BaseSettings
from pydantic import Field

__all__ = ['AppConfig']

base_dir = Path(__file__).parents[2]


class AppConfig(BaseSettings):
    app: Mapping[str, Any]
    plugins: Mapping[str, Any]
    base_dir: str = Field(default=str(base_dir), allow_mutation=False)

    class Config:
        case_sensitive = False
        allow_mutation = False
        validate_assignment = True
