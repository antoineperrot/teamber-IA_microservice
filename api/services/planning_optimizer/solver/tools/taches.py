import numpy as np
import pandas as pd

from api.services.task_assigner.tools.id_remapping import flatten_list


def split_tasks(tasks: pd.DataFrame, parts_max_length: float = 1.0) -> pd.DataFrame:
    """
    Découpe des tâches en plusieurs tâches de durées plus courtes.

    :param tasks: dataframe des tâches à découper.
    :param parts_max_length: float (en heures) de la durée maximales des nouvelles tâches
    :return tasks_parts: dataframe des tâches découpées en sous-parties
    """
    tasks["n_parts"] = np.ceil(tasks["evt_dduree"] / parts_max_length).astype(int)
    tasks["n_filled_parts"] = (tasks["evt_dduree"] // parts_max_length).astype(int)
    tasks["length"] = tasks["evt_dduree"] - parts_max_length * tasks["n_filled_parts"]

    filled_rows = [[pd.DataFrame(row[1]).T] * int(row[1]['n_filled_parts'])  for row in tasks.iterrows()]
    filled_rows = pd.concat(flatten_list(filled_rows))
    filled_rows['length'] = parts_max_length

    unfilled_rows = tasks.loc[ (tasks['length'] > 0) & (tasks['length'] < parts_max_length)]
    tasks_parts = pd.concat([filled_rows, unfilled_rows])
    tasks_parts['evt_spkevenement'] = tasks_parts['evt_spkevenement'].astype(int)
    tasks_parts['lgl_sfkligneparent'] = tasks_parts['lgl_sfkligneparent'].astype(int)
    tasks_parts['evt_sfkprojet'] = tasks_parts['evt_sfkprojet'].astype(int)
    tasks_parts['priorite'] = tasks_parts['priorite'].astype(int)
    tasks_parts = tasks_parts.drop(columns=['n_parts','n_filled_parts'])
    tasks_parts.sort_values(by=['evt_spkevenement','length'], inplace=True)
    tasks_parts.reset_index(drop=True, inplace=True)
    tasks_parts['id_part'] = list(range(len(tasks_parts)))
    return tasks_parts
