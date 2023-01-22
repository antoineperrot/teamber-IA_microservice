"""Module de la classe ResultatCalcul"""
from json import loads
import pandas as pd


class ResultatCalcul:
    """Classe stockant un résultat de calcul"""

    def __init__(self,
                 events: pd.DataFrame | None,
                 stats: dict[int:pd.DataFrame] | None,
                 success: bool,
                 message: str | None = None):
        self.events = events
        self.stats = stats
        self.success = success
        self.message = message

    def serialize(self) -> dict:
        """Méthode de sérialisation"""
        out = {"events": loads(self.events.to_json(date_format="iso", date_unit="s")) if \
            self.events is not None else None,
               "stats": self.stats,
               "success": str(self.success),
               "message": str(self.message)}
        return out
