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
        if not utl in dict_hor.keys():
            # pas d'horaires dispo pour cet utilisateur -> impossible de lancer le programme
            utl_without_horaire.append(utl)
        else:
            df_tsk_utl = df_tsk.loc[
                df_tsk["lgl_sfkligneparent"] == utl,
            ]
            task_to_optimize_dict[utl] = df_tsk_utl

    return task_to_optimize_dict, utl_without_horaire
