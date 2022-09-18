import numpy as np
import pandas as pd
def validation_mathematique_solution(solution):
    solution = pd.DataFrame(solution)
    assert all(solution['duree_assignee'] >=0), "Un nombre d'heure négatif a été assigné."
    assert all(solution['duree_assignee'] <= solution['tsk_lgt']), "La durée assignée pour certaines tâches excède celle leur durée."

def validation_stat_cmp(stat_cmp):
    stat_cmp = pd.DataFrame(stat_cmp)
    assert all(stat_cmp['total_h_non_assignees'] >=0), "ValueError dans total_h_non_assignee"
    assert all(stat_cmp[~stat_cmp['niveau_cmp_moyen_par_h_realisee'].isna()]['niveau_cmp_moyen_par_h_realisee'] <= 3),"Mauvais calcul du niveau moyen d'exécution dune tache : > 3."
    assert all(stat_cmp[~stat_cmp['niveau_cmp_moyen_par_h_realisee'].isna()]['niveau_cmp_moyen_par_h_realisee'] >= 0),"Mauvais calcul du niveau moyen d'exécution dune tache : < 0."


def validation_stat_utl(stat_utl):
    stat_utl = pd.DataFrame(stat_utl)
    assert all(stat_utl.taux_occupation.apply(pd.notna)), "TypeError: les données de taux d'occupation contiennent des NaN."
    assert all(stat_utl.taux_occupation.apply(lambda x: (isinstance(x, float) or isinstance(x, int)) and x >= 0 and x <= 1 ) ), "TypeError: les données de taux d'occupation sont incorrectes."
    assert all(stat_utl.dsp_utl.apply(pd.notna)), "TypeError: les données de disponibilités totales contiennent des NaN."
    assert all(stat_utl.dsp_utl.apply(lambda x: (isinstance(x, float) or isinstance(x, int)) and x >= 0 ) ), "TypeError: les données de disponibilités totales sont incorrectes."
    assert all(stat_utl.dsp_utl.apply(lambda x: x >= 0 )), "TypeError: Certaines données de disponibilités totales sont négatives."
    assert all(stat_utl['total_h_assignees'] <= stat_utl['dsp_utl']  ), "Certains utilisateurs sont trop chargés par rapport à leurs disponibiltés."
    assert all(stat_utl['niveau_moyen_execution_tsk'] <= 3), "Le calcul du niveau moyen d'exécution d'une tache par unité de temps est FAUX."
    assert all(stat_utl['niveau_moyen_execution_tsk'] >= 0), "Le calcul du niveau moyen d'exécution d'une tache par unité de temps est FAUX."

def validation_stat_prj(stat_prj):
    stat_prj = pd.DataFrame(stat_prj)
    assert all(stat_prj['total_h_non_assignees'] >=0), "ValueError dans temps_total_non_assigne"
    assert all(stat_prj.n_missing_cmp_per_prj.apply(lambda x: isinstance(x,int))), "ValueError: Le nombre de compétences manquantes par projet n'est pas toujours un entier."

def validation_stat_tsk(stat_tsk):
    stat_tsk = pd.DataFrame(stat_tsk)
    assert all(stat_tsk.n_utl_per_tsk.apply(lambda x: isinstance(x,int))), "ValueError: Le nombre d'utilisateurs par tache n'est pas toujours un entier."


def validation_solution(OUT):
    success = True
    try:
        validation_validite_mathematique_solution(OUT['solution'])
        validation_stat_cmp(OUT['statistics_for']['cmp'])
        validation_stat_utl(OUT['statistics_for']['utl'])
        validation_stat_prj(OUT['statistics_for']['prj'])
        validation_stat_tsk(OUT['statistics_for']['tsk'])
    except :
        success = False

    return success