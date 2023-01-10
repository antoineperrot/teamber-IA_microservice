"""
Fonctions pour préparer les données impératifs brut de Wandeed à l'optimisation
"""
import pandas as pd
from api.string_keys import *


def split_n_clean_impertifs(df_imp: pd.DataFrame) -> dict:
    """
    Sépare le fichier d'entrée des impératifs en un dictionnaire {id_utilsateur:impératif_utilisateur}
    """

    dict_imp = {}

    # TODO: corriger la clé quand j'aurai la bonne
    for utl in df_imp[key_competence].unique():
        df_imp_utl = df_imp.loc[df_imp[key_competence] == utl]
        dict_imp[utl] = df_imp_utl

    return dict_imp
