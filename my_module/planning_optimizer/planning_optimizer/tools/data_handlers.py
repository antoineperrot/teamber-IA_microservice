from typing import List
import pandas as pd


def handler_clean_hor(hor: pd.DataFrame) -> pd.DataFrame:
    hor.sort_values(
        by=["eeh_sfkperiode", "eeh_xheuredebut", "eeh_xheurefin"], inplace=True
    )
    hor = hor[["eeh_sfkperiode", "eeh_xheuredebut", "eeh_xheurefin"]]
    hor.reset_index(drop=True, inplace=True)

    hor = hor.loc[hor["eeh_xheuredebut"] <= hor["eeh_xheurefin"]]
    hor.reset_index(drop=True, inplace=True)
    return hor


def handler_list_hor_utl(list_hor_utl: List[pd.DataFrame]) -> pd.DataFrame:
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

        final_row = {
            "eeh_sfkperiode": day,
            "eeh_xheuredebut": final_hd,
            "eeh_xheurefin": final_hf,
        }

        out = out.append(final_row, ignore_index=True)

    out["eeh_sfkperiode"] = out["eeh_sfkperiode"].astype(int)

    return out
