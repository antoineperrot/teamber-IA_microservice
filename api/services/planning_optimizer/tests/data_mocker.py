"""
Module contenant les fonctions de mockage de données pour la fonctionnalité Planning Optimizer.
"""
from typing import List
import numpy as np
import pandas as pd
from random import choices

from api.back_connector.planning_optimizer.data_handlers.taches import split_n_clean_taches, map_priorites_projets
from api.services.planning_optimizer.tests.test_data.default_horaires import default_horaires


def mock_back_data(date_start: str, date_end: str, avg_n_users: int = 5, avg_n_tasks: int = 25):
    """
    Mock toutes les données censées provenir du front/du back Teamber.
    """

    print("Attention, les impératis mockées sont disponibles uniquement entre 2022-09-05 08:30:00+0000 et \
          2022-09-08 15:30:00+0000")
    n_users = int(np.random.normal(avg_n_users, avg_n_users/5))
    utls = generate_unique_ids(n_users)
    df_tsk = mock_df_tsk(utls, avg_n_tasks)
    priorites_projets = mock_priorites_projets(df_tsk)
    df_tsk = map_priorites_projets(df_tsk, priorites_projets)
    taches = split_n_clean_taches(df_tsk)
    horaires = {utl: default_horaires for utl in utls}
    imperatifs = {utl: mock_imperatifs(utl, date_start, date_end) for utl in utls}
    return taches, horaires, imperatifs


def mock_priorites_projets(df_tsk: pd.DataFrame) -> dict:
    """
    Génère un dictionnaire aléatoire et pertinent de correspondances id_projet <-> niveau de priorités.

    :param df_tsk: DataFrame contenant les tâches à planifier.

    """
    liste_projets = df_tsk["evt_sfkprojet"].unique().astype(int)
    n_projets = len(liste_projets)
    n_prio = np.random.randint(n_projets // 2, n_projets)
    priorites_projets = {id_projet: np.random.randint(0, n_prio) for id_projet in liste_projets}

    return priorites_projets


def mock_df_tsk(liste_utl: List[int], avg_n_tasks: int = 25) -> pd.DataFrame:
    """
    Prend une liste d'utilisateurs liste_utl et génère des tâches aléatoire sur des projets aléatoires.

    Exemple de sortie :
    	evt_dduree	evt_spkevenement	 lgl_sfkligneparent	evt_sfkprojet
    0	0.25	    476	                 24	                3668
    1	0.50	    496	                 3	                3211
    2	2.75	    570	                 1	                3778
    3	3.50	    696	                 10	                2630
    4	1.75	    839	                 1	                2630
    ...	...		    ...	                 ...                ...
    295	0.25	    9768	             8	                3668
    296	2.00	    9807	             8	                1617
    297	2.75	    9876	             5	                3211
    298	3.00	    9957	             10	                3778
    299	3.25	    9972	             30	                2630
    """

    n_utl = len(liste_utl)
    n_tasks = int(np.random.normal(avg_n_tasks, avg_n_tasks/5))
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


def mock_imperatifs(utl: int, date_start, date_fin: str):
    n_evt = 7
    out = pd.DataFrame({"evt_spkevenement": generate_unique_ids(n_evt),
                        "evt_sfkprojet": generate_unique_ids(n_evt),
                        "lgl_sfkligneparent": [utl] * n_evt,
                        "evt_xdate_debut": [pd.Timestamp("2022-09-05 08:30:00+0000"),
                                            pd.Timestamp("2022-09-05 15:00:00+0000"),
                                            pd.Timestamp("2022-09-06 09:00:00+0000"),
                                            pd.Timestamp("2022-09-07 07:00:00+0000"),
                                            pd.Timestamp("2022-09-07 07:30:00+0000"),
                                            pd.Timestamp("2022-09-07 13:00:00+0000"),
                                            pd.Timestamp("2022-09-08 14:30:00+0000")],
                        "evt_xdate_fin": [pd.Timestamp("2022-09-05 09:30:00+0000"),
                                          pd.Timestamp("2022-09-05 17:00:00+0000"),
                                          pd.Timestamp("2022-09-06 10:00:00+0000"),
                                          pd.Timestamp("2022-09-07 08:15:00+0000"),
                                          pd.Timestamp("2022-09-07 08:45:00+0000"),
                                          pd.Timestamp("2022-09-07 14:10:00+0000"),
                                          pd.Timestamp("2022-09-08 15:30:00+0000")]})

    out = out.loc[(out['evt_xdate_fin']>=date_start) & (out['evt_xdate_debut'] <= date_fin)]
    out.reset_index(drop=True, inplace=True)
    return out

