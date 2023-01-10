import numpy as np
import pandas as pd

from api.services.task_assigner.tools.id_remapping import flatten_list
from api.string_keys import *


def split_tasks(tasks: pd.DataFrame, parts_max_length: float = 1.0) -> pd.DataFrame:
    """
    Découpe des tâches en plusieurs tâches de durées plus courtes.

    :param tasks: dataframe des tâches à découper.
    :param parts_max_length: float (en heures) de la durée maximales des nouvelles tâches
    :return tasks_parts: dataframe des tâches découpées en sous-parties
    """
    tasks["n_parts"] = np.ceil(tasks[key_duree_evenement] / parts_max_length).astype(int)
    tasks["n_filled_parts"] = (tasks[key_duree_evenement] // parts_max_length).astype(int)
    tasks["length"] = tasks[key_duree_evenement] - parts_max_length * tasks["n_filled_parts"]

    filled_rows = [
        [pd.DataFrame(row[1]).T] * int(row[1]["n_filled_parts"])
        for row in tasks.iterrows()
    ]
    filled_rows = pd.concat(flatten_list(filled_rows))
    filled_rows["length"] = parts_max_length

    unfilled_rows = tasks.loc[
        (tasks["length"] > 0) & (tasks["length"] < parts_max_length)
    ]
    tasks_parts = pd.concat([filled_rows, unfilled_rows])
    tasks_parts[key_evenement] = tasks_parts[key_evenement].astype(int)
    tasks_parts[key_competence] = tasks_parts[key_competence].astype(int)
    tasks_parts[key_evenement_project] = tasks_parts[key_evenement_project].astype(int)
    tasks_parts[key_project_priority] = tasks_parts[key_project_priority].astype(int)
    tasks_parts = tasks_parts.drop(columns=["n_parts", "n_filled_parts"])
    tasks_parts.sort_values(by=[key_evenement, "length"], inplace=True)
    tasks_parts.reset_index(drop=True, inplace=True)
    tasks_parts["id_part"] = list(range(len(tasks_parts)))
    return tasks_parts
