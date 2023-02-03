"""
Controller du task assigner
"""
import pandas as pd

from datetime import datetime
from werkzeug.exceptions import UnprocessableEntity
from api.back_connector.task_assigner.task_assigner import fetch_task_assigner_data_to_back
from api.services.task_assigner.lib_task_assigner.tools import ContrainteEtreSurProjet
from api.services.task_assigner.solver import solveur_task_assigner, SolverCrashException
from api.services.task_assigner.tests.data_mocker import mock_coherent_data
from api.back_connector.tools import FailRecuperationBackendDataException
from api.models import cache
from api.loggers import logger_task_assigner
from api.config import config


class FrontEndTaskAssignerRequestParameters:
    """Classe contenant ce les infos que doit faire parvenir le front lors d'un appel à TaskAssigner"""
    def __init__(self,
                 backend_access_token: str,
                 backend_url: str,
                 date_start: datetime,
                 date_end: datetime,
                 curseur: float,
                 contrainte_etre_sur_projet: ContrainteEtreSurProjet,
                 avantage_projet: float):
        self.backend_access_token = str(backend_access_token)
        self.backend_url = str(backend_url)
        self.date_start = date_start
        self.date_end = date_end
        self.curseur = float(curseur)
        try:
            self.contrainte_etre_sur_projet = ContrainteEtreSurProjet(contrainte_etre_sur_projet)
        except ValueError:
            available_values = [ContrainteEtreSurProjet.OUI.value,
                                ContrainteEtreSurProjet.NON.value,
                                ContrainteEtreSurProjet.DE_PREFERENCE.value]
            raise ValueError(" valeur incorrecte du paramètre 'contrainte_etre_sur_projet'. Choisir parmi les valeurs "
                             f"{available_values}")
        self.avantage_projet = float(avantage_projet)

        self._check_values()

    @classmethod
    def deserialize(cls, json: dict):
        """Méthode de désérialisation"""

        logger_task_assigner.info("Désérialisation de la demande du front")
        try:
            out = cls(backend_access_token=json["backend_access_token"],
                      backend_url=json["backend_url"],
                      date_start=datetime.fromisoformat(json["date_start"]),
                      date_end=datetime.fromisoformat(json["date_end"]),
                      curseur=json["curseur"],
                      contrainte_etre_sur_projet=json["contrainte_etre_sur_projet"],
                      avantage_projet=json["avantage_projet"])
        except KeyError as ke:
            raise UnprocessableEntity(description=f"Clé manquante: {ke}")
        except ValueError as ve:
            raise UnprocessableEntity(description="Value error:" + str(ve))
        except UnprocessableEntity as ue:
            raise ue
        except Exception:
            available_values = [ContrainteEtreSurProjet.OUI.value,
                                ContrainteEtreSurProjet.NON.value,
                                ContrainteEtreSurProjet.DE_PREFERENCE.value]
            raise UnprocessableEntity(description="Les valeurs ne sont pas castables dans les bons types. "
                                                  "Vérifier les valeurs entrées. Types attendus:\n "
                                                  "'backend_access_token': str\n"
                                                  "'backend_url': str (URL)\n"
                                                  "'date_start': str (isoformat)\n"
                                                  "'date_end': str (isoformat)\n"
                                                  "'curseur': float\n"
                                                  f"'contrainte_etre_sur_projet': str ({available_values})\n"
                                                  "'avantage_projet': float\n")

        out._check_values()
        return out

    def _check_values(self):
        """Vérifie la correctitude des paramètres"""
        logger_task_assigner.info("Vérification de la validité des paramètres d'optimisation choisie")
        try:
            assert 0 <= self.curseur <= 1
        except AssertionError:
            raise UnprocessableEntity(description="'curseur' doit être entre 0 et 1.")


def task_assigner_controller(json_file: dict):
    """
    Controller du Task assigner.
    - vérifie le contenue du json en entrée
    -
    """
    logger_task_assigner.info("Appel du controller")
    request_parameters = FrontEndTaskAssignerRequestParameters.deserialize(json_file)
    return cache.start_calcul(handler=handler_demande_task_assigner, request_parameters=request_parameters)


def check_data_consistency(
        df_prj: pd.DataFrame,
        df_cmp: pd.DataFrame,
        df_tsk: pd.DataFrame,
        df_dsp: pd.DataFrame,
):
    """
    Vérifie que les données reçues sont cohérentes.
    """
    logger_task_assigner.info("Vérification de la consistence des données récupérées dans le BACK.")
    if len(df_cmp) == 0:
        raise UnprocessableEntity(description="Pas de matrice de compétence disponible.")
    if len(df_tsk) == 0:
        raise UnprocessableEntity(description="Pas de tâches à assigner.")


def handler_demande_task_assigner(request_parameters: FrontEndTaskAssignerRequestParameters):
    """Handler d'une demande de task_assigner. Fonction appelée dans le thread de calcul."""

    if config["MODE"] == "PRODUCTION":
        df_prj, df_cmp, df_tsk, df_dsp = fetch_task_assigner_data_to_back(
            backend_url=request_parameters.backend_url,
            backend_access_token=request_parameters.backend_access_token,
            date_start=request_parameters.date_start.isoformat(timespec="seconds"),
            date_end=request_parameters.date_end.isoformat(timespec="seconds"))

    else:
        df_prj, df_cmp, df_tsk, df_dsp = mock_coherent_data()

    check_data_consistency(df_prj, df_cmp, df_tsk, df_dsp)

    # calcul d'une solution
    try:
        solution = solveur_task_assigner(
            df_prj=df_prj,
            df_cmp=df_cmp,
            df_tsk=df_tsk,
            df_dsp=df_dsp,
            curseur=request_parameters.curseur,
            contrainte_etre_sur_projet=request_parameters.contrainte_etre_sur_projet,
            avantage_projet=request_parameters.avantage_projet,
        )
        return solution

    except Exception as e:
        logger_task_assigner.error("Crash du solveur", exc_info=str(e))
        raise SolverCrashException()


