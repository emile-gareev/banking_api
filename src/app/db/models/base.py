import orjson
from pydantic import BaseModel
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from typing import Any, Callable, Optional

metadata = MetaData()

Base = declarative_base(metadata=metadata)


def orjson_dumps(value: Any, *, default: Optional[Callable[[Any], Any]]) -> str:
    return orjson.dumps(value, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
