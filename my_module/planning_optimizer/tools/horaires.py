"""
Module des fonctions servant à manipuler les horaires des utilisateurs
"""
import pandas as pd
import datetime


def find_first_plage_horaire(df_hor: pd.DataFrame, date_debut: pd.Timestamp) -> int:
    """
    Trouve dans le dataframe d'horaire la première plage horaire par laquelle l'utilsateur va commencer son sprint
    étant donné la date de début du sprint.
    Renvoie l'index du data frame de la plage horaire concernée.
    """
    day0 = date_debut.weekday()
    found = False

    while not found:
        premieres_plages_horaires_valides = df_hor.loc[df_hor['eeh_sfkperiode'] == day0]

        on_debut_day = len(premieres_plages_horaires_valides) > 0 and day0 == date_debut.weekday()

        if on_debut_day:
            # Si on a trouvé des plages horaires qui tombent le premier jour du sprint, il faut prendre celle qui
            # contient le timestamp de la date début.
            # Exemple, le sprint commence lundi à 15h, la personne fait 8h-12 et 13h-17h tous les jours. Elle
            # commence donc le lundi sur sa deuxième plage horaire de 13h à 17h.
            premieres_plages_horaires_valides = premieres_plages_horaires_valides.loc[
                (premieres_plages_horaires_valides['eeh_xheurefin'] >= str(date_debut.time())),
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


def avance_cuseur_temps(curseur_temps: pd.Timestamp, ph: pd.Series) -> pd.Timestamp:
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
    return curseur_temps
