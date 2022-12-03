import pandas as pd
import numpy as np
from api.services.task_assigner.tools.id_remapping import flatten_list


def split_tasks(df: pd.DataFrame, mod_lenght: float = 1.0) -> pd.DataFrame:
    """
    Découpe des tâches en plusieurs tâches de durées plus courtes.
    
    :param df: dataframe des tâches à découper.
    :param mod_lenght: float (en heures) de la durée maximales des nouvelles tâches
    :return: dataframe des tâches découpées
    """
    df["n_parts"] = np.ceil(df["evt_dduree"] / mod_lenght).astype(int)
    df["n_filled_parts"] = (df["evt_dduree"] // mod_lenght).astype(int)
    df["length"] = df["evt_dduree"] - mod_lenght * df["n_filled_parts"]

    filled_rows = [[pd.DataFrame(row[1]).T] * int(row[1]['n_filled_parts'])  for row in df.iterrows()]
    filled_rows = pd.concat(flatten_list(filled_rows))
    filled_rows['length'] = mod_lenght

    unfilled_rows = df.loc[ (df['length'] > 0) & (df['length'] < mod_lenght)]
    out = pd.concat([filled_rows, unfilled_rows])
    out['evt_spkevenement'] = out['evt_spkevenement'].astype(int)
    out['lgl_sfkligneparent'] = out['lgl_sfkligneparent'].astype(int)
    out['evt_sfkprojet'] = out['evt_sfkprojet'].astype(int)
    out['priorite'] = out['priorite'].astype(int)
    out = out.drop(columns=['n_parts','n_filled_parts'])
    out.sort_values(by=['evt_spkevenement','length'], inplace=True)
    out.reset_index(drop=True, inplace=True)
    out['id_part'] = list(range(len(out)))
    return out
