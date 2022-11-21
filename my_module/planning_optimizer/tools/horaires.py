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

    while not found:
        premieres_plages_horaires_valides = df_hor.loc[df_hor['eeh_sfkperiode'] == day0]

        on_same_day = len(premieres_plages_horaires_valides) > 0 and day0 == curseur_temps.weekday()

        if on_same_day:
            # Si on a trouvé des plages horaires qui tombent le même jour que le curseur, il faut prendre celle qui
            # contient le timestamp du curseur.
            # Exemple, le curseur est lundi à 15h, la personne fait 8h-12 et 13h-17h tous les jours ouvrés. Sa prochaine
            # plage est donc le lundi sur sa deuxième plage horaire de 13h à 17h.
            # On s'occupera ensuite de tronquer.
            premieres_plages_horaires_valides = premieres_plages_horaires_valides.loc[
                (premieres_plages_horaires_valides['eeh_xheurefin'] > str(curseur_temps.time())),
            ]
            found = len(premieres_plages_horaires_valides) > 0
            if not found:
                day0 = (day0 + 1) % 7
        elif len(premieres_plages_horaires_valides) > 0:
            # si on est pas sur le jour de la date de départ du sprint, alors on prend la première plage horaire
            # dispo.
            # Exemple, le sprint commence lundi à 18h, sauf que la personne fait 8h-12 et 13h-17h tous les jours. Elle
            # commence donc le mardi sur sa première plage horaire, de 8h à 12h.
            found = True
        else:
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
