import json
from typing import Any
from enum import Enum, IntEnum
from datetime import datetime, time, timezone
from uuid import UUID


def handler_serialize(obj):
    return json.dumps(serialize(obj), ensure_ascii=False)


def serialize(obj: Any):
    if isinstance(obj, (datetime, time)):
        return obj.replace(tzinfo=timezone.utc).isoformat()

    if isinstance(obj, (Enum, IntEnum)):
        return obj.value

    if isinstance(obj, UUID):
        return obj.hex

    if isinstance(obj, list):
        return [serialize(item) for item in obj]

    if isinstance(obj, dict):
        return {key: serialize(value) for key, value in obj.items()}

    return obj
