"""
Controller du task assigner
"""
import pandas as pd

from datetime import datetime
from werkzeug.exceptions import UnprocessableEntity
from api.back_connector.task_assigner.task_assigner import fetch_task_assigner_data_to_back
from api.services.task_assigner.tools.contrainte_projet import ContrainteEtreSurProjet
from api.services.task_assigner.solver import solveur, SolverCrashException
from api.loggers import logger_task_assigner


class FrontEndTaskAssignerRequestContent:
    """Classe contenant ce les infos que doit faire parvenir le front lors d'un appel à TaskAssigner"""
    def __init__(self,
                 backend_access_token: str,
                 backend_url: str,
                 date_start: str,
                 date_end: str,
                 curseur: float,
                 contrainte_etre_sur_projet: ContrainteEtreSurProjet,
                 avantage_projet: float):
        self.backend_access_token = backend_access_token
        self.backend_url = backend_url
        self.date_start = date_start
        self.date_end = date_end
        self.curseur = curseur
        self.contrainte_etre_sur_projet = contrainte_etre_sur_projet
        self.avantage_projet = avantage_projet

        self._cast_values()
        self._check_values()

    @classmethod
    def deserialize(cls, json: dict):
        """Méthode de désérialisation"""

        logger_task_assigner.info("Désérialisation de la demande du front")
        out = cls(backend_access_token=json["backend_access_token"],
                  backend_url=json["backend_url"],
                  date_start=json["date_start"],
                  date_end=json["date_end"],
                  curseur=json["curseur"],
                  contrainte_etre_sur_projet=json["contrainte_etre_sur_projet"],
                  avantage_projet=json["avantage_projet"])

        out._cast_values()
        out._check_values()
        return out

    def _cast_values(self):
        try:
            logger_task_assigner.info("Typage des valeurs de la demande du front")
            self.backend_access_token = str(self.backend_access_token)
            self.backend_url = str(self.backend_url)
            self.date_start = str(self.date_start)
            self.date_end = str(self.date_end)
            self.curseur = float(self.curseur)
            self.contrainte_etre_sur_projet = ContrainteEtreSurProjet(self.contrainte_etre_sur_projet)
            self.avantage_projet = float(self.avantage_projet)
        except Exception:
            raise UnprocessableEntity(description="Les valeurs ne sont pas castables dans les bons types. "
                                                  "Vérifier les valeurs entrées. Types attendus:\n "
                                                  "'backend_access_token': str\n"
                                                  "'backend_url': str (URL)\n"
                                                  "'date_start': str (isoformat)\n"
                                                  "'date_end': str (isoformat)\n"
                                                  "'curseur': float\n"
                                                  "'contrainte_etre_sur_projet': str {'oui','non','de preference'}\n"
                                                  "'avantage_projet': float\n")
        
    def _check_values(self):
        """Vérifie la correctitude des paramètres"""
        logger_task_assigner.info("Vérification de la validité des paramètres d'optimisation choisie")
        try:
            datetime.fromisoformat(self.date_start)
        except Exception:
            raise UnprocessableEntity(description="'date_start' is not an isoformat date")
        try:
            datetime.fromisoformat(self.date_end)
        except Exception:
            raise UnprocessableEntity(description="'date_end' is not an isoformat date")
        try:
            assert 0 <= self.curseur <= 1
        except AssertionError:
            raise UnprocessableEntity(description="'curseur' doit être entre 0 et 1.")

        available_values = [ContrainteEtreSurProjet.OUI.value,
                            ContrainteEtreSurProjet.NON.value,
                            ContrainteEtreSurProjet.DE_PREFERENCE.value]
        if self.contrainte_etre_sur_projet not in available_values:
            raise UnprocessableEntity(description="'contrainte_etre_sur_projet' doit être choisi parmi"
                                                  f"{available_values}.")


def task_assigner_controller(json_file: dict):
    """
    Controller du Task assigner.
    - vérifie le contenue du json en entrée
    -
    """
    logger_task_assigner.info("Appel du controller")
    front_end_request_content = FrontEndTaskAssignerRequestContent.deserialize(json_file)

    df_prj, df_cmp, df_tsk, df_dsp = fetch_task_assigner_data_to_back(
        backend_url=front_end_request_content.backend_url,
        backend_access_token=front_end_request_content.backend_access_token,
        date_start=front_end_request_content.date_start,
        date_end=front_end_request_content.date_end)

    check_data_consistency(df_prj, df_cmp, df_tsk, df_dsp)

    # calcul d'une solution
    try:
        solution = solveur(
            df_prj=df_prj,
            df_cmp=df_cmp,
            df_tsk=df_tsk,
            df_dsp=df_dsp,
            curseur=front_end_request_content.curseur,
            contrainte_etre_sur_projet=front_end_request_content.contrainte_etre_sur_projet,
            avantage_projet=front_end_request_content.avantage_projet,
        )
        return solution

    except Exception as e:
        logger_task_assigner.error("Crash du solveur", exc_info=str(e))
        raise SolverCrashException()


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
