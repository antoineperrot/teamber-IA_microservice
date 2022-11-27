"""
Module d'optimisation.
"""
import pandas as pd
from api.services.planning_optimizer.solver.planning.tools import make_df_ph, add_imperatifs


def solver(horaire: pd.DataFrame,
           tache: pd.DataFrame,
           imperatif: pd.DataFrame | None,
           date_start: str,
           date_end: str,
           duree_min_morceau: float,
           longueur_min_ph : float):

    df_ph = make_df_ph(horaire, date_start, date_end, longueur_min_ph)
    df_ph = add_imperatifs(df_ph, imperatif, longueur_min_ph)


