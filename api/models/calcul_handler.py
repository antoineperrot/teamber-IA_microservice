"""
Module for planification calcul handler
"""
from threading import Thread, Condition
from api.models import StatutCalculEnum, EtatCalcul
from api.loggers import root_logger
from api.back_connector.tools import FailRecuperationBackendDataException


class CalculHandler:
    """
    Object to store calcul state
    """

    calcul_lock: Condition = Condition()

    def __init__(self, calcul_id: int, handler: callable, **kwargs):
        self.calcul_id = calcul_id
        self.handler = handler
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
            root_logger.info(f"Lancement d'un thread. Id calcul: {self.calcul_id}")
            self.etat.set_statut(StatutCalculEnum.IN_PROGRESS)
            cache.refresh_status(self.etat)

            try:
                solver_output = self.handler(**self.kwargs)
                self.etat.set_statut(StatutCalculEnum.SUCCESS)
                self.etat.set_result(solver_output)
                cache.refresh_status(self.etat)

            except FailRecuperationBackendDataException as e:
                self.etat.set_statut(StatutCalculEnum.FAIL)
                self.etat.set_result(None)
                self.etat.set_message(message=e.msg)
                cache.refresh_status(self.etat)

            except Exception as e:
                root_logger.error("Failed to compute planification", exc_info=e)
                self.etat.set_statut(StatutCalculEnum.FAIL)
                self.etat.set_result(None)
                self.etat.set_message(str(e))
                cache.refresh_status(self.etat)

            CalculHandler.calcul_lock.notify_all()
            root_logger.info(f"Fin d'un thread. Id calcul: {self.calcul_id}")
