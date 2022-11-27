"""
Module contenant les fonctions de mockage de données pour la fonctionnalité Planning Optimizer.
"""
from typing import List
import numpy as np
import pandas as pd
from random import choices


def generate_unique_ids(n: int) -> List[int]:
    """
    Génère des listes aléatoires d'id
    """
    ids = []
    for i in range(n):
        rdm_id = np.random.randint(1000, 10000)
        while rdm_id in ids:
            rdm_id = np.random.randint(10, 1000)
        ids.append(rdm_id)
    ids = np.sort(ids)
    return ids


def mock_priorites_projets_projets(df_tsk: pd.DataFrame) -> dict:
    """
    Génère un dictionnaire aléatoire et pertinent de correspondances id_projet <-> niveau de priorités.

    :param df_tsk: DataFrame contenant les tâches à planifier.

    """
    liste_projets = df_tsk["evt_sfkprojet"].unique().astype(int)
    n_projets = len(liste_projets)
    n_prio = np.random.randint(n_projets // 2, n_projets)
    dict_prio = {id_projet: np.random.randint(0, n_prio) for id_projet in liste_projets}

    return dict_prio


def mock_df_tsk(dict_hor: dict) -> pd.DataFrame:
    """
    Prend un dictionnaire de vrais horaires utilisateurs et génère des tâches aléatoire sur des projets aléatoires.

    Exemple de sortie :
    	evt_dduree	evt_spkevenement	lgl_sfkligneparent	evt_sfkprojet
    0	0.25	476	24	3668
    1	0.50	496	3	3211
    2	2.75	570	1	3778
    3	3.50	696	10	2630
    4	1.75	839	1	2630
    ...	...	...	...	...
    295	0.25	9768	8	3668
    296	2.00	9807	8	1617
    297	2.75	9876	5	3211
    298	3.00	9957	10	3778
    299	3.25	9972	30	2630
    """
    liste_utl = list(dict_hor.keys())
    n_utl = len(liste_utl)
    n_tasks = 25 * n_utl
    n_projets = n_utl // 2 + 1
    ids_tasks = generate_unique_ids(n_tasks)
    ids_prj = generate_unique_ids(n_projets)
    duree_tasks = np.round(np.random.randint(1, 4 * 4, n_tasks) / 4, 2)

    task_utl = choices(liste_utl, k=n_tasks)
    task_prj = choices(ids_prj, k=n_tasks)
    # TODO: corriger la clé quand j'aurai la bonne
    out = pd.DataFrame({"evt_dduree": duree_tasks,
                        "evt_spkevenement": ids_tasks,
                        "lgl_sfkligneparent": task_utl,
                        "evt_sfkprojet": task_prj})

    return out
