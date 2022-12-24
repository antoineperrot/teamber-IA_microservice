"""
Module d'optimisation.
"""
import pandas as pd

from api.services.planning_optimizer.solver.planning.horaires import (
    compute_availabilities,
)
from api.services.planning_optimizer.solver.planning.planning import (
    SimulatedAnnealingPlanningOptimizer,
)
from api.services.planning_optimizer.solver.tools.taches import split_tasks

from api.services.planning_optimizer.solver.planning.solution_interpreter import make_stats


def solver(
    horaires: pd.DataFrame,
    taches: pd.DataFrame,
    imperatifs: pd.DataFrame | None,
    date_start: str,
    date_end: str,
    parts_max_length: float,
    min_duration_section: float,
    save_optimization_statistics: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prend les données d'un utilisateur et renvoie son emploi du temps optimisé.
    """

    availabilities = compute_availabilities(
        horaires, imperatifs, date_start, date_end, min_duration_section
    )
    splitted_tasks = split_tasks(taches, parts_max_length)

    optimizer = SimulatedAnnealingPlanningOptimizer(
        availabilities=availabilities, tasks=splitted_tasks, save_for_testing=save_optimization_statistics
    )

    optimizer.optimize(n_iterations_per_task=250)
    events, ordonnancement = optimizer.schedule_events()
    stats = make_stats(events, taches)

    return events, stats
