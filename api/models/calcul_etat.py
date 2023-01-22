"""Module de l'Etat de calcul"""
from enum import Enum


class StatutCalculEnum(Enum):
    """Enum statut calcul"""
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    IN_PROGRESS = "IN_PROGRESS"
    NOT_STARTED = "NOT_STARTED"


class EtatCalcul:
    """Class stockant l'état d'un calcul, caractérisé par son état (succès, échec etc.), et son résultat en cas de
    succès"""

    def __init__(self, identifiant: int, statut: StatutCalculEnum):
        self.identifiant = identifiant
        self.statut = statut
        self.result = None
