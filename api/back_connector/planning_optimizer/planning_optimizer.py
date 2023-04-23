"""
Module de récupération des données auprès du BACK pour la fonctionnalité planning_optimizer.
"""
import pandas as pd
from werkzeug.exceptions import UnprocessableEntity
from api.back_connector.planning_optimizer.data_handlers.filtrage import filtre
from api.back_connector.tools import make_sql_requests
from api.loggers import logger_planning_optimizer
from api.string_keys import *
from api.back_connector.planning_optimizer.requests import get_request_tasks, get_request_horaires, get_request_imperatifs


def fetch_data_to_wandeed_backend(url: str,
                                  access_token: str,
                                  date_start: str,
                                  date_end: str,
                                  selected_users: list[int] | None,
                                  key_project_prioritys_projets: dict | None) -> tuple[dict[int: pd.DataFrame],
                                                                                dict[int: pd.DataFrame],
                                                                                dict[int: pd.DataFrame],
                                                                                list[int]]:
    """
    Prépare et envoie les requêtes SQL auprès du Back Wandeed qui renvoie les données demandées.

    :param url: url de la base de données du back
    :param access_token: token d'accès à la base de données du back
    :param date_start: date de début du sprint à optimiser, au format ISO. example : "2022-10-03T06:31:00.000Z"
    :param date_end: date de FIN du sprint à optimiser, au format ISO. example : "2022-10-10T18:30:00.000Z"
    :param selected_users: IDs des utilisateurs sélectionnés pour l'optimisation
    :param key_project_prioritys_projets: dictionnaire de la forme {id_projet (int):niveau_key_project_priority_projet (int)}.
                             Niveau le plus important: 0.

    :return df_imp:
        TODO: à compléter

    :return df_hor: dataframe contenant les horaires des utilisateurs
        epu_sfkutilisateur  -> id de l'utilisateur
        key_debut_periode_horaire_utilisateur   -> debut de période d'application de l'horaire
        key_fin_periode_horaire_utilisateur     -> fin de période d'application de l'horaire
        key_epl_employe_horaire -> horaire de l'employe

    :return df_tsk:
        duree_evenement          -> duree (en h) de la tâche
        evenement    -> id de la tâche
        competence  -> utilisateur concerné
        evenement_project       -> projet de rattachement de la tâche
    """
    sql_querys_dict = {
        PO_MY_KEY_TACHES: get_request_tasks(date_start=date_start, date_end=date_end, selected_users=selected_users),
        PO_MY_KEY_HORAIRES: get_request_horaires(date_start=date_start, date_end=date_end, selected_users=selected_users),
        PO_MY_KEY_IMPERATIFS: get_request_imperatifs(date_start=date_start, date_end=date_end, selected_users=selected_users),
    }

    data = make_sql_requests(sql_querys_dict, url, access_token)

    # premier check des données. check qu'on a au moins une données pour les taches.
    for required_data_key in PO_REQUIRED_KEYS:
        if len(data[required_data_key]) == 0:
            raise UnprocessableEntity(description=PO_missing_data_msg[required_data_key])

    # Mise en forme des données
    df_tsk = pd.DataFrame(data[PO_MY_KEY_TACHES])
    df_tsk.dropna(inplace=True)
    if len(df_tsk) == 0:
        raise UnprocessableEntity(description=PO_missing_data_msg[PO_MY_KEY_TACHES])

    df_tsk[key_evenement_project] = df_tsk[key_evenement_project].astype(int)
    df_tsk = df_tsk[[key_evenement_project, key_evenement, key_user_po, key_duree_evenement,
                     key_evenement_date_debut, key_evenement_date_fin]]
    df_tsk.sort_values(by=[key_evenement_project, key_evenement, key_user_po], inplace=True)
    df_tsk.reset_index(inplace=True, drop=True)

    df_hor = pd.DataFrame(data[PO_MY_KEY_HORAIRES])
    if len(df_hor) > 0:
        df_hor = df_hor.reindex(
            columns=[
                key_epu_sfkutilisateur,
                key_debut_periode_horaire_utilisateur,
                key_fin_periode_horaire_utilisateur,
                key_epl_employe_horaire,
            ]
        )
        df_hor.epl_xdebutperiode = pd.to_datetime(df_hor.epl_xdebutperiode).dt.date
        df_hor.epl_xfinperiode = pd.to_datetime(df_hor.epl_xfinperiode).dt.date
        df_hor = df_hor.sort_values(
            by=[key_epu_sfkutilisateur, key_debut_periode_horaire_utilisateur]
        ).reset_index(drop=True)

    df_imp = pd.DataFrame(data[PO_MY_KEY_IMPERATIFS])
    if len(df_imp) > 0:
        df_imp = df_imp[[key_user_po, key_evenement, key_duree_evenement, key_evenement_date_debut, key_evenement_date_fin]]
        df_imp = df_imp.sort_values(by=[key_user_po, key_evenement])
        df_imp[key_evenement_date_debut] = pd.to_datetime(df_imp[key_evenement_date_debut])
        df_imp[key_evenement_date_fin] = pd.to_datetime(df_imp[key_evenement_date_fin])

    imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires = filtre(
        df_imp, df_hor, df_tsk, key_project_prioritys_projets
    )
    return imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires
