import pandas as pd
from fastapi import HTTPException


def controller_data(
    df_prj: pd.DataFrame,
    df_cmp: pd.DataFrame,
    df_tsk: pd.DataFrame,
    df_dsp: pd.DataFrame,
):
    """
    Vérifie que les données reçues sont cohérentes.
    """
    if len(df_cmp) == 0:
        raise HTTPException(
            status_code=422, detail="Pas de matrice de compétence disponible."
        )
    if len(df_tsk) == 0:
        raise HTTPException(status_code=422, detail="Pas de tâches à assigner.")
