import numpy as np
import pandas as pd

def test_mapping(df_out):
    assert all(df_out.tsk.apply(lambda x: x in id_tsk)), "Certains id_tsk ne sont pas dans la liste des id_tsk fournis au départ."
    assert all(df_out.prj.apply(lambda x: x in id_prj)), "Certains id_prj ne sont pas dans la liste des id_prj fournis au départ."
    assert all(df_out.cmp.apply(lambda x: x in id_cmp)), "Certains id_cmp ne sont pas dans la liste des id_cmp fournis au départ."
    assert all(df_out.utl.apply(lambda x: x in id_utl +['not assigned'])), "Certains id_utl ne sont pas dans la liste des id_utl fournis au départ."

def test_validite_mathematique_solution(df_out, solution_vector):
    assert all(A @ solution_vector <= b + 1e-6), "Math : la solution_vector x ne respecte pas la contrainte Ax <= b."  # + 1e-6 : prise en compte d'une tolérance d'erreur d'arrondi numérique.
    assert all(df_out['duree_assignee'] >=0), "Un nombre d'heure négatif a été assigné."
    assert all(df_out['duree_assignee'] <= df_out['tsk_lgt']), "La durée assignée pour certaines tâches excède celle leur durée."

def test_stat_cmp(stat_cmp):
    assert all(stat_cmp['total_h_non_assignees'] >=0), "ValueError dans total_h_non_assignees"
    assert all(stat_cmp[~stat_cmp['niveau_cmp_moyen_par_h_realisee'].isna()]['niveau_cmp_moyen_par_h_realisee'] <= 3),"Mauvais calcul du niveau moyen d'exécution dune tache : > 3."
    assert all(stat_cmp[~stat_cmp['niveau_cmp_moyen_par_h_realisee'].isna()]['niveau_cmp_moyen_par_h_realisee'] >= 0),"Mauvais calcul du niveau moyen d'exécution dune tache : < 0."

def test_stat_utl(stat_utl):
    assert all(stat_utl.taux_occupation.apply(pd.notna)), "TypeError: les données de taux d'occupation contiennent des NaN."
    assert all(stat_utl.taux_occupation.apply(lambda x: (isinstance(x, float) or isinstance(x, int)) and x >= 0 and x <= 1 ) ), "TypeError: les données de taux d'occupation sont incorrectes."
    assert all(stat_utl.dsp_utl.apply(pd.notna)), "TypeError: les données de disponibilités totales contiennent des NaN."
    assert all(stat_utl.dsp_utl.apply(lambda x: (isinstance(x, float) or isinstance(x, int)) and x >= 0 ) ), "TypeError: les données de disponibilités totales sont incorrectes."
    assert all(stat_utl.dsp_utl.apply(lambda x: x >= 0 )), "TypeError: Certaines données de disponibilités totales sont négatives."
    assert all(stat_utl['total_h_assignees'] <= stat_utl['dsp_utl'] + 1e-1  ), "Certains utilisateurs sont trop chargés par rapport à leurs disponibiltés."
    assert all(stat_utl['niveau_moyen_execution_tsk'] <= 3), "Le calcul du niveau moyen d'exécution d'une tache par unité de temps est FAUX."
    assert all(stat_utl['niveau_moyen_execution_tsk'] >= 0), "Le calcul du niveau moyen d'exécution d'une tache par unité de temps est FAUX."
    
def test_stat_prj(stat_prj):
    assert all(stat_prj.total_h_non_assignees	 >=0), "ValueError dans total_h_non_assignees"
    assert all(stat_prj.n_missing_cmp_per_prj.apply(lambda x: isinstance(x,int))), "ValueError: Le nombre de compétences manquantes par projet n'est pas toujours un entier."

def test_stat_tsk(stat_tsk):
    assert all(stat_tsk.n_utl_per_tsk.apply(lambda x: isinstance(x,int))), "ValueError: Le nombre d'utilisateurs par tache n'est pas toujours un entier."
