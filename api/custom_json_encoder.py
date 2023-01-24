"""
Module for custom encoder
"""
from datetime import datetime
from pandas import DataFrame, Timestamp
from flask.json import JSONEncoder
from api.services.planning_optimizer.lib_planning_optimizer import ResultatCalcul
from api.models import EtatCalcul, StatutCalculEnum
from json import loads


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
