"""Contient les noms des champs utilisés en BDD Wandeed"""

# clé BDD Wandeed :
key_competence = "lgl_sfkligneparent"
key_evenement = "evt_spkevenement"
key_duree_evenement = "evt_dduree"
key_evenement_project = "evt_sfkprojet"
key_project = "int_sfkprojet"
key_user = "utl_spkutilisateur"
key_user_dispo = "utl_sdispo"


key_day_plage_horaire = "eeh_sfkperiode"
key_debut_plage_horaire = "eeh_xheuredebut"
key_fin_plage_horaire = "eeh_xheurefin"
key_debut_periode_horaire_utilisateur = "epl_xdebutperiode"
key_fin_periode_horaire_utilisateur = "epl_xfinperiode"

# à interpréter
key_emc_sfkarticle = "emc_sfkarticle"
key_emc_sniveau = "emc_sniveau"
key_emc_sfkutilisateur = "emc_sfkutilisateur"

key_epu_sfkutilisateur = "epu_sfkutilisateur"
key_epl_employe_horaire = "epl_employe_horaire"

key_evenement_date_debut = "evt_xdate_debut"
key_evenement_date_fin = "evt_xdate_fin"

# clés noms tables BDD Wandeed :
key_table_evenements = "lst_vevenement_py"
key_table_horaires_utilisateurs = "lst_vutilisateur_horaires_py"

# mes clés locales :
KEY_TIMESTAMP_DEBUT = "TIMESTAMP_DEBUT"
KEY_TIMESTAMP_FIN = "TIMESTAMP_FIN"
KEY_PROJECT_PRIORITY = "KEY_PROJECT_PRIORITY"
KEY_DUREE = "DUREE"
KEY_ID_PART = "ID_PART"
KEY_DUREE_PART = "DUREE_PART"
KEY_NUMBER_PARTS = "N_PARTS"
KEY_NUMBER_FILLED_PARTS = "N_FILLED_PARTS"
KEY_START = "START"
KEY_END = "END"

MY_KEY_IMPERATIFS = "IMPERATIFS"
MY_KEY_HORAIRES = "HORAIRES"
MY_KEY_TACHES = "TACHES"

# Liste de clés requises dans les requêtes en BDD :
LIST_FIELD_KEYS_IMPERATIFS_REQUEST = [
                key_evenement,
                key_evenement_project,
                key_duree_evenement,
                key_competence,  # TODO : à remplacer par clé utilisateur
                key_evenement_date_debut,
                key_evenement_date_fin,
            ]

LIST_FIELD_KEYS_HORAIRES_REQUEST = [
                key_epu_sfkutilisateur,
                key_epl_employe_horaire,
                key_debut_periode_horaire_utilisateur,
                key_fin_periode_horaire_utilisateur,
            ]

LIST_FIELD_KEYS_TACHES_REQUEST = [
                key_evenement,
                key_evenement_project,
                key_duree_evenement,
                key_competence,  # TODO : à remplacer par clé utilisateur
            ]
