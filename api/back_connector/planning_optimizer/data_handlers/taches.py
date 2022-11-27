"""
Fonctions pour préparer les données taches brut de Wandeed à l'optimisation
"""
import pandas as pd


def split_n_clean_taches(df_tsk: pd.DataFrame) -> dict:
    """
    :param df_tsk: pd.DataFrame des taches sur la période concernée

    :return taches: un dictionnaire {id_utl:taches_de_utl} à optimiser ensuite pour chaque utl
    :return missing_data_utl: la liste des id_utl pour qui l'on manque de données: soit on ne connaît pas leurs
    horaires, soit ils n'ont pas de tâches assignées dans df_tsk.

    Enlève les lignes contenant des NaN du df_tsk
    """

    df_tsk.dropna(inplace=True)
    df_tsk["evt_sfkprojet"] = df_tsk["evt_sfkprojet"].astype(int)
    taches = {}  # {id_utilisateur: df_tache}

    # TODO: corriger la clé quand j'aurai la bonne
    for utl in df_tsk["lgl_sfkligneparent"].unique():
        df_tsk_utl = df_tsk.loc[
            df_tsk["lgl_sfkligneparent"] == utl,
        ]
        if len(df_tsk_utl) > 0:
            # si l'utilisateur a effectivement des tâches qui lui sont assignées, on va pouvoir optimizer
            # son emploi du temps.
            taches[utl] = df_tsk_utl.reset_index(drop=True)
    return taches


def map_priorites_projets(df_tsk: pd.DataFrame, priorites_projets: dict) -> pd.DataFrame:
    """
    :param df_tsk: pd.DataFrame contenant les taches: (id, duree, id_utl, id_projet)
    :param priorites_projets: dict faisant le mapping id_projet <-> niveau de priorité du projet.

    -> le niveau de priorité de la tâches est alors défini comme étant celui du projet auquel la tâche se réfère.
    -> les tâches faisant référence à des projets pour lesquels aucun niveau de priorité n'est défini se verront
    attribuer le niveau de priorité le plus bas.

    :return df_tsk: idem que df_tsk input, avec les niveaux de priorités des tâches en plus.
    """

    niveau_min_priorite = int(max(list(priorites_projets.values())) + 1) if len(priorites_projets) > 0 else 0
    df_tsk["priorite"] = df_tsk["evt_sfkprojet"].map(priorites_projets).fillna(niveau_min_priorite)
    return df_tsk
