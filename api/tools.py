"""
Contient des petites fonctions utiles, notemment:
les fonctions de split des données pour planning_optimizer et task_assigner
une fois les données reçues de get_data_planning_optimizer et get_data_task_assigner.
"""
import pandas as pd
import simplejson
from typing import Tuple

def return_json(response):
    """
    Standard json encoder fails to encode np.NaN.
    This function replaces NaNs with "null", and returns a JSON formatted string.
    """
    return simplejson.dumps(response, ignore_nan=True)


def split_data_task_assigner(data: dict) -> Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame,pd.DataFrame]:
    """
    Split les datas reçues à la sortie de get_data_task_assigner en 4 pd.DataFrame:

    TODO: à compléter

    :return df_prj:

    :return df_cmp:

    :return df_tsk:

    :return df_tsk:

    """
    # recuperation matrice_projet
    df_prj = pd.DataFrame(data["matrice_projet"])
    # recuperation matrice_competence : on oublie les compétences pour lesquels les utl sont indéfinis
    df_cmp = (
        pd.DataFrame(data["matrice_competence"])
        .dropna()
        .reset_index(drop=True)
        .astype(int)
    )
    # recuperation des taches à assigner :
    df_tsk = pd.DataFrame(data["taches"])
    # recuperation des disponibilites utl :
    df_dsp = pd.DataFrame(data["dispos_utilisateurs"])

    return df_prj, df_cmp, df_tsk, df_tsk


def split_data_planning_optimizer(
    data: dict,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split les datas reçues à la sortie de get_data_planning_optimizer en 3 pd.DataFrame:
    :return df_imp:
        TODO: à compléter

    :return df_hor: dataframe contenant les horaires des utilisateurs
        "epu_sfkutilisateur"  -> id de l'utilisateur
        "epl_xdebutperiode"   -> debut de période d'application de l'horaire
        "epl_xfinperiode"     -> fin de période d'application de l'horaire
        "epl_employe_horaire" -> horaire de l'employe

    :return df_tsk:
        "evt_dduree"          -> duree (en h) de la tâche
        "evt_spkevenement"    -> id de la tâche
        "lgl_sfkligneparent"  -> utilisateur concerné
        "evt_sfkprojet"       -> projet de rattachement de la tâche

    """
    df_imp = pd.DataFrame(data["imperatifs"])
    df_hor = pd.DataFrame(data["horaires"]).reindex(
        columns=[
            "epu_sfkutilisateur",
            "epl_xdebutperiode",
            "epl_xfinperiode",
            "epl_employe_horaire",
        ]
    )
    df_hor.epl_xdebutperiode = pd.to_datetime(df_hor.epl_xdebutperiode).dt.date
    df_hor.epl_xfinperiode = pd.to_datetime(df_hor.epl_xfinperiode).dt.date
    df_hor = df_hor.sort_values(
        by=["epu_sfkutilisateur", "epl_xdebutperiode"]
    ).reset_index(drop=True)
    df_tsk = pd.DataFrame(data["taches"])
    return df_imp, df_hor, df_tsk

