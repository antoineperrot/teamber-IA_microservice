"""
Fonction d'optimisation des plannings
"""
import datetime

import pandas as pd
from numpy import round
from pandas import DataFrame
from api.config import config
from api.loggers import logger_planning_optimizer
from api.services.planning_optimizer.lib_planning_optimizer import optimize_one_planning,\
    NoAvailabilitiesException, ResultatCalcul
from api.string_keys import *


def make_global_stats_charts(global_stats: dict[int: DataFrame]):
    """Make global stats charts"""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    labels = ['total_worked_time', 'total_remaining_time']
    values = [global_stats[label] for label in labels]
    pie_trace = go.Pie(labels=labels, values=values, name="Time usage")

    hist_trace = go.Bar(y=global_stats['project']['pct_completion'].values * 100,
                        x=global_stats['project'].index.astype(str),
                        name="pct_completion")
    pie_trace2 = go.Pie(labels=global_stats['users'], values=global_stats['worked_time_users'], name="Worktime repartition")
    # create a subplot with two columns
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "histogram"}, {"type": "pie"}]])

    # add the traces to the subplot
    fig.add_trace(pie_trace, row=1, col=1)
    fig.add_trace(hist_trace, row=1, col=2)
    fig.add_trace(pie_trace2, row=1, col=3)

    # update the layout
    fig.update_layout(title='Sprint planning stats')

    fig.show()


def make_global_stats(users_stats: dict[int: DataFrame]) -> dict:
    """Statistiques globales sur les projets"""
    df_projects = [utl_stats["projects"] for utl_stats in users_stats.values()]
    df_all = pd.concat(df_projects, ignore_index=True)

    # we can then group the dataframe by "project" and sum the "length" column
    stats_by_project = df_all.groupby(key_evenement_project).agg({KEY_DUREE_EFFECTUEE: "sum", key_duree_evenement: "sum"})
    stats_by_project["pct_completion"] = round(stats_by_project[KEY_DUREE_EFFECTUEE] / stats_by_project[key_duree_evenement], 2)
    total_worked_time = round(sum([utl_stats["total_working_time"] for utl_stats in users_stats.values()]), 2)
    total_available_time = round(sum([utl_stats["total_available_time"] for utl_stats in users_stats.values()]), 2)
    worked_time_percent = round(total_worked_time / total_available_time, 2)
    global_stats = {"project": stats_by_project,
                    "total_worked_time": total_worked_time,
                    "total_available_time": total_available_time,
                    "total_remaining_time": total_available_time - total_worked_time,
                    "worked_time_percent": worked_time_percent,
                    "users": list(users_stats.keys()),
                    "worked_time_users": [user_stat["total_working_time"] for user_stat in users_stats.values()]}
    assert all(stats_by_project["pct_completion"] <= 1)
    assert all(stats_by_project["pct_completion"] >= 0)
    assert worked_time_percent >= 0
    assert worked_time_percent <= 1
    # print the resulting dataframe

    if bool(int(config["TEST_MODE"])):
        make_global_stats_charts(global_stats)
    return global_stats


def solver_planning_optimizer(
    working_times: dict[int: DataFrame],
    taches: dict[int: DataFrame],
    imperatifs: dict[int: DataFrame],
    date_start: datetime.datetime,
    date_end: datetime.datetime,
    parts_max_length: float,
    min_duration_section: float,
) -> dict[str: dict[int: ResultatCalcul]]:
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

    utilisateurs = list(taches.keys())
    utilisateurs.sort()

    optimized_plannings = {}
    users_stats = {}
    for i, utl in enumerate(utilisateurs):
        int_utl = int(utl)
        try:
            resultat = optimize_one_planning(
                working_times=working_times[utl],
                taches=taches[utl],
                imperatifs=imperatifs[utl],
                date_start=date_start,
                date_end=date_end,
                parts_max_length=parts_max_length,
                min_duration_section=min_duration_section,
                utilisateur_id=int_utl
            )
            optimized_plannings[int_utl] = resultat
            users_stats[int_utl] = resultat.stats
            logger_planning_optimizer.info(f"Optimisation des plannings: {i+1} sur {len(utilisateurs)} traité(s)."
                                           f"Utilisateur {utl}: planning optimisé.")

        except NoAvailabilitiesException:
            logger_planning_optimizer.warning(f"Optimisation des plannings: {i+1} sur {len(utilisateurs)} traité(s)."
                                              f"Utilisateur {utl}: Pas de disponibilités pour cet utilisateur,"
                                              f" impossible d'optimiser le planning.")
            optimized_plannings[int_utl] = ResultatCalcul(success=False,
                                                          message="No availibilities were found for this user given"
                                                                  " the sprint dates, the user working times and "
                                                                  "compulsory agenda events.",
                                                          stats=None,
                                                          events=None)

    global_stats = make_global_stats(users_stats=users_stats)

    return {"solution": optimized_plannings,
            "global_stats": global_stats}
