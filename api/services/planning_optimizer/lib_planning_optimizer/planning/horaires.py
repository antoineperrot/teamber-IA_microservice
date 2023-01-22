"""
Module des fonctions servant à manipuler les horaires des utilisateurs
"""
import datetime

import pandas as pd
from api.string_keys import *
from api.loggers import logger_planning_optimizer


class NoAvailabilitiesException(Exception):
    """Exception à lever lorsqu'un utilisateur n'a aucune disponibilité"""

    def __init__(self, id_utl: int | None = None):
        self.msg = f"L'utilsateur {id_utl} n'a aucune disponibilité compte tenu de ses horaires et de la période" \
                   f"indiquée."

    def __repr__(self):
        return self.msg


def find_next_ph(df_hor: pd.DataFrame,
                 curseur_temps: pd.Timestamp) -> int:
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
                (df_hor[key_day_plage_horaire] == day0)
                & (str_heure_curseur < df_hor[key_fin_plage_horaire])
            ]
        else:
            premieres_plages_horaires_valides = df_hor.loc[
                df_hor[key_day_plage_horaire] == day0
            ]
        found = len(premieres_plages_horaires_valides) > 0
        if not found:
            # il faut essayer le jour suivant de la semaine.
            day0 = (day0 + 1) % 7
    first_plage_horaire_index = premieres_plages_horaires_valides.index[0]
    return first_plage_horaire_index


def avance_cuseur_temps(curseur_temps: pd.Timestamp,
                        date_end_sprint: pd.Timestamp, ph: pd.Series) -> pd.Timestamp:
    """
    Amène le curseur temps courant à la fin de la prochaine plage horaire ph utilisée.
    """
    day_ph = ph[key_day_plage_horaire]
    if curseur_temps.weekday() <= day_ph:
        diff_days = day_ph - curseur_temps.weekday()
    else:
        diff_days = 7 - (curseur_temps.weekday() - day_ph)

    curseur_temps = curseur_temps + datetime.timedelta(days=int(diff_days))
    hour_ph = int(ph[key_fin_plage_horaire][:2])
    minutes_ph = int(ph[key_fin_plage_horaire][-2:])
    curseur_temps = curseur_temps.replace(hour=hour_ph, minute=minutes_ph, second=0)
    curseur_temps = min(curseur_temps, date_end_sprint)
    return curseur_temps


def make_base(
    working_times: pd.DataFrame,
    date_start: datetime.datetime,
    date_end: datetime.datetime,
    min_duration_section: float = 0.5,
) -> pd.DataFrame:
    """
    :param working_times: pd.DataFrame des horaires d'un utilisateur
    :param date_start: str au format ISO, date de début du sprint
    :param date_end: str au format ISO, date de fin du sprint
    :param min_duration_section: float indiquant la durée minimale en heures d'une plage horaire sur laquelle
    on va planifier des tâches.

    :return df_ph: dataframe des plages horaires, chacune déterminées par un timestamp de début et de fin,
    des intervalles de temps sur lesquels des tâches vont pouvoir être planifiées.
    """
    date_start = pd.to_datetime(date_start)
    date_end = pd.to_datetime(date_end)
    curseur_temps = date_start

    sequence_ph = []
    # TODO : corriger keys columns ?
    while curseur_temps < date_end:
        index_next_ph = find_next_ph(working_times, curseur_temps)
        next_ph = working_times.iloc[index_next_ph]
        next_ph_dict = next_ph.to_dict()
        curseur_temps = avance_cuseur_temps(curseur_temps, date_end, next_ph)
        next_ph_dict[KEY_TIMESTAMP_FIN] = curseur_temps
        next_ph_dict[KEY_TIMESTAMP_DEBUT] = curseur_temps.replace(
            hour=int(next_ph[key_debut_plage_horaire][:2]),
            minute=int(next_ph[key_debut_plage_horaire][-2:]),
            second=0,
        )
        if next_ph_dict[KEY_TIMESTAMP_DEBUT] < date_end:
            sequence_ph.append(pd.DataFrame([next_ph_dict]))

    if len(sequence_ph) == 0:
        out = pd.DataFrame.from_dict({KEY_TIMESTAMP_DEBUT: [], KEY_TIMESTAMP_FIN: []})
        return out

    out = pd.concat(sequence_ph)

    out.loc[out[KEY_TIMESTAMP_DEBUT] < date_start, KEY_TIMESTAMP_DEBUT] = date_start
    out.loc[out[KEY_TIMESTAMP_FIN] > date_end, KEY_TIMESTAMP_FIN] = date_end

    out = out[[KEY_TIMESTAMP_DEBUT, KEY_TIMESTAMP_FIN]]
    out[KEY_DUREE] = out[KEY_TIMESTAMP_FIN] - out[KEY_TIMESTAMP_DEBUT]
    out[KEY_DUREE] = out[KEY_DUREE] / datetime.timedelta(hours=1)
    out = out.loc[out[KEY_DUREE] >= min_duration_section]
    out = out.reset_index(drop=True)
    _data = [True] + list(
        out.iloc[1:][KEY_TIMESTAMP_DEBUT].values >= out.iloc[:-1][KEY_TIMESTAMP_FIN].values
    )
    _index = list(range(len(_data)))
    valid_indexes = pd.Series(data=_data, index=_index)
    out = out.loc[valid_indexes]
    out = out.reset_index(drop=True)
    return out


def find_next_section_ends(remaining_imp: pd.DataFrame,
                           date_end: pd.Timestamp) -> tuple[pd.Timestamp, pd.Timestamp, pd.DataFrame]:
    """
    Retourne la date de début et de fin du prochain impératifs se trouvant dans un dataframe d'impératifs restant.
    Attention, il se peut que des impératifs se chevauchent dans le temps.
    Cette fonction prend un compte cette éventualité.
    La fontion retourne également le dataframe des impératifs restant, càd futur end_next_imp

    :param remaining_imp: un dataframe d'impératifs futurs.
    :param date_end: Timestamp de la date de fin de sprint

    :return start_next_imp: Timestamp de la date de début de la prochaine indisponibilité lié aux remaining_imp
    :return end_next_imp: Timestamp de la date de fin de la prochaine indisponibilité lié aux remaining_imp
    :return remaining_imp: impératifs futurs à end_next_imp.


    :param remaining_imp: dataframe d'imperatifs restants à traiter
    """
    arg_start_next_imp = remaining_imp[key_evenement_date_debut].argmin()
    end_next_imp = remaining_imp.iloc[arg_start_next_imp][key_evenement_date_fin]
    start_next_section = remaining_imp.iloc[arg_start_next_imp][key_evenement_date_fin]
    remaining_imp = remaining_imp.drop(arg_start_next_imp, axis=0)

    evt_a_cheval = remaining_imp.loc[remaining_imp[key_evenement_date_debut] <= end_next_imp]
    if len(evt_a_cheval) > 0:
        start_next_section = evt_a_cheval[key_evenement_date_fin].max()
        remaining_imp = remaining_imp.drop(evt_a_cheval.index, axis=0)

    end_next_section = (
        min(remaining_imp[key_evenement_date_debut].min(), date_end)
        if len(remaining_imp) > 0
        else date_end
    )
    remaining_imp.reset_index(drop=True, inplace=True)
    return start_next_section, end_next_section, remaining_imp


def find_sections_ends(
    imperatifs: pd.DataFrame, date_start: pd.Timestamp, date_end: pd.Timestamp
) -> pd.DataFrame:
    """
    Découpe un sprint en plusieurs sous-sprint. Les sous-sprint sont les disponibilités d'un impératif au suivant.
    """
    remaining_imp = imperatifs

    sections_starts = []
    sections_ends = []

    # ajout première section à partir de date_start:
    sections_starts.append(date_start)
    sections_ends.append(imperatifs[key_evenement_date_debut].min())

    while len(remaining_imp) > 0:
        start_next_section, end_next_section, remaining_imp = find_next_section_ends(
            remaining_imp, date_end
        )
        sections_starts.append(start_next_section)
        sections_ends.append(end_next_section)

    dict_start_next_section = {
        i: section_start for i, section_start in enumerate(sections_starts)
    }
    dict_end_next_section = {
        i: section_end for i, section_end in enumerate(sections_ends)
    }
    out = pd.DataFrame.from_dict(
        {KEY_START: dict_start_next_section, KEY_END: dict_end_next_section}
    )
    return out


def compute_availabilities(
    working_times: pd.DataFrame,
    imperatifs: pd.DataFrame,
    date_start: datetime.datetime,
    date_end: datetime.datetime,
    min_duration_section: float,
) -> pd.DataFrame:
    """
    A partir des horaires d'un utilisateur, de ses impératifs (événements non-replanifiables), d'une date de
    début et de fin de sprint, retourne les créneaux sur lesquels l'utilisateur est disponible.
    """
    if len(imperatifs) == 0:
        availabilities = make_base(working_times=working_times,
                                   date_start=pd.Timestamp(date_start),
                                   date_end=pd.Timestamp(date_end),
                                   min_duration_section=min_duration_section)
    else:
        sections_ends = find_sections_ends(imperatifs=imperatifs,
                                           date_start=pd.Timestamp(date_start),
                                           date_end=pd.Timestamp(date_end))

        bases = [
            make_base(working_times=working_times,
                      date_start=section_start,
                      date_end=section_end,
                      min_duration_section=min_duration_section)
            for (section_start, section_end) in sections_ends.values
        ]
        availabilities = pd.concat(bases)

    if len(availabilities) == 0:
        raise

    availabilities.reset_index(inplace=True, drop=True)
    return availabilities
