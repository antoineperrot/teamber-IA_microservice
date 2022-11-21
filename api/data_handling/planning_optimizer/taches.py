"""
Fonctions pour préparer les données taches brut de Wandeed à l'optimisation
"""

from typing import List, Tuple
import pandas as pd


def split_tsk_utl(dict_hor: dict, df_tsk: pd.DataFrame) -> Tuple[dict, List[int]]:
    """
    :param dict_hor: dictionnaire des horaires sortant de la fonction make_clean_hor
    :param df_tsk: pd.DataFrame des taches sur la période concernée

    :return task_to_optimize_dict: un dictionnaire {id_utl:taches_de_utl} à optimiser ensuite pour chaque utl
    :return utl_without_horaire: la liste des id_utl contenus dans df_tsk, pour qui on souhaiterait donc
    potentiellement optimiser les emplois du temps, mais pour qui on ne dispose pas des horaires de travail.
    """
    task_to_optimize_dict = {}  # {id_utilisateur: df_tache}

    utl_without_horaire = []
    for utl in df_tsk["lgl_sfkligneparent"].unique():
        if utl not in dict_hor.keys():
            # pas d'horaires dispo pour cet utilisateur -> impossible de lancer le programme
            utl_without_horaire.append(utl)
        else:
            df_tsk_utl = df_tsk.loc[
                df_tsk["lgl_sfkligneparent"] == utl,
            ]
            task_to_optimize_dict[utl] = df_tsk_utl

    return task_to_optimize_dict, utl_without_horaire


def make_clean_task(df_tsk: pd.DataFrame):
    """
    Enlève les lignes contenant des NaN.
    """
    df_tsk.dropna(inplace=True)
    df_tsk['evt_sfkprojet'] = df_tsk['evt_sfkprojet'].astype(int)
    return df_tsk


def map_priorite(df_tsk: pd.DataFrame, dict_priorites: dict) -> pd.DataFrame:
    """
    :param df_tsk: pd.DataFrame contenant les taches: (id, duree, id_utl, id_projet)
    :param dict_priorites: dict faisant le mapping id_projet <-> niveau de priorité du projet.

    -> le niveau de priorité de la tâches est alors défini comme étant celui du projet auquel la tâche se réfère.

    :return df_tsk: idem que df_tsk input, avec les niveaux de priorités des tâches en plus.
    """
    df_tsk['priorite'] = df_tsk['evt_sfkprojet'].map(dict_priorites)
    return df_tsk
