"""
Fonctions pour préparer les données brutes de Wandeed à l'optimisation
"""

from typing import List, Tuple
import pandas as pd


def handler_clean_hor(hor: pd.DataFrame) -> pd.DataFrame:
    """
    Ré-ordonne les colonnes et les lignes d'un dataframe d'horaires utilisateurs.
    """
    hor.sort_values(
        by=["eeh_sfkperiode", "eeh_xheuredebut", "eeh_xheurefin"], inplace=True
    )
    hor = hor[["eeh_sfkperiode", "eeh_xheuredebut", "eeh_xheurefin"]]
    hor.reset_index(drop=True, inplace=True)

    hor = hor.loc[hor["eeh_xheuredebut"] <= hor["eeh_xheurefin"]]
    hor.reset_index(drop=True, inplace=True)
    return hor


def handler_list_hor_utl(list_hor_utl: List[pd.DataFrame]) -> pd.DataFrame:
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
        day = current_row["eeh_sfkperiode"]
        heure_debut = current_row["eeh_xheuredebut"]
        heure_fin = current_row["eeh_xheurefin"]

        to_delete = temp.loc[
            (temp["eeh_sfkperiode"] == day)
            & (temp["eeh_xheuredebut"] >= heure_debut)
            & (temp["eeh_xheurefin"] <= heure_fin)
        ]
        if len(to_delete) > 0:
            temp = temp.drop(index=to_delete.index)
            temp.reset_index(inplace=True, drop=True)

        kept = temp.loc[
            (temp["eeh_sfkperiode"] == day)
            & (temp["eeh_xheuredebut"] <= heure_fin)
            & (temp["eeh_xheuredebut"] >= heure_debut)
            & (temp["eeh_xheurefin"] >= heure_fin)
        ]

        if len(kept) > 0:
            temp = temp.drop(index=kept.index)
            temp.reset_index(inplace=True, drop=True)
            final_hd = min(str(heure_debut), str(kept["eeh_xheuredebut"].min()))
            final_hf = max(str(heure_fin), str(kept["eeh_xheurefin"].max()))
        else:
            final_hd = heure_debut
            final_hf = heure_fin

        final_row_df = pd.DataFrame(
            {
                "eeh_sfkperiode": [day],
                "eeh_xheuredebut": [final_hd],
                "eeh_xheurefin": [final_hf],
            }
        )

        out = pd.concat([out, final_row_df], ignore_index=True)
    #         out = out.append(final_row, ignore_index=True)

    out["eeh_sfkperiode"] = out["eeh_sfkperiode"].astype(int)

    return out


def make_horaire_clean(df_hor: pd.DataFrame) -> dict:
    """
    Prend le dataframe d'horaires envoyé par Wandeed pour en faire un dictionnaire
    propre contenant pour chaque id utilisateur ses horaires sous forme de pd.DataFrame
    nettoyé et cohérent.
    """
    out = {}
    for utl in df_hor["epu_sfkutilisateur"].unique():
        list_dict_hor_utl = list(
            df_hor.loc[
                df_hor["epu_sfkutilisateur"] == utl,
            ]["epl_employe_horaire"]
        )
        list_df_hor_utl = [pd.DataFrame(_d) for _d in list_dict_hor_utl]
        out[utl] = handler_list_hor_utl(list_df_hor_utl)
    return out


def split_data_planning_optimizer(
    data: dict,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split les datas reçues à la sortie de get_data_planning_optimizer en 3 pd.DataFrame:
    :return df_imp:
        TODO: à compléter

    :return df_hor: dataframe contenant les horaires des utilisateurs
        "epu_sfkutilisateur"  -> id de l'utilisateur
        "epl_xdebutperiode"   -> debut de période d'application de l'horaire
        "epl_xfinperiode"     -> fin de période d'application de l'horaire
        "epl_employe_horaire" -> horaire de l'employe

    :return df_tsk:
        "evt_dduree"          -> duree (en h) de la tâche
        "evt_spkevenement"    -> id de la tâche
        "lgl_sfkligneparent"  -> utilisateur concerné
        "evt_sfkprojet"       -> projet de rattachement de la tâche

    """
    df_imp = pd.DataFrame(data["imperatifs"])
    df_hor = pd.DataFrame(data["horaires"]).reindex(
        columns=[
            "epu_sfkutilisateur",
            "epl_xdebutperiode",
            "epl_xfinperiode",
            "epl_employe_horaire",
        ]
    )
    df_hor.epl_xdebutperiode = pd.to_datetime(df_hor.epl_xdebutperiode).dt.date
    df_hor.epl_xfinperiode = pd.to_datetime(df_hor.epl_xfinperiode).dt.date
    df_hor = df_hor.sort_values(
        by=["epu_sfkutilisateur", "epl_xdebutperiode"]
    ).reset_index(drop=True)
    df_tsk = pd.DataFrame(data["taches"])
    return df_imp, df_hor, df_tsk


def split_tsk_utl(dict_hor: dict, df_tsk: pd.DataFrame) -> Tuple[dict, List[int]]:
    """
    :param dict_hor: dictionnaire des horaires sortant de la fonction make_clean_hor
    :param df_tsk: pd.DataFrame des taches sur la période concernée

    :return task_to_optimize_dict: un dictionnaire {id_utl:taches_de_utl} à optimiser ensuite pour chaque utl
    :return utl_without_horaire: la liste des id_utl contenus dans df_tsk, pour qui on souhaiterait donc
    potentiellement optimiser les emplois du temps, mais pour qui on ne dispose pas des horaires de travail.
    """
    task_to_optimize_dict = {}  # {id_utilisateur: df_tache}

    utl_without_horaire = []
    for utl in df_tsk["lgl_sfkligneparent"].unique():
        if not utl in dict_hor.keys():
            # pas d'horaires dispo pour cet utilisateur -> impossible de lancer le programme
            utl_without_horaire.append(utl)
        else:
            df_tsk_utl = df_tsk.loc[
                df_tsk["lgl_sfkligneparent"] == utl,
            ]
            task_to_optimize_dict[utl] = df_tsk_utl

    return task_to_optimize_dict, utl_without_horaire
