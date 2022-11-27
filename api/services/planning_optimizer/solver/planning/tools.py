"""
Module des fonctions servant à manipuler les horaires des utilisateurs
"""
import pandas as pd
import datetime


def find_next_ph(df_hor: pd.DataFrame, curseur_temps: pd.Timestamp) -> int:
    """
    Trouve dans le dataframe d'horaire la prochaine plage horaire utilisée à remplir étant donné le temps courant
    curseur_temps.
    Renvoie l'index du data frame de la plage horaire concernée.
    """
    day0 = curseur_temps.weekday()
    found = False
    str_heure_curseur = str(curseur_temps.time())
    while not found:
        if day0 == curseur_temps.weekday():
            premieres_plages_horaires_valides = df_hor.loc[
                (df_hor["eeh_sfkperiode"] == day0)
                & (str_heure_curseur < df_hor["eeh_xheurefin"])
            ]
        else:
            premieres_plages_horaires_valides = df_hor.loc[
                df_hor["eeh_sfkperiode"] == day0
            ]
        found = len(premieres_plages_horaires_valides) > 0
        if not found:
            # il faut essayer le jour suivant de la semaine.
            day0 = (day0 + 1) % 7
    first_plage_horaire_index = premieres_plages_horaires_valides.index[0]
    return first_plage_horaire_index


def avance_cuseur_temps(
    curseur_temps: pd.Timestamp, date_end_sprint: pd.Timestamp, ph: pd.Series
) -> pd.Timestamp:
    """
    Amène le curseur temps courant à la fin de la prochaine plage horaire ph utilisée.
    """
    day_ph = ph["eeh_sfkperiode"]
    if curseur_temps.weekday() <= day_ph:
        diff_days = day_ph - curseur_temps.weekday()
    else:
        diff_days = 7 - (curseur_temps.weekday() - day_ph)

    curseur_temps = curseur_temps + datetime.timedelta(days=int(diff_days))
    hour_ph = int(ph["eeh_xheurefin"][:2])
    minutes_ph = int(ph["eeh_xheurefin"][-2:])
    curseur_temps = curseur_temps.replace(hour=hour_ph, minute=minutes_ph, second=0)
    curseur_temps = min(curseur_temps, date_end_sprint)
    return curseur_temps


def make_df_ph(plages_horaires_df: pd.DataFrame,
               date_start: str,
               date_end: str,
               longueur_min_ph: float = 10.0) -> pd.DataFrame:
    """
    :param plages_horaires_df: pd.DataFrame des horaires d'un utilisateur
    :param date_start: str au format ISO, date de début du sprint
    :param date_end: str au format ISO, date de fin du sprint
    :param longueur_min_ph: float indiquant la durée minimale en heures d'une plage horaire sur laquelle
    on va planifier des tâches.

    :return df_ph: dataframe des plages horaires, chacune déterminées par un timestamp de début et de fin,
    des intervalles de temps sur lesquels des tâches vont pouvoir être planifiées.
    """
    date_start = pd.Timestamp(date_start)
    date_end = pd.Timestamp(date_end)
    curseur_temps = date_start

    sequence_ph = []
    while curseur_temps < date_end:
        index_next_ph = find_next_ph(plages_horaires_df, curseur_temps)
        next_ph = plages_horaires_df.iloc[index_next_ph]
        next_ph_dict = next_ph.to_dict()
        curseur_temps = avance_cuseur_temps(curseur_temps, date_end, next_ph)
        next_ph_dict["timestamp_fin"] = curseur_temps
        next_ph_dict["timestamp_debut"] = curseur_temps.replace(
            hour=int(next_ph.eeh_xheuredebut[:2]),
            minute=int(next_ph.eeh_xheuredebut[-2:]),
            second=0,
        )
        if next_ph_dict["timestamp_debut"] < date_end:
            sequence_ph.append(pd.DataFrame([next_ph_dict]))

    # TODO: retirer plages horaires trop courtes
    out = pd.concat(sequence_ph)

    out.loc[out["timestamp_debut"] < date_start, "timestamp_debut"] = date_start
    out.loc[out["timestamp_fin"] > date_end, "timestamp_fin"] = date_end

    out = out[["timestamp_debut", "timestamp_fin"]]
    df_ph = out.reset_index(drop=True)
    return df_ph


def add_imperatifs(df_ph: pd.DataFrame, imperatifs: pd.DataFrame | None, longueur_min_ph: float):
    """
    A partir d'un dataframe de plage horaires disponibles de travail, et d'un dataframe d'impératifs (événements
    non-repanifiables), retourne les nouvelles plages horaires qui prennent en compte les impératifs.

    :param df_ph: dataframe des plages horaires, chacune déterminées par un timestamp de début et de fin,
    des intervalles de temps sur lesquels des tâches vont pouvoir être planifiées.
    :param imperatifs: dataframe des impératifs, déterminés par un timestamp de début et de fin,
    des intervalles de temps pour lesquels des événements non-replanifiables existent.
    :param longueur_min_ph: float indiquant la durée minimale en heures d'une plage horaire sur laquelle
    on va planifier des tâches.
    """
    if imperatifs is None:
        return df_ph
    else:
        # TODO: à rédiger
        return df_ph
