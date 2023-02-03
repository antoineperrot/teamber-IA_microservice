"""
Contient toutes les fonctions qui consistent à remapper les entrees/sorties des
ID locaux/externes.
"""
import numpy as np
import pandas as pd

from api.string_keys import *


def remap_df_out(df_out: pd.DataFrame,
                 mapping_int_to_tsk: dict,
                 mapping_int_to_utl: dict,
                 mapping_int_to_prj: dict,
                 mapping_int_to_cmp: dict) -> pd.DataFrame:
    """
    REMAPPING DES ID LOCAUX EN ID WANDEED
    """
    remapped_df_out = pd.DataFrame.copy(df_out)
    remapped_df_out["tsk"] = df_out["tsk"].map(mapping_int_to_tsk)
    remapped_df_out["utl"] = df_out["utl"].map(mapping_int_to_utl)
    remapped_df_out["prj"] = df_out["prj"].map(mapping_int_to_prj)
    remapped_df_out["cmp"] = df_out["cmp"].map(mapping_int_to_cmp)
    remapped_df_out["duree_assignee"] = np.round(df_out["duree_assignee"], 2)
    return remapped_df_out


def make_usefull_mapping_dicts(
    df_tsk: pd.DataFrame, df_dsp: pd.DataFrame
) -> tuple[dict, dict, dict, dict]:
    """
    FABRICATION DE DICTIONNAIRE UTILES PAR LA SUITE
    """
    d_tsk_to_cmp = {int(row["tsk"]): int(row["cmp"]) for i, row in df_tsk.iterrows()}
    d_tsk_to_prj = {int(row["tsk"]): int(row["prj"]) for i, row in df_tsk.iterrows()}
    d_tsk_to_lgt = {int(row["tsk"]): row[key_duree_evenement] for i, row in df_tsk.iterrows()}
    d_utl_to_dsp = {int(row["utl"]): row[key_user_dispo] for _, row in df_dsp.iterrows()}
    d_utl_to_dsp["not assigned"] = np.sum(list(d_utl_to_dsp.values()))
    return d_tsk_to_cmp, d_tsk_to_prj, d_tsk_to_lgt, d_utl_to_dsp


def make_mapping_dicts_extern_to_local(id_utl, id_prj, id_cmp, id_tsk):
    """
    CONVERSION DES IDS Wandeed en Identifiant local
    """
    mapping_utl_to_int = {int(_id): int(_int) for _int, _id in enumerate(id_utl)}
    mapping_prj_to_int = {int(_id): int(_int) for _int, _id in enumerate(id_prj)}
    mapping_cmp_to_int = {int(_id): int(_int) for _int, _id in enumerate(id_cmp)}
    mapping_tsk_to_int = {int(_id): int(_int) for _int, _id in enumerate(id_tsk)}
    return mapping_utl_to_int, mapping_prj_to_int, mapping_cmp_to_int, mapping_tsk_to_int


def make_mapping_dicts_local_to_extern(id_utl, id_prj, id_cmp, id_tsk):
    """
    CONVERSION DES Identifiant local en IDS Wandeed
    """
    mapping_int_to_utl = {int(_int): int(_id) for _int, _id in enumerate(id_utl)}
    mapping_int_to_utl["not assigned"] = "not assigned"
    mapping_int_to_prj = {int(_int): int(_id) for _int, _id in enumerate(id_prj)}
    mapping_int_to_cmp = {int(_int): int(_id) for _int, _id in enumerate(id_cmp)}
    mapping_int_to_tsk = {int(_int): int(_id) for _int, _id in enumerate(id_tsk)}
    return mapping_int_to_utl, mapping_int_to_prj, mapping_int_to_cmp, mapping_int_to_tsk


def make_list_ids(df_prj, df_cmp, df_tsk, df_dsp):
    """
    FAIT LA LISTE DE TOUS LES IDS (PRJ, CMP, TSK, UTL) CONTENUS DANS LES DONNEES RECUES
    """
    # sauvegarde des id utilisateurs ET conservation des ids_utl uniques
    lst_utl = list()
    lst_utl.append(list(np.unique(df_prj[key_user])))
    lst_utl.append(list(np.unique(df_cmp[key_emc_sfkutilisateur])))
    lst_utl.append(list(np.unique(df_dsp[key_user])))
    id_utl = list(np.sort(np.unique(flatten_list(lst_utl))))

    # sauvegarde des id projets ET conservation des ids_prj uniques
    lst_prj = list()
    lst_prj.append(list(np.unique(df_prj[key_project])))
    lst_prj.append(list(np.unique(df_tsk[key_evenement_project])))
    id_prj = list(np.sort(np.unique(flatten_list(lst_prj))))

    # sauvegardes des ids competences ET conservation des ids_cmp uniques
    lst_cmp = list()
    lst_cmp.append(list(np.unique(df_cmp[key_emc_sfkarticle])))
    lst_cmp.append(list(np.unique(df_tsk[key_competence])))
    id_cmp = list(np.sort(np.unique(flatten_list(lst_cmp))))

    # sauvegardes des ids tsk ET conservation des ids_tsk uniques
    id_tsk = list(np.sort(np.unique(df_tsk[key_evenement])))

    return id_utl, id_prj, id_cmp, id_tsk


def flatten_list(list_of_list: list[list]) -> list:
    """Met à place une liste de liste"""
    out = list()
    for sublist in list_of_list:
        for item in sublist:
            out.append(item)
    return out


def add_local_ids_in_dfs(
    df_prj: pd.DataFrame,
    df_cmp: pd.DataFrame,
    df_tsk: pd.DataFrame,
    df_dsp: pd.DataFrame,
    mapping_cmp_to_int: dict,
    mapping_utl_to_int: dict,
    mapping_tsk_to_int: dict,
    mapping_prj_to_int: dict,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    AJOUT DES VARIABLES LOCALES DANS LES DATAFRAMES
    """
    df_cmp["cmp"] = df_cmp[key_emc_sfkarticle].map(mapping_cmp_to_int)
    df_cmp["utl"] = df_cmp[key_emc_sfkutilisateur].map(mapping_utl_to_int)
    df_tsk["tsk"] = df_tsk[key_evenement].map(mapping_tsk_to_int)
    df_tsk["cmp"] = df_tsk[key_competence].map(mapping_cmp_to_int)
    df_tsk["prj"] = df_tsk[key_evenement_project].map(mapping_prj_to_int)
    df_prj["utl"] = df_prj[key_user].map(mapping_utl_to_int)
    df_prj["prj"] = df_prj[key_project].map(mapping_prj_to_int)
    df_dsp["utl"] = df_dsp[key_user].map(mapping_utl_to_int)

    # commodités pour plus tard
    df_cmp = df_cmp.sort_values(by="utl")
    return df_prj, df_cmp, df_tsk, df_dsp
