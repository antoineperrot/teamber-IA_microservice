"""
Module d'optimisation.
"""
import pandas as pd

from api.services.planning_optimizer.solver.planning.horaires import compute_availabilities
from api.services.planning_optimizer.solver.planning.planning import SimulatedAnnealingPlanningOptimizer
from api.services.planning_optimizer.solver.tools.taches import split_tasks


def solver(horaires: pd.DataFrame,
           taches: pd.DataFrame,
           imperatifs: pd.DataFrame | None,
           date_start: str,
           date_end: str,
           parts_max_length: float,
           min_duration_section: float):
    """
    Prend les données d'un utilisateur et renvoie son emploi du temps optimisé.
    """

    availabilities = compute_availabilities(horaires, imperatifs, date_start, date_end, min_duration_section)
    splitted_tasks = split_tasks(taches, parts_max_length)

    optimizer = SimulatedAnnealingPlanningOptimizer(availabilities=availabilities,
                                                    tasks=splitted_tasks)

    optimizer.optimize(n_iterations_per_task=250)
    events = optimizer.schedule_events()
    #unfilled_tasks = optimizer.get_unfilled_task()

    return events, None, availabilities
