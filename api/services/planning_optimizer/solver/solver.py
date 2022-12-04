"""
Module d'optimisation.
"""
import pandas as pd
from api.services.planning_optimizer.solver.planning.horaires import make_base
from api.services.planning_optimizer.solver.tools.taches import split_tasks


def solver(horaires: pd.DataFrame,
           taches: pd.DataFrame,
           imperatifs: pd.DataFrame | None,
           date_start: str,
           date_end: str,
           duree_min_morceau: float,
           longueur_min_ph: float):
    """
    Prend les données d'un utilisateur et renvoie son emploi du temps optimisé.
    """

    base = make_base(horaires, date_start, date_end, longueur_min_ph)
    # base = add_imperatifs(base, imperatifs, longueur_min_ph)
    splitted_taches = split_tasks(taches, duree_min_morceau)



