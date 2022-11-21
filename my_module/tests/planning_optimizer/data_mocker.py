"""
Module contenant les fonctions de mockage de données pour la fonctionnalité Planning Optimizer.
"""
import pandas as pd
import numpy as np


def mock_dict_priorites_projets(df_tsk: pd.DataFrame) -> dict:
    """
    Génère un dictionnaire aléatoire et pertinent de correspondances id_projet <-> niveau de priorités.

    :param df_tsk: DataFrame contenant les tâches à planifier.

    """
    liste_projets = df_tsk['evt_sfkprojet'].unique().astype(int)
    n_projets = len(liste_projets)
    n_prio = np.random.randint(n_projets//2, n_projets)
    dict_prio = {id_projet: np.random.randint(0, n_prio) for id_projet in liste_projets}

    return dict_prio
