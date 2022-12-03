from api.services.planning_optimizer.solver import solver


def optimize_plannings(horaires: dict, taches: dict, imperatifs: dict, date_start: str, date_end: str,
                       duree_min_morceau: float = 1.0):
    """
    Fonction optimisant les emplois du temps de chacun des utilisateurs.
    """

    utilisateurs = set(taches.keys())

    optimized_plannings = {}
    for utl in utilisateurs:
        optimized_plannings[utl] = solver(horaires[utl],
                                          taches[utl],
                                          imperatifs[utl],
                                          date_start,
                                          date_end,
                                          duree_min_morceau)
