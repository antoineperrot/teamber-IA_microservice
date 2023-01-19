"""
Module contenant les controllers des données d'entrée de la fonctionnalité planning_optimizer
"""
from datetime import datetime
from werkzeug.exceptions import UnprocessableEntity
from api.loggers import logger_planning_optimizer
from api.back_connector.planning_optimizer import fetch_data_to_wandeed_backend
from api.services.planning_optimizer import solver_planning_optimizer
from api.services.planning_optimizer.lib_planning_optimizer import ResultatCalcul
from api.config import config
from api.services.planning_optimizer.tests.data_mocker import mock_back_data


def planning_optimizer_controller(json: dict) -> dict[int: ResultatCalcul]:
    """Controller du service planning_optimizer"""
    logger_planning_optimizer.info("Appel du controller")

    front_end_request = FrontEndPlanningOptimizerRequestContent.deserialize(json=json)

    if config["MODE"] == "PRODUCTION":
        imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires = fetch_data_to_wandeed_backend(
             url=front_end_request.backend_url,
             access_token=front_end_request.backend_access_token,
             date_start=front_end_request.date_start.isoformat(),
             date_end=front_end_request.date_end.isoformat(),
             key_project_prioritys_projets=front_end_request.key_project_prioritys_projets
        )
    else:
        imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires = mock_back_data(
            date_start=front_end_request.date_start,
            date_end=front_end_request.date_end,
            avg_n_tasks=10,
            avg_n_users=2
        )

    optimized_planning = solver_planning_optimizer(
        imperatifs=imperatifs,
        working_times=horaires,
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
                 date_start: datetime,
                 date_end: datetime,
                 key_project_prioritys_projets: dict,
                 parts_max_length: float,
                 min_duration_section: float):
        self.backend_url = str(backend_url)
        self.backend_access_token = str(backend_access_token)
        self.date_start = date_start
        self.date_end = date_end
        self.key_project_prioritys_projets = key_project_prioritys_projets
        self.parts_max_length = float(parts_max_length)
        self.min_duration_section = float(min_duration_section)

        self._check_values()

    @classmethod
    def deserialize(cls, json: dict):
        """Méthode de désérialisation"""

        logger_planning_optimizer.info("Désérialisation de la demande du front")
        try:
            out = cls(backend_access_token=json["backend_access_token"],
                      backend_url=json["backend_url"],
                      date_start=datetime.fromisoformat(json["date_start"]),
                      date_end=datetime.fromisoformat(json["date_end"]),
                      key_project_prioritys_projets=json["key_project_prioritys_projets"],
                      parts_max_length=json["parts_max_length"],
                      min_duration_section=json["min_duration_section"])
        except KeyError as ke:
            raise UnprocessableEntity(description="Missing key:" + str(ke))
        except ValueError as ve:
            raise UnprocessableEntity(description="Value error:" + str(ve))
        except Exception as e:
            raise UnprocessableEntity(description=f"Message d'erreur: {e}\n"
                                                  "Aide : Les valeurs ne sont pas castables dans les bons types. "
                                                  "Vérifier les valeurs entrées. Types attendus:\n "
                                                  "'backend_access_token': str\n"
                                                  "'backend_url': str (URL)\n"
                                                  "'date_start': str (isoformat)\n"
                                                  "'key_project_prioritys_projets': dict (isoformat)\n"
                                                  "'date_end': str (isoformat)\n"
                                                  "'parts_max_length': float\n"
                                                  "'min_duration_section': float\n")

        out._check_values()
        return out

    def _check_values(self):
        """Vérifie la correctitude des paramètres"""
        logger_planning_optimizer.info("Vérification de la validité des paramètres d'optimisation choisie")

        try:
            assert 0 < self.parts_max_length
        except AssertionError:
            raise UnprocessableEntity(description="'parts_max_length' doit être strictement positif")
        try:
            assert 0 < self.min_duration_section
        except AssertionError:
            raise UnprocessableEntity(description="'min_duration_section' doit être strictement positif")

        if not (self.date_end - self.date_start).total_seconds() > 60 * 60:
            raise UnprocessableEntity(description="La période de sprint indiquée est trop courte. Minimum 1h.")
        self.key_project_prioritys_projets = self._assert_and_type_mapping_priority_structure()

    def _assert_and_type_mapping_priority_structure(self):
        """Vérifie la validité du dictionnaire de priorités envoyé"""
        try:
            self.key_project_prioritys_projets = dict(self.key_project_prioritys_projets)
        except ValueError:
            raise ValueError("key_project_prioritys_projets n'a pas le bon format.\nFormat attendu : {int: int}.")

        for key, value in self.key_project_prioritys_projets.items():
            try:
                key_float = float(key)
            except ValueError:
                raise TypeError(f"key_project_prioritys_projets: la clé '{key}' n'est pas un float.")
            if int(key) != key_float:
                raise TypeError(f"key_project_prioritys_projets: la clé '{key}' n'est pas un entier.")
            self.key_project_prioritys_projets[key] = value

            try:
                value_float = float(value)
            except ValueError:
                raise TypeError(f"key_project_prioritys_projets: la valeur '{value}' n'est pas un float.")
            if int(value) != value_float:
                raise TypeError(f"key_project_prioritys_projets: la valeur '{value}' n'est pas un entier.")
            self.key_project_prioritys_projets[key] = int(value)

            return self.key_project_prioritys_projets
