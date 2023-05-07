"""
Fonctions pour préparer les données horaires brut de Wandeed à l'optimisation
"""
import pandas as pd
from api.string_keys import *


def handler_clean_hor(hor: pd.DataFrame) -> pd.DataFrame:
    """
    Ré-ordonne les colonnes et les lignes d'un dataframe d'horaires utilisateurs.
    - retire 1 à l'index des jours de la semaine pour que le lundi corresponde au jour 0 et pas 1.
    """
    hor.sort_values(
        by=[key_day_plage_horaire, key_debut_plage_horaire, key_fin_plage_horaire], inplace=True
    )
    hor = hor[[key_day_plage_horaire, key_debut_plage_horaire, key_fin_plage_horaire]]
    hor.reset_index(drop=True, inplace=True)

    hor = hor.loc[hor[key_debut_plage_horaire] <= hor[key_fin_plage_horaire]]
    hor.reset_index(drop=True, inplace=True)
    return hor


def handler_list_hor_utl(list_hor_utl: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatène un ensemble de dataframe d'horaires utilisateurs en un seul dataframe (appelé union dans la fonction suivante) et le nettoie.
    """
    list_hor_utl = [handler_clean_hor(hor) for hor in list_hor_utl]

    if len(list_hor_utl) == 1:
        union = list_hor_utl[0]
    else:
        union = list_hor_utl[0]
        for i in range(1, len(list_hor_utl)):
            union = pd.merge(union, list_hor_utl[i], how="outer")
        union = handler_clean_hor(union)
        union = handler_union_hor(union)
        union = handler_clean_hor(union)
    union[key_day_plage_horaire] = union[key_day_plage_horaire] - 1
    return union


def handler_union_hor(union: pd.DataFrame) -> pd.DataFrame:
    """
    Lorsque qu'un dataframe d'horaire est une union d'horaires possible, cette fonction fusionne tous les créneaux
    horaires pour qu'il n'y ait plus que l'essentiel avec des créneaux propres sans redondance.
    """
    out = pd.DataFrame({key: [] for key in list(union.columns)})
    temp = pd.DataFrame.copy(union)

    while len(temp) > 0:
        first_index = temp.index[0]

        current_row = temp.iloc[first_index]
        day = current_row[key_day_plage_horaire]
        heure_debut = current_row[key_debut_plage_horaire]
        heure_fin = current_row[key_fin_plage_horaire]

        to_delete = temp.loc[
            (temp[key_day_plage_horaire] == day)
            & (temp[key_debut_plage_horaire] >= heure_debut)
            & (temp[key_fin_plage_horaire] <= heure_fin)
        ]
        if len(to_delete) > 0:
            temp = temp.drop(index=to_delete.index)
            temp.reset_index(inplace=True, drop=True)

        kept = temp.loc[
            (temp[key_day_plage_horaire] == day) &
            ( ((temp[key_fin_plage_horaire] <= heure_fin) & (temp[key_debut_plage_horaire] <= heure_debut))
            | ((temp[key_fin_plage_horaire] >= heure_fin) & (temp[key_debut_plage_horaire] <= heure_fin))
            | ((temp[key_fin_plage_horaire] >= heure_fin) & (temp[key_debut_plage_horaire] <= heure_debut)))
        ]

        if len(kept) > 0:
            temp = temp.drop(index=kept.index)
            temp.reset_index(inplace=True, drop=True)
            final_hd = min(str(heure_debut), str(kept[key_debut_plage_horaire].min()))
            final_hf = max(str(heure_fin), str(kept[key_fin_plage_horaire].max()))
        else:
            final_hd = heure_debut
            final_hf = heure_fin

        final_row_df = pd.DataFrame(
            {
                key_day_plage_horaire: [day],
                key_debut_plage_horaire: [final_hd],
                key_fin_plage_horaire: [final_hf],
            }
        )

        out = pd.concat([out, final_row_df], ignore_index=True)

    out[key_day_plage_horaire] = out[key_day_plage_horaire].astype(int)
    out = handler_clean_hor(out)    
    return out


def make_clean_hor(df_hor: pd.DataFrame) -> dict:
    """
    Prend le dataframe d'horaires envoyé par Wandeed pour en faire un dictionnaire
    propre contenant pour chaque id utilisateur ses horaires sous forme de pd.DataFrame
    nettoyé et cohérent.
    """
    horaires = {}
    if len(df_hor) == 0:
        return horaires
    for utl in df_hor[key_epu_sfkutilisateur].unique():
        list_horaires_utl = list(
            df_hor.loc[
                df_hor[key_epu_sfkutilisateur] == utl,
            ][key_epl_employe_horaire]
        )
        list_df_hor_utl = [pd.DataFrame(_d) for _d in list_horaires_utl]
        horaires[utl] = handler_list_hor_utl(list_df_hor_utl)
    return horaires
