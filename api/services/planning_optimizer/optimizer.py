from api.services.planning_optimizer.solver import solver


def optimize_plannings(horaires: dict, taches: dict, imperatifs: dict, date_start: str, date_end: str,
                       parts_max_length: float = 1.0, min_duration_section: float = 0.5):
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
                                          parts_max_length,
                                          min_duration_section=min_duration_section)
