"""Module de l'Etat de calcul"""
from enum import Enum
from api.loggers import root_logger


class StatutCalculEnum(Enum):
    """Enum statut calcul"""
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    IN_PROGRESS = "IN_PROGRESS"
    NOT_STARTED = "NOT_STARTED"
    CRASH_SOLVEUR = "CRASH_SOLVEUR"


class EtatCalcul:
    """Class stockant l'état d'un calcul, caractérisé par son état (succès, échec etc.), et son résultat en cas de
    succès"""

    def __init__(self, identifiant: int, statut: StatutCalculEnum, message: str = ""):
        self.identifiant = identifiant
        self.statut = statut
        self.result = None
        self.message = message
        root_logger.info(self)

    def set_statut(self, new_statut: StatutCalculEnum):
        """setter du statut"""
        self.statut = new_statut
        root_logger.info(self)

    def __repr__(self) -> str:
        out = f"EtatCalcul(identifiant={self.identifiant}, statut={self.statut}, result={self.result})"
        return out

    def set_result(self, new_result):
        """setter du result"""
        self.result = new_result
        root_logger.info(self)

    def set_message(self, message: str):
        """setter du message"""
        self.message = message

    def serialize(self) -> dict:
        """Séarialisation method"""
        out = {"identifiant": self.identifiant,
               "statut": self.statut,
               "result": self.result,
               "message": self.message}
        return out
