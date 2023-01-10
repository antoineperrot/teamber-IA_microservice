import numpy as np
import pandas as pd
from api.string_keys import *


def make_mat_prj(df_prj: pd.DataFrame, n_prj: int, n_utl: int) -> np.ndarray:
    """
    FABRICATION MATRICE PROJET
    """
    # construction d'un dictionnaire qui contient, pour chaque prjet, la liste des utilisateurs en faisant parti.
    d_prj_to_utl = df_prj.groupby("prj")["utl"].apply(np.sort).to_dict()

    # REMPLISSAGE MATRICE PROJET :
    mat_prj = np.zeros((n_prj, n_utl)).astype(int)
    for prj in range(n_prj):
        for utl in d_prj_to_utl[prj]:
            mat_prj[prj, utl] = 1

    return mat_prj


def make_mat_cmp(df_cmp: pd.DataFrame, n_cmp: int, n_utl: int) -> np.ndarray:
    """
    FABRICATION MATRICE COMPETENCE
    """

    # construction matrice de cmp np.array
    mat_cmp = np.zeros((n_cmp, n_utl)).astype(int)

    # REMPLISSAGE MATRICE DE COMPETENCE

    # ce dict est organisé en arborescence : utl//comp//niveau
    d_utl_to_cmp_to_lvl = {}
    utl_competants = list(np.unique(df_cmp["utl"]))
    for utl in utl_competants:
        d_utl_to_cmp_to_lvl[utl] = {}
        df_cmp_tmp = df_cmp.loc[
            df_cmp["utl"] == utl,
        ]
        for i, row in df_cmp_tmp.iterrows():
            cmp = row["cmp"]
            lvl = row[key_emc_sniveau]
            d_utl_to_cmp_to_lvl[utl][cmp] = lvl

    for utl in d_utl_to_cmp_to_lvl:
        for cmp in d_utl_to_cmp_to_lvl[utl].keys():
            lvl = d_utl_to_cmp_to_lvl[utl][cmp]
            mat_cmp[cmp, utl] = lvl

    return mat_cmp


def make_mat_spe(mat_cmp: np.ndarray) -> np.ndarray:
    """
    la matrice de spécialisation permet de mettre en avant le fait que certaines personnes ne
    savent réaliser qu'un nombre limité de tâches, a un niveau de compétence peut-être inférieur à d'autmat_spe personnes plus expertes, mais étant donné
    qu'elle ne savent faire que ces tâches, il vaut mieux leur assigner à eux et laisser le champ libre à des personnes plus expertes, souvent plus transverses (chef d'équipe etc).
    """
    mat_spe = mat_cmp.astype(float)
    mat_spe[:, mat_cmp.sum(axis=0) == 0] = np.nan
    mat_spe = mat_spe / mat_spe.sum(axis=0) * 3
    mat_spe[mat_spe == np.nan] = 0
    mat_spe[:, mat_cmp.max(axis=0) == 0] = 0
    return mat_spe
