"""
Module contenant les fonctions de mockage de données pour la fonctionnalité Planning Optimizer.
"""
import datetime
import random

import numpy as np
import pandas as pd

from api.lib_planning_optimizer.tests.test_data import default_horaires
from api.string_keys import *
from api.back_connector.planning_optimizer.data_handlers.taches import (
    split_n_clean_taches,
    map_key_project_prioritys_projets,
)
from api.loggers import logger_planning_optimizer


def mock_key_project_prioritys_projets(df_tsk: pd.DataFrame) -> dict:
    """
    Génère un dictionnaire aléatoire et pertinent de correspondances id_projet <-> niveau de priorités.

    :param df_tsk: DataFrame contenant les tâches à planifier.

    """
    logger_planning_optimizer.debug("mock priorités projets")
    liste_projets = df_tsk[key_evenement_project].unique().astype(int)
    n_projets = len(liste_projets)
    n_prio = max(np.random.randint(n_projets // 2, n_projets), 1)
    key_project_prioritys_projets = {
        id_projet: np.random.randint(0, n_prio) for id_projet in liste_projets
    }

    return key_project_prioritys_projets


def mock_df_tsk(liste_utl: list[int], avg_n_tasks: int = 25) -> pd.DataFrame:
    """
    Prend une liste d'utilisateurs liste_utl et génère des tâches aléatoire sur des projets aléatoires.

    Exemple de sortie :
        key_duree_evenement	key_evenement	 key_competence	key_evenement_project
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
    logger_planning_optimizer.debug("mock taches")
    n_utl = len(liste_utl)
    n_tasks = max(1, int(np.random.normal(avg_n_tasks, avg_n_tasks / 5)))
    n_projets = n_utl * 3 + 1
    ids_tasks = generate_unique_ids(n_tasks)
    ids_prj = generate_unique_ids(n_projets)
    duree_tasks = np.round(np.random.randint(1, 4 * 4, n_tasks) / 4, 2)

    task_utl = random.choices(liste_utl, k=n_tasks)
    task_prj = random.choices(ids_prj, k=n_tasks)
    # TODO: corriger la clé quand j'aurai la bonne
    out = pd.DataFrame(
        {
            key_duree_evenement: duree_tasks,
            key_evenement: ids_tasks,
            key_competence: task_utl,
            key_evenement_project: task_prj,
        }
    )

    return out


def mock_back_data(
    date_start: datetime.datetime,
    date_end: datetime.datetime,
    avg_n_users: int = 5,
    avg_n_tasks: int = 25,
) -> tuple[dict[int: pd.DataFrame], dict[int: pd.DataFrame], dict[int: pd.DataFrame], list]:
    """
    Mock toutes les données censées provenir du front/du back Teamber.
    """

    logger_planning_optimizer.info("mock données back")
    n_users = int(np.random.normal(avg_n_users, avg_n_users / 5))
    utls = generate_unique_ids(n_users)
    df_tsk = mock_df_tsk(utls, avg_n_tasks)
    key_project_prioritys_projets = mock_key_project_prioritys_projets(df_tsk)
    df_tsk = map_key_project_prioritys_projets(df_tsk, key_project_prioritys_projets)
    taches = split_n_clean_taches(df_tsk)
    horaires = {utl: default_horaires for utl in utls}
    imperatifs = {utl: mock_imperatifs(utl, date_start, date_end) for utl in utls}
    return imperatifs, horaires, taches, []


def generate_unique_ids(n: int) -> list[int]:
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


def mock_imperatifs(utl: int,
                    date_start: datetime.datetime,
                    date_fin: datetime.datetime) -> pd.DataFrame:
    """Mock des impératifs"""
    n_imperatifs = 7
    logger_planning_optimizer.debug("mock impératifs projets")

    start_date = date_start.date()
    end_date = date_fin.date()
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    imperatifs_datetimes_start = []
    imperatifs_datetimes_end = []
    for i in range(n_imperatifs):
        random_second = random.randrange(int_delta) if int_delta > 0 else 0
        random_date_imperatifs = start_date + datetime.timedelta(seconds=random_second)
        hour_start = np.random.randint(7, 19)
        minute_start = np.random.randint(0, 12) * 5
        random_datetime_start_imp = datetime.datetime(random_date_imperatifs.year,
                                                      random_date_imperatifs.month,
                                                      random_date_imperatifs.day,
                                                      hour_start,
                                                      minute_start)
        random_datetime_end_imp = random_datetime_start_imp + datetime.timedelta(minutes=(1 + np.random.poisson(7)) * 5)

        imperatifs_datetimes_start.append(random_datetime_start_imp)
        imperatifs_datetimes_end.append(random_datetime_end_imp)

    imperatifs_datetimes_start = pd.to_datetime(imperatifs_datetimes_start)
    imperatifs_datetimes_end = pd.to_datetime(imperatifs_datetimes_end)

    out = pd.DataFrame(
        {
            key_evenement: generate_unique_ids(n_imperatifs),
            key_evenement_project: generate_unique_ids(n_imperatifs),
            key_competence: [utl] * n_imperatifs,
            key_evenement_date_debut: list(imperatifs_datetimes_start),
            key_evenement_date_fin: list(imperatifs_datetimes_end),
        }
    )

    out = out.loc[
        (out[key_evenement_date_fin] >= date_start) & (out[key_evenement_date_debut] <= date_fin)
        ]
    out = out.sort_values(by=key_evenement_date_debut)
    out.reset_index(drop=True, inplace=True)
    return out
