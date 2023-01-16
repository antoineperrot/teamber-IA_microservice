"""
Fonction d'optimisation des plannings
"""
from pandas import DataFrame

from api.services.planning_optimizer.lib_planning_optimizer import optimize_one_planning


def solver_planning_optimizer(
    horaires: dict[int: DataFrame],
    taches: dict[int: DataFrame],
    imperatifs: dict[int: DataFrame],
    date_start: str,
    date_end: str,
    parts_max_length: float,
    min_duration_section: float,
) -> dict[int:DataFrame]:
    """
    Fonction optimisant les emplois du temps de chacun des utilisateurs.

    :param horaires: dict de la forme {id (int): horaire (Dataframe)} contenant les horaires des utilisateurs.
    :param taches: dict de la forme {id (int): taches (Dataframe)} contenant les taches des utilisateurs.
    :param imperatifs: dict de la forme {id (int): imperatifs (Dataframe)} contenant les imperatifs des utilisateurs.
    :param date_start: str au format ISO, date de début du sprint
    :param date_end: str au format ISO, date de fin du sprint
    :param min_duration_section: float indiquant la durée minimale en heures d'une plage horaire sur laquelle
    on va planifier des tâches.
    :param parts_max_length: float (en heures) de la durée maximales des nouvelles tâches
    """

    utilisateurs = set(taches.keys())

    optimized_plannings = {}
    for utl in utilisateurs:
        optimized_plannings[utl] = optimize_one_planning(
            horaires=horaires[utl],
            taches=taches[utl],
            imperatifs=imperatifs[utl],
            date_start=date_start,
            date_end=date_end,
            parts_max_length=parts_max_length,
            min_duration_section=min_duration_section,
        )
    return optimized_plannings
