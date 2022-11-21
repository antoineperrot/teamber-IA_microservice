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
            premieres_plages_horaires_valides = df_hor.loc[ (df_hor['eeh_sfkperiode'] == day0)
                                                           &(str_heure_curseur < df_hor['eeh_xheurefin'] )]
        else:
            premieres_plages_horaires_valides = df_hor.loc[df_hor['eeh_sfkperiode'] == day0]
        found = len(premieres_plages_horaires_valides) > 0
        if not found:
            # il faut essayer le jour suivant de la semaine.
            day0 = (day0 + 1) % 7
    first_plage_horaire_index = premieres_plages_horaires_valides.index[0]
    return first_plage_horaire_index


def avance_cuseur_temps(curseur_temps: pd.Timestamp, date_fin_sprint: pd.Timestamp, ph: pd.Series) -> pd.Timestamp:
    """
    Amène le curseur temps courant à la fin de la prochaine plage horaire ph utilisée.
    """
    day_ph = ph['eeh_sfkperiode']
    if curseur_temps.weekday() <= day_ph:
        diff_days = day_ph - curseur_temps.weekday()
    else:
        diff_days = 7 - (curseur_temps.weekday() - day_ph)

    curseur_temps = curseur_temps + datetime.timedelta(days=int(diff_days))
    hour_ph = int(ph['eeh_xheurefin'][:2])
    minutes_ph = int(ph['eeh_xheurefin'][-2:])
    curseur_temps = curseur_temps.replace(hour=hour_ph, minute=minutes_ph, second=0)
    curseur_temps = min(curseur_temps, date_fin_sprint)
    return curseur_temps
