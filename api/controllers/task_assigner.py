from datetime import datetime
from werkzeug.exceptions import UnprocessableEntity
from api.back_connector.task_assigner.task_assigner import fetch_task_assigner_data_to_back


class FrontEndRequestContent:
    """Classe contenant ce les infos que doit faire parvenir le front lors d'un appel à TaskAssigner"""
    def __init__(self,
                 backend_access_token: str,
                 backend_url: str,
                 date_start: str,
                 date_end: str,
                 curseur: float = 0.0,
                 contrainte_etre_sur_projet: str = "de_preference",
                 avantage_projet: float = 1.0):
        self.backend_access_token = backend_access_token
        self.backend_url = backend_url
        self.date_start = date_start
        self.date_end = date_end
        self.curseur = curseur
        self.contrainte_etre_sur_projet = contrainte_etre_sur_projet
        self.avantage_projet = avantage_projet

    @staticmethod
    def deserialize(cls, json: dict):
        """Méthode de désérialisation"""
        out = FrontEndRequestContent(backend_access_token=json["backend_access_token"],
                                     backend_url=json["backend_url"],
                                     date_start=json["date_start"],
                                     date_end=json["date_end"],
                                     curseur=json["curseur"],
                                     contrainte_etre_sur_projet=json["contrainte_etre_sur_projet"],
                                     avantage_projet=json["avantage_projet"])

        # TODO : assertion des paramètres

        return out

    def _cast_values(self):
        try:
            self.backend_access_token = str(self.backend_access_token)
            self.backend_url = str(self.backend_url)
            self.date_start = str(self.date_start)
            self.date_end = str(self.date_end)
            self.curseur = float(self.curseur)
            self.contrainte_etre_sur_projet = str(self.contrainte_etre_sur_projet)
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




def task_assigner_controller(json_file: dict):
    """
    Controller du Task assigner.
    - vérifie le contenue du json en entrée
    -
    """
    front_end_request_content = FrontEndRequestContent.deserialize(json_file)
    front_end_request_content.check()

    data_task_assigner = fetch_task_assigner_data_to_back(backend_access_token, date_start, date_end, backend_url)

    df_prj, df_cmp, df_tsk, df_dsp = split_data_task_assigner(data_task_assigner)

    check_validity_data_assigner(df_prj, df_cmp, df_tsk, df_dsp)

    # calcul d'une solution
    solution = solveur(
        df_prj,
        df_cmp,
        df_tsk,
        df_dsp,
        curseur,
        contrainte_etre_sur_projet,
        avantage_projet,
    )
    pass


def check_validity_data_assigner(
        df_prj: pd.DataFrame,
        df_cmp: pd.DataFrame,
        df_tsk: pd.DataFrame,
        df_dsp: pd.DataFrame,
):
    """
    Vérifie que les données reçues sont cohérentes.
    """
    if len(df_cmp) == 0:
        raise UnprocessableEntity(description="Pas de matrice de compétence disponible.")
    if len(df_tsk) == 0:
        raise UnprocessableEntity(description="Pas de tâches à assigner.")
