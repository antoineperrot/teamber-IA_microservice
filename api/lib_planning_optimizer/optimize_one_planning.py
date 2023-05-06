"""
Module d'optimisation.
"""
import datetime
import pandas as pd

from api.config import config
from api.lib_planning_optimizer.planning.horaires import NoAvailabilitiesException, compute_availabilities
from api.lib_planning_optimizer.planning.planning import SimulatedAnnealingPlanningOptimizer
from api.lib_planning_optimizer.planning.solution_interpreter import make_stats
from api.lib_planning_optimizer.resultat_calcul import ResultatCalcul
from api.lib_planning_optimizer.tools import split_tasks, make_timeline
from api.string_keys import *


def optimize_one_planning(
    working_times: pd.DataFrame,
    taches: pd.DataFrame,
    imperatifs: pd.DataFrame | None,
    date_start: datetime.datetime,
    date_end: datetime.datetime,
    parts_max_length: float,
    min_duration_section: float,
    utilisateur_id: int,
    save_optimization_statistics: bool = False,
) -> ResultatCalcul:
    """
    Prend les données d'un utilisateur et renvoie son emploi du temps optimisé.
    """
    availabilities = compute_availabilities(
        working_times=working_times,
        imperatifs=imperatifs,
        date_start=date_start,
        date_end=date_end,
        min_duration_section=min_duration_section
    )

    if len(availabilities) == 0:
        raise NoAvailabilitiesException()
    splitted_tasks = split_tasks(taches, parts_max_length)

    optimizer = SimulatedAnnealingPlanningOptimizer(
        availabilities=availabilities,
        tasks=splitted_tasks,
        save_for_testing=save_optimization_statistics
    )

    optimizer.optimize(n_iterations_per_task=250)
    events, ordonnancement = optimizer.schedule_events()
    stats = make_stats(events=events, tasks=taches, availabilities=availabilities)
    events = events.drop(KEY_ID_PART, axis="columns")
    keys = [key_evenement, key_evenement_project, KEY_PROJECT_PRIORITY, KEY_START, KEY_END]
    events = events[keys]

    out = ResultatCalcul(success=True, events=events, stats=stats)

    if bool(int(config["SHOW_PLOTS"])):
        make_timeline(
            availabilities=availabilities, events=events, imperatifs=imperatifs, utilisateur_id=utilisateur_id)
    return out
