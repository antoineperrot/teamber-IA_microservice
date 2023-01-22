"""
Module for the cache to handle all planification computations
"""
import time

from cachelib.simple import SimpleCache

from solveur_api.models.calcul_handler import CalculHandler


class CalculCache:
    """
    Cache for all calculs started
    By default, cache items expires after 5 minutes
    """

    def __init__(self, threshold=500, default_timeout=300):
        self._cache: SimpleCache = SimpleCache(threshold=threshold, default_timeout=default_timeout)

    def start_calcul(self, demande_calcul: DemandeCalculPlanification) -> EtatCalculPlanification:
        """
        Starts a calcul of a planification
        @return: calcul id
        @rtype: EtatCalculPlanification
        """
        # Generate an id from timestamp to have an int
        id_calcul: int = int(time.time())
        while self._cache.get(str(id_calcul)) is not None:
            id_calcul += 1

        # Add to cache
        calcul_handler = CalculHandler(calcul_id=id_calcul, demande_calcul=demande_calcul)
        self._cache.add(str(id_calcul), calcul_handler.state)
        calcul_handler.start(self)
        return calcul_handler.state

    def get_status(self, calcul_id: int) -> EtatCalculPlanification:
        """
        Gets the status of a calcul
        @return: ResultatCalculPlanification with specified id, None if not found
        @type calcul_id: int
        @rtype: ResultatCalculPlanification

        @param calcul_id: id to get
        """
        return self._cache.get(str(calcul_id))

    def refresh_status(self, calcul_result: EtatCalculPlanification):
        """
        Rafraichis le statut d'un calcul handler dans le cache
        :param calcul_result:
        :return:
        """
        self._cache.set(str(calcul_result.calcul_id), calcul_result)


cache = CalculCache(default_timeout = 3600)
