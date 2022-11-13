"""
Contient les fonctions de split des données pour task_assigner
une fois les données reçues et get_data_task_assigner.
"""
import pandas as pd
from typing import Tuple


def split_data_task_assigner(
    data: dict,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split les datas reçues à la sortie de get_data_task_assigner en 4 pd.DataFrame:

    TODO: à compléter

    :return df_prj:

    :return df_cmp:

    :return df_tsk:

    :return df_dsp:

    """
    # recuperation matrice_projet
    df_prj = pd.DataFrame(data["matrice_projet"])
    # recuperation matrice_competence : on oublie les compétences pour lesquels les utl sont indéfinis
    df_cmp = (
        pd.DataFrame(data["matrice_competence"])
        .dropna()
        .reset_index(drop=True)
        .astype(int)
    )
    # recuperation des taches à assigner :
    df_tsk = pd.DataFrame(data["taches"])
    # recuperation des disponibilites utl :
    df_dsp = pd.DataFrame(data["dispos_utilisateurs"])

    return df_prj, df_cmp, df_tsk, df_dsp
