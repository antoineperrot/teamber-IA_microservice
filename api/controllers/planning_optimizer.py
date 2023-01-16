"""
Module contenant les controllers des données d'entrée de la fonctionnalité planning_optimizer
"""
from datetime import datetime
from werkzeug.exceptions import UnprocessableEntity
from api.loggers import logger_planning_optimizer
from api.back_connector.planning_optimizer import fetch_data_to_wandeed_backend
from api.services.planning_optimizer import solver_planning_optimizer


def planning_optimizer_controller(json: dict):
    """Controller du service planning_optimizer"""
    logger_planning_optimizer.info("Appel du controller")
    front_end_request = FrontEndPlanningOptimizerRequestContent.deserialize(json=json)
    imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires = fetch_data_to_wandeed_backend(
         url=front_end_request.backend_url,
         access_token=front_end_request.backend_access_token,
         date_start=front_end_request.date_start,
         date_end=front_end_request.date_end,
         key_project_prioritys_projets=front_end_request.key_project_prioritys_projets
    )

    optimized_planning = solver_planning_optimizer(
        imperatifs=imperatifs,
        horaires=horaires,
        taches=taches,
        date_start=front_end_request.date_start,
        date_end=front_end_request.date_end,
        parts_max_length=front_end_request.parts_max_length,
        min_duration_section=front_end_request.min_duration_section,
    )
    return optimized_planning


class FrontEndPlanningOptimizerRequestContent:
    """Classe contenant les infos que doit faire parvenir le front lors d'un appel à PlanningOptimizer"""

    def __init__(self,
                 backend_url: str,
                 backend_access_token: str,
                 date_start: str,
                 date_end: str,
                 key_project_prioritys_projets: dict,
                 parts_max_length: float,
                 min_duration_section: float):
        self.backend_url = backend_url
        self.backend_access_token = backend_access_token
        self.date_start = date_start
        self.date_end = date_end
        self.key_project_prioritys_projets = key_project_prioritys_projets
        self.parts_max_length = parts_max_length
        self.min_duration_section = min_duration_section

        self._cast_values()
        self._check_values()

    @classmethod
    def deserialize(cls, json: dict):
        """Méthode de désérialisation"""

        logger_planning_optimizer.info("Désérialisation de la demande du front")
        out = cls(backend_access_token=json["backend_access_token"],
                  backend_url=json["backend_url"],
                  date_start=json["date_start"],
                  date_end=json["date_end"],
                  key_project_prioritys_projets=json["key_project_prioritys_projets"],
                  parts_max_length=json["parts_max_length"],
                  min_duration_section=json["min_duration_section"])

        out._cast_values()
        out._check_values()
        return out

    def _cast_values(self):
        try:
            logger_planning_optimizer.info("Typage des valeurs de la demande du front")
            self.backend_access_token = str(self.backend_access_token)
            self.backend_url = str(self.backend_url)
            self.date_start = str(self.date_start)
            self.date_end = str(self.date_end)
            self.parts_max_length = float(self.parts_max_length)
            self.min_duration_section = float(self.min_duration_section)

        except Exception:
            raise UnprocessableEntity(description="Les valeurs ne sont pas castables dans les bons types. "
                                                  "Vérifier les valeurs entrées. Types attendus:\n "
                                                  "'backend_access_token': str\n"
                                                  "'backend_url': str (URL)\n"
                                                  "'date_start': str (isoformat)\n"
                                                  "'key_project_prioritys_projets': dict (isoformat)\n"
                                                  "'date_end': str (isoformat)\n"
                                                  "'parts_max_length': float\n"
                                                  "'min_duration_section': float\n")

    def _check_values(self):
        """Vérifie la correctitude des paramètres"""
        logger_planning_optimizer.info("Vérification de la validité des paramètres d'optimisation choisie")
        try:
            datetime.fromisoformat(self.date_start)
        except Exception:
            raise UnprocessableEntity(description="'date_start' is not an isoformat date")
        try:
            datetime.fromisoformat(self.date_end)
        except Exception:
            raise UnprocessableEntity(description="'date_end' is not an isoformat date")
        try:
            assert 0 < self.parts_max_length
        except AssertionError:
            raise UnprocessableEntity(description="'parts_max_length' doit être strictement positif")
        try:
            assert 0 < self.min_duration_section
        except AssertionError:
            raise UnprocessableEntity(description="'min_duration_section' doit être strictement positif")
