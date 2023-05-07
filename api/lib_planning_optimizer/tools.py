"""Module des tools du solveur de planning optimizer"""
import numpy as np
import plotly.express as px
import pandas as pd

from api.loggers import logger_planning_optimizer
from api.lib_task_assigner.tools.id_remapping import flatten_list
from api.string_keys import *
from api.tools import timed_function

KEY_AVAILABILITIES = "AVAILABILITIES"
KEY_WORK = "WORK"


def energy_waisted_time(ordo_length: list[float], sections_lengths: list[float]):
    """
    Calcule le temps perdu pour un ordonnancement donné.

    :param ordo_length: liste des durées successives des tâches
    :param sections_lengths: liste des durées successives des sections temporelle de travail.

    :return ratio_waisted_time: float, proportion du temps total travaillé sur le temps total disponible.
    """
    n_tasks, n_sections = len(ordo_length), len(sections_lengths)

    wasted_time = 0
    total_available_time = 0
    i_section, i_length = 0, 0
    while i_length < n_tasks and i_section < n_sections:
        current_section_used_time = 0
        j = i_length
        current_section_is_filled = False
        total_available_time += sections_lengths[i_section]
        while j < n_tasks and not current_section_is_filled:
            if (
                ordo_length[j] + current_section_used_time
                <= sections_lengths[i_section]
            ):
                current_section_used_time += ordo_length[j]
                j += 1
            else:
                current_section_is_filled = True

        i_length = j

        total_available_time += sections_lengths[i_section]
        wasted_time += max(sections_lengths[i_section] - current_section_used_time, 0)
        i_section += 1

    ratio_wasted_time = wasted_time / total_available_time

    return ratio_wasted_time


def energy_key_project_prioritys(ordo_prio):
    """Calcule l'énergie de le l'ordonnancement des niveaux de priorités."""
    target = np.sort(ordo_prio)
    energy = (
        np.linalg.norm(target - ordo_prio, ord=1)
        / len(np.unique(ordo_prio))
        / len(ordo_prio)
    )
    return energy


def energy_dispersion(ordo_evt):
    """
    Calcule une énergie de dispersion, quantifiant si une tâche est réalisée d'un bloc (energie = 0),
    ou à plusieurs occasions (energie > 0).
    """
    list_evt = np.unique(ordo_evt)
    pen = 0
    c = 0
    for t in list_evt:
        indexs = np.where(ordo_evt == t)[0]
        if len(indexs) > 1:
            c += 1
            pen_local = 0
            for i in range(len(indexs) - 1):
                if indexs[i + 1] > indexs[i] + 1:
                    pen_local += 1
            pen_local /= len(indexs)
            pen += pen_local
    out = pen / c if c > 0 else 0
    return out


@timed_function(logger_planning_optimizer)
def split_tasks(tasks: pd.DataFrame, parts_max_length: float = 1.0) -> pd.DataFrame:
    """
    Découpe des tâches en plusieurs tâches de durées plus courtes.

    :param tasks: dataframe des tâches à découper.
    :param parts_max_length: float (en heures) de la durée maximales des nouvelles tâches
    :return tasks_parts: dataframe des tâches découpées en sous-parties
    """
    tasks[KEY_NUMBER_PARTS] = np.ceil(tasks[key_duree_evenement] / parts_max_length).astype(int)
    tasks[KEY_NUMBER_FILLED_PARTS] = (tasks[key_duree_evenement] // parts_max_length).astype(int)
    tasks[KEY_DUREE_PART] = tasks[key_duree_evenement] - parts_max_length * tasks[KEY_NUMBER_FILLED_PARTS]

    filled_rows = [
        [pd.DataFrame(row[1]).T] * int(row[1][KEY_NUMBER_FILLED_PARTS])
        for row in tasks.iterrows()
    ]
    flatten_list_filled_rows = flatten_list(filled_rows)
    if len(flatten_list_filled_rows) > 0:
        filled_rows = pd.concat(flatten_list(filled_rows))
        filled_rows[KEY_DUREE_PART] = parts_max_length
    else:
        filled_rows = pd.DataFrame()
    unfilled_rows = tasks.loc[
        (tasks[KEY_DUREE_PART] > 0) & (tasks[KEY_DUREE_PART] < parts_max_length)
    ]
    tasks_parts = pd.concat([filled_rows, unfilled_rows])
    tasks_parts[key_evenement] = tasks_parts[key_evenement].astype(int)
    tasks_parts[key_evenement_project] = tasks_parts[key_evenement_project].astype(int)
    tasks_parts[KEY_PROJECT_PRIORITY] = tasks_parts[KEY_PROJECT_PRIORITY].astype(int)
    tasks_parts = tasks_parts.drop(columns=[KEY_NUMBER_PARTS, KEY_NUMBER_FILLED_PARTS])
    tasks_parts.sort_values(by=[key_evenement, KEY_DUREE_PART], inplace=True)
    tasks_parts.reset_index(drop=True, inplace=True)
    tasks_parts[KEY_ID_PART] = list(range(len(tasks_parts)))
    return tasks_parts


@timed_function(logger=logger_planning_optimizer)
def make_timeline(availabilities: pd.DataFrame,
                  events: pd.DataFrame,
                  imperatifs: pd.DataFrame,
                  utilisateur_id: int):
    """
    Dessine la timeline des événements planifiées, des disponibilités de travail et des impératifs.
    """

    if imperatifs is None:
        task_imperatifs = []
        start_imperatifs = []
        end_imperatifs = []
    else:
        task_imperatifs = ["Imperatifs"] * len(imperatifs)
        start_imperatifs = imperatifs[key_evenement_date_debut].to_list()
        end_imperatifs = imperatifs[key_evenement_date_fin].to_list()

    # create some sample data
    data = {
        'Task': task_imperatifs + ['Availabilities'] * len(availabilities) + ["Optimized tasks"] * len(
            events),
        'Start': start_imperatifs + availabilities[KEY_TIMESTAMP_DEBUT].to_list() + events[KEY_START].to_list(),
        'Finish': end_imperatifs + availabilities[KEY_TIMESTAMP_FIN].to_list() + events[
            KEY_END].to_list()
    }
    df = pd.DataFrame(data)

    # create the timeline using plotly express
    fig = px.timeline(df, x_start='Start', x_end='Finish', y='Task', color='Task')
    fig.update_traces(marker_color='green', selector=dict(name='Imperatifs'))

    # update the layout
    fig.update_layout(
        title=f'Timeline sprint utilisateur {utilisateur_id}',
        xaxis_title='Date',
        yaxis_title='Task',
        height=300
    )

    # show the figure
    fig.show()
