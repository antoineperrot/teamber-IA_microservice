"""
Module for custom encoder
"""
import json
from datetime import datetime
from json import JSONEncoder
from json import loads

from flask.json import JSONEncoder
from flask.json.provider import JSONProvider
from pandas import DataFrame, Timestamp

from api.models import EtatCalcul, StatutCalculEnum
from api.services.planning_optimizer.lib_planning_optimizer import ResultatCalcul


class CustomJsonEncoder(JSONEncoder):
    """
    Custom json encoder for specific encoding
    """

    def default(self, o):  # pylint: disable=E0202
        """custom encoder"""
        if isinstance(o, StatutCalculEnum):
            return o.value
        if isinstance(o, ResultatCalcul):
            return o.serialize()
        if isinstance(o, EtatCalcul):
            return o.serialize()
        elif isinstance(o, Timestamp):
            return o.to_pydatetime()
        elif isinstance(o, datetime):
            return o.isoformat(timespec="seconds")
        elif isinstance(o, DataFrame):
            return loads(o.to_json(date_format="iso"))

        # default, if not one of the specified object. Caller's problem if this is not serializable.
        return JSONEncoder.default(self, o)


class CustomJsonProvider(JSONProvider):
    """
    Custom json provider class
    """

    def dumps(self, obj, **kwargs):
        kwargs["cls"] = CustomJsonEncoder
        return json.dumps(obj, **kwargs)

    def loads(self, s: str | bytes, **kwargs):
        return json.loads(s, **kwargs)
