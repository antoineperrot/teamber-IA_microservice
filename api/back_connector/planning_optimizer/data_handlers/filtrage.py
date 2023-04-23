"""
Module de filtrage des données pour la fonctionnalité Planning Optimizer.
Philosohie: une fois les données récupérées auprès du back, ne garder que ce qui pas pouvoir être processé,
optimisé, et jeter les données inutiles. Par exemple:
- les utilisateurs pour lesquels on a des tâches mais pas d'horaires
- les utilisateurs pour lesquels on a pas de tâches.
"""
import pandas as pd

from api.back_connector.planning_optimizer.data_handlers.horaires import (
    make_clean_hor,
)
from api.back_connector.planning_optimizer.data_handlers.imperatifs import (
    split_n_clean_impertifs,
)
from api.back_connector.planning_optimizer.data_handlers.taches import (
    split_n_clean_taches,
    map_key_project_prioritys_projets,
)
from api.loggers import logger_planning_optimizer
from api.tools import get_defaults_horaires


def filtre(
    df_imp: pd.DataFrame,
    df_hor: pd.DataFrame,
    df_tsk: pd.DataFrame,
    key_project_prioritys_projets: dict[int: int],
) -> tuple[dict[int: pd.DataFrame],
           dict[int: pd.DataFrame],
           dict[int: pd.DataFrame],
           list[int]]:
    """
    Filtre et nettoie les données brutes reçues depuis le BACK Wandeed. Ne renvoie que le nécessaire à
    l'optimisation.
    """

    df_tsk = map_key_project_prioritys_projets(df_tsk, key_project_prioritys_projets)
    taches = split_n_clean_taches(df_tsk)
    imperatifs = split_n_clean_impertifs(df_imp)
    horaires = make_clean_hor(df_hor)

    logger_planning_optimizer.info("filtrage des données du back.")

    all_users = list(taches.keys())
    all_users.sort()
    all_users = set(all_users)
    users_with_horaires = set(all_users) & set(horaires.keys())
    utilisateurs_avec_taches_sans_horaires = list(
        set(all_users) - users_with_horaires
    )

    for utl in utilisateurs_avec_taches_sans_horaires:
        logger_planning_optimizer.info(
            f"Mock des horaires de travail de l'utilisateur {utl}"
        )
        horaires[utl] = get_defaults_horaires()

    # puis recoupage
    for user in all_users:
        if user not in imperatifs.keys():
            imperatifs[user] = None

    horaires = {key: horaires[key] for key in all_users}

    return imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires
