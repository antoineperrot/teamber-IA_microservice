"""
Module contenant les controllers des données d'entrée de la fonctionnalité lib_planning_optimizer
"""
from datetime import datetime

from werkzeug.exceptions import UnprocessableEntity

from api.back_connector.planning_optimizer import fetch_data_to_wandeed_backend
from api.back_connector.tools import to_iso_8601
from api.config import config
from api.lib_planning_optimizer.resultat_calcul import ResultatCalcul
from api.lib_planning_optimizer.solver import solver_planning_optimizer
from api.lib_planning_optimizer.tests.data_mocker import mock_back_data
from api.loggers import logger_planning_optimizer
from api.models import cache
from api.models.calcul_etat import EtatCalcul


class FrontEndPlanningOptimizerRequestParameters:
    """Classe contenant les infos que doit faire parvenir le front lors d'un appel à PlanningOptimizer"""

    def __init__(self,
                 backend_url: str,
                 backend_access_token: str,
                 date_start: datetime,
                 date_end: datetime,
                 selected_users: list[int] | None,
                 key_project_prioritys_projets: dict,
                 parts_max_length: float,
                 min_duration_section: float):
        self.backend_url = str(backend_url)
        self.backend_access_token = str(backend_access_token)
        self.date_start = date_start
        self.date_end = date_end
        self.selected_users = selected_users
        self.key_project_prioritys_projets = key_project_prioritys_projets
        self.parts_max_length = float(parts_max_length)
        self.min_duration_section = float(min_duration_section)
        self.date_start = self.date_start.replace(second=0, microsecond=0)
        self.date_end = self.date_end.replace(second=0, microsecond=0)

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
                      selected_users=json["selected_users"],
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
                                                  "'date_end': str (isoformat)\n"
                                                  "'key_project_prioritys_projets': dict[int: int] \n"
                                                  "'parts_max_length': float\n"
                                                  "'selected_users': list[int] OR None\n"
                                                  "'min_duration_section': float\n")

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

        if not(isinstance(self.selected_users, (list, type(None)))):
            raise UnprocessableEntity(description="'selected_users' doit être une liste d'entiers (IDs) OU None.")

        if isinstance(self.selected_users, list):
            if len(self.selected_users) == 0:
                raise UnprocessableEntity(description="'selected_users' ne peut pas être une liste vide, veuillez"
                                                      " indiquer des utilisateurs par leur ID.")
            for user in self.selected_users:
                try:
                    if int(user) != user:
                        raise UnprocessableEntity(description="'selected_users' doit être une liste d'entiers (IDs).")
                except Exception:
                    raise UnprocessableEntity(description="'selected_users' doit être une liste d'entiers (IDs).")

    def _assert_and_type_mapping_priority_structure(self) -> dict[int: int] | None:
        """Vérifie la validité du dictionnaire de priorités envoyé"""
        if not isinstance(self.key_project_prioritys_projets, (dict, type(None))):
            raise ValueError("key_project_prioritys_projets n'a pas le bon type.\nTypes attendu : dictionnaire {int: int}"
                             " OU None.")
        if isinstance(self.key_project_prioritys_projets, type(None)):
            return None
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


def planning_optimizer_controller(json: dict) -> EtatCalcul:
    """Controller du service lib_planning_optimizer"""
    logger_planning_optimizer.info("Appel du controller")
    request_parameters = FrontEndPlanningOptimizerRequestParameters.deserialize(json=json)
    return cache.start_calcul(handler=handler_demande_planning_optimizer, request_parameters=request_parameters)


def handler_demande_planning_optimizer(request_parameters: FrontEndPlanningOptimizerRequestParameters) \
        -> dict[str: dict[int: ResultatCalcul]]:
    """Handler demande lib_planning_optimizer"""
    if config["MODE"] == "PRODUCTION":
        imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires = fetch_data_to_wandeed_backend(
             url=request_parameters.backend_url,
             access_token=request_parameters.backend_access_token,
             date_start=to_iso_8601(request_parameters.date_start),
             date_end=to_iso_8601(request_parameters.date_end),
             selected_users=request_parameters.selected_users,
             key_project_prioritys_projets=request_parameters.key_project_prioritys_projets
        )
    else:
        imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires = mock_back_data(
            date_start=request_parameters.date_start,
            date_end=request_parameters.date_end,
            avg_n_tasks=50,
            avg_n_users=5)

    optimized_plannings = solver_planning_optimizer(
        imperatifs=imperatifs,
        working_times=horaires,
        taches=taches,
        date_start=request_parameters.date_start,
        date_end=request_parameters.date_end,
        parts_max_length=request_parameters.parts_max_length,
        min_duration_section=request_parameters.min_duration_section)

    return optimized_plannings
