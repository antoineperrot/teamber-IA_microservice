"""
Module for custom encoder
"""
from datetime import datetime
from pandas import DataFrame, Timestamp
from flask.json import JSONEncoder
from api.services.planning_optimizer.lib_planning_optimizer import ResultatCalcul


class CustomJsonEncoder(JSONEncoder):
    """
    Custom json encoder for specific encoding
    """

    def default(self, o):  # pylint: disable=E0202
        """custom encoder"""
        if isinstance(o, ResultatCalcul):
            return o.serialize()
        elif isinstance(o, DataFrame):
            return o.to_dict()
        elif isinstance(o, Timestamp):
            o = o.to_pydatetime()
            return o.isoformat()
        # default, if not one of the specified object. Caller's problem if this is not serializable.
        return JSONEncoder.default(self, o)
