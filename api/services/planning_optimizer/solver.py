"""
Fonction d'optimisation des plannings
"""
import datetime

from pandas import DataFrame
from api.services.planning_optimizer.lib_planning_optimizer import optimize_one_planning,\
    NoAvailabilitiesException, ResultatCalcul


def solver_planning_optimizer(
    working_times: dict[int: DataFrame],
    taches: dict[int: DataFrame],
    imperatifs: dict[int: DataFrame],
    date_start: datetime.datetime,
    date_end: datetime.datetime,
    parts_max_length: float,
    min_duration_section: float,
) -> dict[int: ResultatCalcul]:
    """
    Fonction optimisant les emplois du temps de chacun des utilisateurs.

    :param working_times: dict de la forme {id (int): horaire (Dataframe)} contenant les horaires des utilisateurs.
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
        int_utl = int(utl)
        try:
            optimized_plannings[int_utl] = optimize_one_planning(
                working_times=working_times[utl],
                taches=taches[utl],
                imperatifs=imperatifs[utl],
                date_start=date_start,
                date_end=date_end,
                parts_max_length=parts_max_length,
                min_duration_section=min_duration_section,
            )
        except NoAvailabilitiesException:
            optimized_plannings[int_utl] = ResultatCalcul(success=False,
                                                          message="No availibilities were found for this user given"
                                                                  " the sprint dates, the user working times and "
                                                                  "compulsory agenda events.",
                                                          stats=None,
                                                          events=None)

    return optimized_plannings
