import numpy as np
import pandas as pd


def make_stat_cmp(df_out: pd.DataFrame) -> pd.DataFrame:
    """
    Production de statistiques par compétences
    """
    avg_lvl = np.round(
        df_out.loc[df_out["utl"] != "not assigned"]
        .groupby("cmp")["lvl"]
        .mean()
        .rename("niveau_cmp_moyen_par_h_realisee"),
        2,
    )
    cmp_miss = (
        df_out.loc[df_out["utl"] == "not assigned"]
        .groupby("cmp")["duree_assignee"]
        .sum()
        .rename("total_h_non_assignees")
    )
    stat_cmp = pd.DataFrame([avg_lvl, cmp_miss]).T
    stat_cmp["total_h_non_assignees"] = stat_cmp["total_h_non_assignees"].fillna(0)
    stat_cmp.sort_values("total_h_non_assignees", ascending=False, inplace=True)
    stat_cmp.reset_index(inplace=True)

    assert(all(stat_cmp["total_h_non_assignees"].values >= 0))
    assert all(np.logical_or(stat_cmp["niveau_cmp_moyen_par_h_realisee"].isna().values, stat_cmp["niveau_cmp_moyen_par_h_realisee"].values >= 0))
    assert all(np.logical_or(stat_cmp["niveau_cmp_moyen_par_h_realisee"].isna().values, stat_cmp["niveau_cmp_moyen_par_h_realisee"].values <= 3))

    return stat_cmp


def make_stat_utl(
    df_out: pd.DataFrame, mapping_utl_to_dsp: dict, mapping_utl_to_int: dict
) -> pd.DataFrame:
    """
    Production de statistiques par utilisateur
    """
    avg_lvl = df_out[["utl", "duree_assignee", "lvl"]].loc[
        df_out["utl"] != "not assigned"
    ]
    avg_lvl["niveau_moyen_execution_tsk"] = avg_lvl["duree_assignee"] * avg_lvl["lvl"]
    avg_lvl_exe_tsk = np.round(
        avg_lvl.groupby("utl")["niveau_moyen_execution_tsk"].sum()
        / avg_lvl.groupby("utl")["duree_assignee"].sum(),
        1,
    )
    avg_lvl_exe_tsk.rename("niveau_moyen_execution_tsk", inplace=True)
    tot_h = (
        df_out.loc[df_out["utl"] != "not assigned"]
        .groupby("utl")["duree_assignee"]
        .sum()
        .rename("total_h_assignees")
    )
    stat_utl = pd.DataFrame([avg_lvl_exe_tsk, tot_h]).T
    stat_utl["utl_int"] = stat_utl.index.map(mapping_utl_to_int)
    stat_utl["dsp_utl"] = stat_utl.utl_int.map(mapping_utl_to_dsp)
    stat_utl["taux_occupation"] = np.round(
        stat_utl["total_h_assignees"] / stat_utl["dsp_utl"], 2
    )
    stat_utl = stat_utl.reset_index().drop("utl_int", axis=1)

    assert all(stat_utl["niveau_moyen_execution_tsk"] >= 0)
    assert all(stat_utl["niveau_moyen_execution_tsk"] <= 3)
    assert all(stat_utl["total_h_assignees"].values <= stat_utl["dsp_utl"].values)
    assert all(stat_utl["taux_occupation"] <= 1)
    assert all(stat_utl["taux_occupation"] >= 0)
    return stat_utl


def make_stat_tsk(
    df_out: pd.DataFrame, mapping_tsk_to_lgt: dict, mapping_int_to_tsk: dict
) -> pd.DataFrame:
    """
    Production de statistiques par tache
    """
    n_utl_per_tsk = (
        df_out.loc[df_out["utl"] != "not assigned"]
        .groupby("tsk")["utl"]
        .count()
        .rename("n_utl_per_tsk")
        .astype(int)
    )
    tmp = pd.Series(mapping_tsk_to_lgt).sort_index()
    tmp = tmp.set_axis(list(mapping_int_to_tsk.values()), copy=False)
    pct_per_tsk = (
        (
            df_out.loc[df_out["utl"] != "not assigned"]
            .groupby("tsk")["duree_assignee"]
            .sum()
            / tmp
        )
        .fillna(0)
        .rename("pct_assignation_tache")
        * 100
    ).astype(int)
    stat_tsk = pd.DataFrame([n_utl_per_tsk, pct_per_tsk]).T
    stat_tsk["n_utl_per_tsk"] = stat_tsk["n_utl_per_tsk"].fillna(0).astype(int)
    stat_tsk["pct_assignation_tache"] = stat_tsk["pct_assignation_tache"].astype(int)
    stat_tsk.reset_index(inplace=True)
    stat_tsk.sort_values(by="pct_assignation_tache", inplace=True)
    stat_tsk.rename(mapper={"index": "tsk"}, axis=1, inplace=True)
    stat_tsk.reset_index(inplace=True, drop=True)

    assert all(stat_tsk["pct_assignation_tache"] >= 0)
    assert all(stat_tsk["pct_assignation_tache"] <= 100)
    assert all(stat_tsk["n_utl_per_tsk"] >= 0)
    return stat_tsk


def make_stat_prj(df_out: pd.DataFrame) -> pd.DataFrame:
    """
    Production de statistiques par projet
    """
    unassigned_time_per_prj = (
        df_out.groupby("prj")["duree_non_assignee"]
        .sum()
        .rename("total_h_non_assignees")
    )
    n_missing_cmp_per_prj = (
        df_out.loc[df_out["utl"] == "not assigned"]
        .groupby("prj")["cmp"]
        .count()
        .rename("n_missing_cmp_per_prj")
    )
    stat_prj = pd.DataFrame([unassigned_time_per_prj, n_missing_cmp_per_prj]).T
    stat_prj.reset_index(inplace=True)
    stat_prj["n_missing_cmp_per_prj"] = (
        stat_prj["n_missing_cmp_per_prj"].fillna(0).astype(int)
    )
    stat_prj.sort_values("total_h_non_assignees", ascending=False, inplace=True)
    stat_prj.reset_index(inplace=True, drop=True)
    assert all(stat_prj["n_missing_cmp_per_prj"] >= 0)
    assert all(stat_prj["total_h_non_assignees"] >= 0)
    return stat_prj
