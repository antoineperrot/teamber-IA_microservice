"""
Module de traduction de la solution mathématique en une sortie DataFrame interprétable.
"""
import datetime
import numpy as np
import pandas as pd

from api.services.planning_optimizer.solver.planning.ordonnancement import (
    Ordonnancement,
)


def get_next_part(i_current_part: int, parts: pd.DataFrame) -> int:
    """
    :param i_current_part: index de la ligne courante dans le dataframe
    :param parts: dataframe contenant les morceaux à fusionner

    :return i_next_part: index de la première partie du prochain événement,
        ou len(parts) si arrive au bparts du df.
    :return i_next_part: première partie du prochain événement ou dernière partie du df si arrive au bparts du df.
    """
    current_part = parts.iloc[i_current_part]
    i_next_part = i_current_part + 1
    next_part = parts.iloc[i_next_part if i_next_part < len(parts) else len(parts) - 1]

    while (
        next_part["start"] == current_part["end"]
        and next_part["evt_spkevenement"] == current_part["evt_spkevenement"]
        and i_next_part < len(parts)
    ):
        i_next_part = i_next_part + 1
        next_part = parts.iloc[
            i_next_part if i_next_part < len(parts) else len(parts) - 1
        ]
    return i_next_part


def add_event(
    parts: pd.DataFrame | None = None,
    i_current_part: int | None = None,
    i_next_part: int | None = None,
    events: dict[str:list] | None = None,
) -> dict[str:list]:
    """
    :param parts: dataframe contenant les parties à regrouper en événement.
    :param i_current_part: index de la partie courante dans le dataframe
    :param i_next_part: index de la partie du prochain événement à regrouper
    :param events: dictionnaire contenant les événements déjà regroupés. Si None,
        initialise ce dictionnaire

    :return events: dictionnaire contenant les événements passées en entrée
        augmenté du nouvel événement.
    """

    if (
        events is None
        and i_current_part is None
        and i_next_part is None
        and parts is None
    ):
        events = {
            "start": [],
            "end": [],
            "evt_spkevenement": [],
            "evt_sfkprojet": [],
            "priorite": [],
        }
        return events

    current_part = parts.iloc[i_current_part]
    i_end_part = i_next_part - 1 if i_next_part > i_current_part else len(parts) - 1
    end_part = parts.iloc[i_end_part]
    if i_next_part > i_current_part + 1:
        events["start"].append(current_part["start"])
        events["end"].append(end_part["end"])
        events["evt_spkevenement"].append(current_part["evt_spkevenement"])
        events["evt_sfkprojet"].append(current_part["evt_sfkprojet"])
        events["priorite"].append(current_part["priorite"])
    else:
        events["start"].append(current_part["start"])
        events["end"].append(current_part["end"])
        events["evt_spkevenement"].append(current_part["evt_spkevenement"])
        events["evt_sfkprojet"].append(current_part["evt_sfkprojet"])
        events["priorite"].append(current_part["priorite"])

    return events


def move_indexes_forward(
    parts: pd.DataFrame,
    i_current_part: int | None = None,
    i_next_part: int | None = None,
) -> tuple[int, int]:
    """
    Incrémente ou initialise les indexs s'ils ne sont pas précisés.

    :param parts: dataframe contenant les parties à regrouper en événement.
    :param i_current_part: index de la partie courante dans le dataframe
    :param i_next_part: index de la partie du prochain événement à regrouper
    """
    if i_current_part is None and i_next_part is None:
        i_current_part = 0
        i_next_part = min(1, len(parts) - 1)
        return i_current_part, i_next_part

    if i_next_part > i_current_part + 1:
        i_current_part = i_next_part
        i_next_part = i_next_part + 1
    else:
        i_current_part = i_next_part
        i_next_part = min(i_next_part + 1, len(parts) - 1)
    return i_current_part, i_next_part


def make_events(parts: pd.DataFrame) -> pd.DataFrame:
    """
    Regroupe des parties de tâches adjacentes dans le temps en des événements distincts.

    :param parts: dataframe contenant les parties à regrouper en événement.
    :return events: dataframe des événements regroupés.
    """
    i_current_part, i_next_part = move_indexes_forward(parts=parts)
    events = add_event()
    while i_current_part < len(parts):
        i_next_part = get_next_part(i_current_part=i_current_part, parts=parts)
        events = add_event(
            parts=parts,
            i_current_part=i_current_part,
            i_next_part=i_next_part,
            events=events,
        )
        i_current_part, i_next_part = move_indexes_forward(
            parts=parts, i_current_part=i_current_part, i_next_part=i_next_part
        )

    events = pd.DataFrame(events)
    return events


def schedule_parts(
    availabilities: pd.DataFrame, tasks: pd.DataFrame, ordonnancement: Ordonnancement
):
    """
    Rempli les plages horaires de disponibilités avec un ordonnancement de tâches.
    :param availabilities: dataframe des plages horaires de disponibilités
    :param tasks: dataframe des tâches contenant les parties de tâches
    :param ordonnancement: objet Ordonnancement contenant un ordonnancement quasi-optimal des parties de tâches.

    :return scheduled_tasks_parts: dataframe contenant les parties de tâches planifiées.
    """
    scheduled_tasks_parts = {"id_part": [], "start": [], "end": []}

    i_current_section = 0
    no_more_sections = i_current_section == len(availabilities)

    i_current_part = 0
    no_more_parts = i_current_part == len(tasks)

    while not no_more_parts and not no_more_sections:
        current_section_is_filled = False
        current_section_start = availabilities.iloc[i_current_section][
            "timestamp_debut"
        ]
        current_section_end = availabilities.iloc[i_current_section]["timestamp_fin"]
        curseur_temps = current_section_start
        while not current_section_is_filled and not no_more_parts:
            id_part = ordonnancement.ordonnancement[i_current_part]
            part = tasks.iloc[id_part]
            length_part = datetime.timedelta(hours=part["length"])
            if curseur_temps + length_part > current_section_end:
                current_section_is_filled = True
                i_current_section += 1
            else:
                scheduled_tasks_parts["id_part"].append(id_part)
                scheduled_tasks_parts["start"].append(curseur_temps)
                scheduled_tasks_parts["end"].append(curseur_temps + length_part)
                i_current_part += 1
                no_more_parts = i_current_part == len(tasks)
                curseur_temps = curseur_temps + length_part

        no_more_sections = i_current_section == len(availabilities)

    scheduled_tasks_parts = pd.DataFrame(scheduled_tasks_parts)
    scheduled_tasks_parts = scheduled_tasks_parts.merge(tasks, on="id_part")
    scheduled_tasks_parts = scheduled_tasks_parts[
        ["start", "end", "evt_spkevenement", "evt_sfkprojet", "priorite","id_part"]
    ]
    return scheduled_tasks_parts


def schedule_events(
    availabilities: pd.DataFrame, tasks: pd.DataFrame, ordonnancement: Ordonnancement
):
    """
    Planifie les événements correspondant à l'ordonnancement quasi-optimal des tâches calculé lors de l'optimisation,
    à partir des disponibilités et des tâches.
    :param availabilities: dataframe des plages horaires de disponibilités
    :param tasks: dataframe des tâches contenant les parties de tâches
    :param ordonnancement: objet Ordonnancement contenant un ordonnancement quasi-optimal des parties de tâches.

    :return events: dataframe contenant les tâches/événements planifié(e)s.
    """
    scheduled_parts = schedule_parts(availabilities, tasks, ordonnancement)
    events = make_events(scheduled_parts)
    return scheduled_parts, events


def make_stats(events: pd.DataFrame, tasks: pd.DataFrame) -> dict[str: pd.DataFrame]:
    """
    Fourni un pourcentage de planification des tâches, à partir de ce qui a pu être planifié, et des
    tâches que l'on souhaitait initialiement planifier de manière optimale dans la période de sprint.

    :param events: dataframe des tâches planifiées
    :param tasks: dataframe des tâches à planifier de manière optimale
    """

    # stats percent completion for tasks
    events['duree'] = events['end'] - events['start']
    events['duree'] = events['duree'].apply(lambda x: x.total_seconds() / 3600)
    events = events.groupby('evt_spkevenement').sum("duree").reset_index()[['evt_spkevenement', 'duree']]
    tache_to_duree = dict(zip(events['evt_spkevenement'], events['duree']))
    stat_tasks = pd.DataFrame.copy(tasks)
    stat_tasks['duree_effectuee'] = stat_tasks['evt_spkevenement'].map(tache_to_duree)
    stat_tasks.fillna(0, inplace=True)
    stat_tasks['pct_completion'] = np.round(stat_tasks['duree_effectuee'] / stat_tasks['evt_dduree'], 2)
    stat_tasks = stat_tasks[['evt_spkevenement',
                             "lgl_sfkligneparent", "evt_sfkprojet", "priorite",'evt_dduree', "duree_effectuee",
                             "pct_completion"]]
    stat_tasks.sort_values(by="pct_completion", ascending=False)

    # stats percent completion for projects
    stat_projects = pd.DataFrame.copy(stat_tasks).groupby("evt_sfkprojet").sum()[["evt_dduree", "duree_effectuee"]]
    stat_projects['projet_percent_completion'] = np.round(stat_projects["duree_effectuee"] / stat_projects["evt_dduree"], 2)
    stat_projects = stat_projects.reset_index()

    stats = {"tasks": stat_tasks, "projects": stat_projects}
    return stats
