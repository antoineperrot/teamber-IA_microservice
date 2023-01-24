"""
Module for the cache to handle all planification computations
"""
import time

from cachelib.simple import SimpleCache

from api.models.calcul_handler import CalculHandler
from api.models import EtatCalcul


class CalculCache:
    """
    Cache for all calculs started
    By default, cache items expires after 5 minutes
    """

    def __init__(self, threshold=500, default_timeout=300):
        self._cache: SimpleCache = SimpleCache(threshold=threshold, default_timeout=default_timeout)

    def start_calcul(self, handler: callable, **kwargs) -> EtatCalcul:
        """
        Starts a calcul of a planification
        @return: calcul id
        @rtype: EtatCalcul
        """
        # Generate an id from timestamp to have an int
        calcul_id: int = int(time.time())
        while self._cache.get(str(calcul_id)) is not None:
            calcul_id += 1

        # Add to cache
        calcul_handler = CalculHandler(calcul_id=calcul_id, handler=handler, **kwargs)
        self._cache.add(str(calcul_id), calcul_handler.etat)
        calcul_handler.start(self)
        return calcul_handler.etat

    def get_status(self, calcul_id: int) -> EtatCalcul:
        """
        Gets the status of a calcul
        @return: ResultatCalculPlanification with specified id, None if not found
        @type calcul_id: int
        @rtype: ResultatCalculPlanification

        @param calcul_id: id to get
        """
        return self._cache.get(str(calcul_id))

    def refresh_status(self, calcul_result: EtatCalcul):
        """
        Rafraichis le statut d'un calcul handler dans le cache
        :param calcul_result:
        :return:
        """
        self._cache.set(str(calcul_result.identifiant), calcul_result)


cache = CalculCache(default_timeout=3600)
