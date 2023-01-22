"""
Module for planification calcul handler
"""
from threading import Thread, Condition
from api.models import StatutCalculEnum, EtatCalcul
from api.loggers import root_logger


class CalculHandler:
    """
    Object to store calcul state
    """

    calcul_lock: Condition = Condition()

    def __init__(self, calcul_id: int, solver: callable, **kwargs):
        self.calcul_id = calcul_id
        self.solver = solver
        self.kwargs = kwargs
        self.etat = EtatCalcul(identifiant=calcul_id, statut=StatutCalculEnum.NOT_STARTED)

    def start(self, cache):
        """
        Starts a calcul
        """
        Thread(name=f"Calcul {self.calcul_id}", target=self.calcul_function, args=[cache]).start()

    def calcul_function(self, cache):
        """
        Performs a planification computation
        """

        with CalculHandler.calcul_lock:
            self.etat.status = StatutCalculEnum.IN_PROGRESS
            cache.refresh_status(self.etat)

            try:
                solver_output = self.solver(**self.kwargs)
                self.etat.status = StatutCalculEnum.SUCCESS
                self.etat.result = solver_output
                cache.refresh_status(self.etat)

            except Exception as e:
                root_logger.error("Failed to compute planification", exc_info=e)
                self.etat.status = StatutCalculEnum.FAIL
                self.etat.result = None
                cache.refresh_status(self.etat)

            CalculHandler.calcul_lock.notify_all()
