"""Contient les noms des champs utilisés en BDD Wandeed"""

# clé BDD Wandeed :
key_competence = "lgl_sfkligneparent"
key_user_po = "evu_sfkutilisateur"
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
KEY_DUREE_EFFECTUEE = "DUREE_EFFECTUEE"
KEY_PCT_COMPLETION = "PERCENT_COMPLETION"

PO_MY_KEY_IMPERATIFS = "IMPERATIFS"
PO_MY_KEY_HORAIRES = "HORAIRES"
PO_MY_KEY_TACHES = "TACHES"

PO_REQUIRED_KEYS = [PO_MY_KEY_TACHES]

PO_missing_data_msg = {PO_MY_KEY_TACHES: "Aucune donnée valide récupérée pour les tâches à optimiser. Assurez-vous que sur la période indiquée, il existe bien des tâches faisant référence à des projets."}

TA_MY_KEY_MATRICE_COMPETENCE = "MATRICE_COMPETENCE"
TA_MY_KEY_DISPOS_UTILISATEURS = "DISPONIBILITES_UTILISATEURS"
TA_MY_KEY_MATRICE_PROJET = "MATRICE_PROJET"
TA_MY_KEY_TACHES_A_ASSIGNER = "TACHES_A_ASSIGNER"
TA_REQUIRED_KEYS = [TA_MY_KEY_MATRICE_PROJET, TA_MY_KEY_MATRICE_COMPETENCE,
                    TA_MY_KEY_DISPOS_UTILISATEURS, TA_MY_KEY_TACHES_A_ASSIGNER]

TA_missing_data_msg = {TA_MY_KEY_DISPOS_UTILISATEURS: "les disponibilités des utilisateurs.",
                       TA_MY_KEY_MATRICE_COMPETENCE: "la matrice de compétence est inexistante pour les utilisateurs sélectionnés. Veillez à bien renseigner les niveaux des utilisateurs pour chacune de leurs compétences.",
                       TA_MY_KEY_TACHES_A_ASSIGNER: "les tâches à assigner. Veillez à ce qu'il y ait bien pour la période sélectionnée, des tâches faisant références à des compétences.",
                       TA_MY_KEY_MATRICE_PROJET: "la matrice projet. Cette matrice renseigne pour chaque projet la liste des utilisateurs concernée. Veillez à ce que celle-ci soit bien remplie ou relacher la contrainte 'etre_sur_projet' à Faux."}

for key, val in TA_missing_data_msg.items():
    TA_missing_data_msg[key] = "Aucune donnée valide récupérée pour " + val
