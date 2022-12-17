"""
Contient toutes les fonctions qui consistent à remapper les entrees/sorties des
ID locaux/externes.
"""
from typing import Tuple, List

import numpy as np
import pandas as pd


def remap_df_out(df_out: pd.DataFrame, int_to_tsk, int_to_utl, int_to_prj, int_to_cmp):
    """
    REMAPPING DES ID LOCAUX EN ID WANDEED
    """
    remapped_df_out = pd.DataFrame.copy(df_out)
    remapped_df_out["tsk"] = df_out["tsk"].map(int_to_tsk)
    remapped_df_out["utl"] = df_out["utl"].map(int_to_utl)
    remapped_df_out["prj"] = df_out["prj"].map(int_to_prj)
    remapped_df_out["cmp"] = df_out["cmp"].map(int_to_cmp)
    remapped_df_out["duree_assignee"] = np.round(df_out["duree_assignee"], 2)
    return remapped_df_out


def make_usefull_mapping_dicts(
    df_tsk: pd.DataFrame, df_dsp: pd.DataFrame
) -> Tuple[dict, dict, dict, dict]:
    """
    FABRICATION DE DICTIONNAIRE UTILES PAR LA SUITE
    """
    d_tsk_to_cmp = {int(row["tsk"]): int(row["cmp"]) for i, row in df_tsk.iterrows()}
    d_tsk_to_prj = {int(row["tsk"]): int(row["prj"]) for i, row in df_tsk.iterrows()}
    d_tsk_to_lgt = {int(row["tsk"]): row["evt_dduree"] for i, row in df_tsk.iterrows()}
    d_utl_to_dsp = {int(row["utl"]): row["utl_sdispo"] for _, row in df_dsp.iterrows()}
    d_utl_to_dsp["not assigned"] = np.sum(list(d_utl_to_dsp.values()))
    return d_tsk_to_cmp, d_tsk_to_prj, d_tsk_to_lgt, d_utl_to_dsp


def make_mapping_dicts_extern_to_local(id_utl, id_prj, id_cmp, id_tsk):
    """
    CONVERSION DES IDS Wandeed en Identifiant local
    """
    utl_to_int = {int(_id): int(_int) for _int, _id in enumerate(id_utl)}
    prj_to_int = {int(_id): int(_int) for _int, _id in enumerate(id_prj)}
    cmp_to_int = {int(_id): int(_int) for _int, _id in enumerate(id_cmp)}
    tsk_to_int = {int(_id): int(_int) for _int, _id in enumerate(id_tsk)}
    return utl_to_int, prj_to_int, cmp_to_int, tsk_to_int


def make_mapping_dicts_local_to_extern(id_utl, id_prj, id_cmp, id_tsk):
    """
    CONVERSION DES Identifiant local en IDS Wandeed
    """
    int_to_utl = {int(_int): int(_id) for _int, _id in enumerate(id_utl)}
    int_to_utl["not assigned"] = "not assigned"
    int_to_prj = {int(_int): int(_id) for _int, _id in enumerate(id_prj)}
    int_to_cmp = {int(_int): int(_id) for _int, _id in enumerate(id_cmp)}
    int_to_tsk = {int(_int): int(_id) for _int, _id in enumerate(id_tsk)}
    return int_to_utl, int_to_prj, int_to_cmp, int_to_tsk


def make_list_ids(df_prj, df_cmp, df_tsk, df_dsp):
    """
    FAIT LA LISTE DE TOUS LES IDS (PRJ, CMP, TSK, UTL) CONTENUS DANS LES DONNEES RECUES
    """
    # sauvegarde des id utilisateurs ET conservation des ids_utl uniques
    lst_utl = []
    lst_utl.append(list(np.unique(df_prj["utl_spkutilisateur"])))
    lst_utl.append(list(np.unique(df_cmp["emc_sfkutilisateur"])))
    lst_utl.append(list(np.unique(df_dsp["utl_spkutilisateur"])))
    id_utl = list(np.sort(np.unique(flatten_list(lst_utl))))

    # sauvegarde des id projets ET conservation des ids_prj uniques
    lst_prj = []
    lst_prj.append(list(np.unique(df_prj["int_sfkprojet"])))
    lst_prj.append(list(np.unique(df_tsk["evt_sfkprojet"])))
    id_prj = list(np.sort(np.unique(flatten_list(lst_prj))))

    # sauvegardes des ids competences ET conservation des ids_cmp uniques
    lst_cmp = []
    lst_cmp.append(list(np.unique(df_cmp["emc_sfkarticle"])))
    lst_cmp.append(list(np.unique(df_tsk["lgl_sfkligneparent"])))
    id_cmp = list(np.sort(np.unique(flatten_list(lst_cmp))))

    # sauvegardes des ids tsk ET conservation des ids_tsk uniques
    lst_tsk = []
    id_tsk = list(np.sort(np.unique(df_tsk["evt_spkevenement"])))

    return id_utl, id_prj, id_cmp, id_tsk


def flatten_list(list_of_list: List[list]) -> list:
    out = []
    for sublist in list_of_list:
        for item in sublist:
            out.append(item)
    return out


def add_local_ids_in_dfs(
    df_prj: pd.DataFrame,
    df_cmp: pd.DataFrame,
    df_tsk: pd.DataFrame,
    df_dsp: pd.DataFrame,
    cmp_to_int: dict,
    utl_to_int: dict,
    tsk_to_int: dict,
    prj_to_int: dict,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    AJOUT DES VARIABLES LOCALES DANS LES DATAFRAMES
    """
    df_cmp["cmp"] = df_cmp["emc_sfkarticle"].map(cmp_to_int)
    df_cmp["utl"] = df_cmp["emc_sfkutilisateur"].map(utl_to_int)
    df_tsk["tsk"] = df_tsk["evt_spkevenement"].map(tsk_to_int)
    df_tsk["cmp"] = df_tsk["lgl_sfkligneparent"].map(cmp_to_int)
    df_tsk["prj"] = df_tsk["evt_sfkprojet"].map(prj_to_int)
    df_prj["utl"] = df_prj["utl_spkutilisateur"].map(utl_to_int)
    df_prj["prj"] = df_prj["int_sfkprojet"].map(prj_to_int)
    df_dsp["utl"] = df_dsp["utl_spkutilisateur"].map(utl_to_int)

    # commodités pour plus tard
    df_cmp = df_cmp.sort_values(by="utl")
    return df_prj, df_cmp, df_tsk, df_dsp
