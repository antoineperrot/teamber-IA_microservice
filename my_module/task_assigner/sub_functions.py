import pandas as pd
import numpy as np
from scipy.optimize import linprog

def split_data_from_dic(dic):
    """
    RECUPERATION DES DONNEES
    """
    
    # recuperation matrice_projet
    df_prj = pd.DataFrame(dic['matrice_projet']['data']['result'])
    # recuperation matrice_competence : on oublie les compétences pour lesquels les utl sont indéfinis
    df_cmp = pd.DataFrame(dic['matrice_competence']['data']['result']).dropna().reset_index(drop=True).astype(int)
    # recuperation des taches à assigner :
    df_tsk = pd.DataFrame(dic['taches']['data']['result'])
    # recuperation des disponibilites utl :
    df_dsp = pd.DataFrame(dic['dispos_utilisateurs']['data']['result'])
    
    return df_prj, df_cmp, df_tsk, df_dsp

def flatten_list(list_of_list):
    out = []
    for sublist in list_of_list : 
        for item in sublist : out.append(item)
    return out

def make_list_ids(df_prj, df_cmp, df_tsk, df_dsp):
    """
    FAIT LA LISTE DE TOUS LES IDS (PRJ, CMP, TSK, UTL) CONTENUS DANS LES DONNEES RECUES
    """
    # sauvegarde des id utilisateurs ET conservation des ids_utl uniques
    lst_utl = []
    lst_utl.append(list(np.unique(df_prj['utl_spkutilisateur'])))
    lst_utl.append(list(np.unique(df_cmp['emc_sfkutilisateur'])))
    lst_utl.append(list(np.unique(df_dsp['utl_spkutilisateur'])))
    id_utl = list(np.sort(np.unique(flatten_list(lst_utl))))
    
    # sauvegarde des id projets ET conservation des ids_prj uniques
    lst_prj = []
    lst_prj.append(list(np.unique(df_prj['int_sfkprojet'])))
    lst_prj.append(list(np.unique(df_tsk['evt_sfkprojet'])))
    id_prj = list(np.sort(np.unique(flatten_list(lst_prj))))
    
    # sauvegardes des ids competences ET conservation des ids_cmp uniques
    lst_cmp = []
    lst_cmp.append(list(np.unique(df_cmp['emc_sfkarticle'])))
    lst_cmp.append(list(np.unique(df_tsk['lgl_sfkligneparent'])))
    id_cmp = list(np.sort(np.unique(flatten_list(lst_cmp))))
    
    # sauvegardes des ids tsk ET conservation des ids_tsk uniques
    lst_tsk = []
    id_tsk = list(np.sort(np.unique(df_tsk['evt_spkevenement'])))
    
    return id_utl, id_prj, id_cmp, id_tsk

def make_mapping_dicts_extern_to_local(id_utl, id_prj, id_cmp, id_tsk):
    """
    CONVERSION DES IDS Wandeed en Identifiant local
    """
    utl_to_int = {int(_id) : int(_int) for _int,_id in enumerate(id_utl)}
    prj_to_int = {int(_id) : int(_int) for _int,_id in enumerate(id_prj)}
    cmp_to_int = {int(_id) : int(_int) for _int,_id in enumerate(id_cmp)}
    tsk_to_int = {int(_id) : int(_int) for _int,_id in enumerate(id_tsk)}
    return utl_to_int, prj_to_int, cmp_to_int, tsk_to_int

def make_mapping_dicts_local_to_extern(id_utl, id_prj, id_cmp, id_tsk):
    """
    CONVERSION DES Identifiant local en IDS Wandeed
    """
    int_to_utl = {int(_int): int(_id)  for _int,_id in enumerate(id_utl)}
    int_to_utl['not assigned'] = 'not assigned'
    int_to_prj = {int(_int): int(_id)  for _int,_id in enumerate(id_prj)}
    int_to_cmp = {int(_int): int(_id)  for _int,_id in enumerate(id_cmp)}
    int_to_tsk = {int(_int): int(_id)  for _int,_id in enumerate(id_tsk)}
    return int_to_utl, int_to_prj, int_to_cmp, int_to_tsk

def add_local_ids_in_dfs(df_prj, df_cmp, df_tsk, df_dsp,
                        cmp_to_int, utl_to_int, tsk_to_int, prj_to_int):
    """
    AJOUT DES VARIABLES LOCALES DANS LES DATAFRAMES
    """
    df_cmp['cmp'] = df_cmp['emc_sfkarticle'].map(cmp_to_int)
    df_cmp['utl'] = df_cmp['emc_sfkutilisateur'].map(utl_to_int)
    df_tsk['tsk'] = df_tsk['evt_spkevenement'].map(tsk_to_int)
    df_tsk['cmp'] = df_tsk['lgl_sfkligneparent'].map(cmp_to_int)
    df_tsk['prj'] = df_tsk['evt_sfkprojet'].map(prj_to_int)
    df_prj['utl'] = df_prj['utl_spkutilisateur'].map(utl_to_int)
    df_prj['prj'] = df_prj['int_sfkprojet'].map(prj_to_int)
    df_dsp['utl'] = df_dsp['utl_spkutilisateur'].map(utl_to_int)

    # commodités pour plus tard
    df_cmp = df_cmp.sort_values(by='utl')
    return df_prj, df_cmp, df_tsk, df_dsp

def make_mat_prj(df_prj,n_prj, n_utl):
    """
    FABRICATION MATRICE PROJET
    """
    # construction d'un dictionnaire qui contient, pour chaque prjet, la liste des utilisateurs en faisant parti.
    d_prj_to_utl = df_prj.groupby('prj')['utl'].apply(np.sort).to_dict()
    
    # REMPLISSAGE MATRICE PROJET :
    mat_prj = np.zeros((n_prj, n_utl)).astype(int)
    for prj in range(n_prj): 
        for utl in d_prj_to_utl[prj]:
            mat_prj[prj, utl] = 1
    
    return mat_prj

def make_mat_cmp(df_cmp, n_cmp, n_utl):
    """
    FABRICATION MATRICE COMPETENCE
    """
    
    # construction matrice de cmp np.array
    mat_cmp = np.zeros((n_cmp, n_utl)).astype(int)

    # REMPLISSAGE MATRICE DE COMPETENCE

    # ce dict est organisé en arborescence : utl//comp//niveau
    d_utl_to_cmp_to_lvl = {}
    utl_competants = list(np.unique(df_cmp['utl']))
    for utl in utl_competants:
        d_utl_to_cmp_to_lvl[utl] = {}
        df_cmp_tmp = df_cmp.loc[df_cmp['utl']==utl,]
        for i, row in df_cmp_tmp.iterrows():
            cmp = row['cmp'] ; lvl = row['emc_sniveau'];
            d_utl_to_cmp_to_lvl[utl][cmp] = lvl

    for utl in d_utl_to_cmp_to_lvl:
        for cmp in d_utl_to_cmp_to_lvl[utl].keys():
            lvl = d_utl_to_cmp_to_lvl[utl][cmp]
            mat_cmp[cmp, utl] = lvl
    
    return mat_cmp

def make_usefull_mapping_dicts(df_tsk, df_dsp):
    """
    FABRICATION DE DICTIONNAIRE UTILES PAR LA SUITE
    """
    d_tsk_to_cmp = {int(row['tsk']):int(row['cmp']) for i, row in df_tsk.iterrows()}
    d_tsk_to_prj = {int(row['tsk']):int(row['prj']) for i, row in df_tsk.iterrows()}
    d_tsk_to_lgt = {int(row['tsk']):row['evt_dduree'] for i, row in df_tsk.iterrows()}
    d_utl_to_dsp = {int(row['utl']):row['utl_sdispo'] for _, row in df_dsp.iterrows()}          
    d_utl_to_dsp['not assigned'] = np.sum(list(d_utl_to_dsp.values()))
    return d_tsk_to_cmp, d_tsk_to_prj, d_tsk_to_lgt, d_utl_to_dsp

def make_arcs_and_cost_func(n_tsk, n_utl, 
              d_tsk_to_cmp, d_tsk_to_prj,
              mat_cmp, mat_prj,
              penalty=-100):
    """
    FABRICATION DES ARCS RELIANT TACHES A UTILISATEURS POTENTIELS, AINSI QUE FONCTION DE COUT
    """
    arcs = []
    n_arcs = 0
    cost_func = []
    for tsk in range(n_tsk):
        for utl in range(n_utl):
            cmp = d_tsk_to_cmp[tsk]
            prj = d_tsk_to_prj[tsk]
            lvl = mat_cmp[cmp, utl]
            utl_on_prj = mat_prj[prj, utl]
            if lvl >= 0 and utl_on_prj : 
                arcs.append( tuple((tsk,utl)) )
                cost_func.append(lvl)

    # chaque tache a également la possibilité de ne pas être assignée, ce qui est fortement pénalisé
    for tsk in range(n_tsk):
        arcs.append(tuple((tsk,'not assigned')))
        cost_func.append(penalty)

    # ajout des variables df'écart (slack variables)
    cost_func += [0]*n_utl  
    cost_func = np.array(cost_func)
    n_arcs = len(arcs)
    return arcs, cost_func, n_arcs

def make_A_and_b(n_tsk,n_utl,n_arcs,
                 d_tsk_to_lgt, d_utl_to_dsp,
                 arcs):
    
    """
    FABRICATION DES MATRICES A et B POUR RESOUDRE AX<=B
    """
    
    #equality constraints :
    A = np.zeros((n_tsk + n_utl , n_arcs + n_utl ))
    b = np.zeros(n_tsk + n_utl)

    # contrainte d'égalité : distribution de toutes les heures
    for tsk in range(n_tsk):
        for idx_arc, arc in enumerate(arcs):
            if arc[0] == tsk:  A[tsk, idx_arc] = 1
        b[tsk] = d_tsk_to_lgt[tsk]

    # contraintes d'inégalités : respect des disponibilités de travail
    for utl in range(n_utl):
        for j in range(n_arcs - n_tsk):
            arc = arcs[j]
            utl_2 = arc[1]
            if utl_2 == utl : A[n_tsk + utl, j] = 1
        A[n_tsk + utl, n_arcs + utl] =   1 # variable d'écart (slack variable)
        b[n_tsk + utl] = d_utl_to_dsp[utl]
        
    return A, b

def solve_linear_programmation_problem(A, b, cost_func):    
    """
    RESOLUTION DU PROBLEME DE PROGRAMMATION LINEAIRE
    """
    method='simplex'
    l = linprog(-cost_func,A_eq=A,b_eq=b,method="simplex",options={'maxiter':10000})
    if l.status !=0 :
        l = linprog(-cost_func, A_eq=A,b_eq=b,method='interior-point',options={'maxiter':10000})
        outcome = l.message
        method = 'interior-point'
    else :
        outcome = l.message

    solution_vector = l.x
    return solution_vector, outcome, method

def make_output_dataframe(solution_vector, arcs, cost_func,
                          d_tsk_to_lgt, d_tsk_to_cmp, d_tsk_to_prj, d_utl_to_dsp):
    """
    MET EN FORME LA SOLUTION DANS UN DATAFRAME PANDAS
    """
    out = pd.DataFrame()
    for j in range(len(arcs)):
        if solution_vector[j] > 0 :
            tsk, utl = arcs[j]
            lvl = cost_func[j]
            out = out.append(pd.DataFrame({
                'prj':[d_tsk_to_prj[tsk]],
                'tsk':[tsk],'utl':[utl],
                'duree_assignee':[solution_vector[j]],
                'tsk_lgt':[d_tsk_to_lgt[tsk]],
                'duree_non_assignee':[d_tsk_to_lgt[tsk] - solution_vector[j]],
                'dsp_utl':[d_utl_to_dsp[utl]],
                'cmp':[d_tsk_to_cmp[tsk]],
                'lvl':[lvl],
                
            } ))
    out.reset_index(drop=True,inplace=True)  
    out.loc[out['utl']=='not assigned','lvl'] = None
    out.sort_values(by=['prj','tsk','utl'],inplace=True)
    return out

def remap_df_out(df_out,
                int_to_tsk, int_to_utl, int_to_prj, int_to_cmp):
    """
    REMAPPING DES ID LOCAUX EN ID WANDEED
    """
    df_out['tsk'] = df_out['tsk'].map(int_to_tsk)
    df_out['utl'] = df_out['utl'].map(int_to_utl)
    df_out['prj'] = df_out['prj'].map(int_to_prj)
    df_out['cmp'] = df_out['cmp'].map(int_to_cmp)
    df_out['duree_assignee'] = np.round(df_out['duree_assignee'],2)
    return df_out


def make_stat_cmp(df_out):
    """
    Production de statistiques par compétences
    """
    avg_lvl = np.round(df_out.loc[df_out['utl']!='not assigned'].groupby('cmp')['lvl'].mean().rename('niveau_cmp_moyen_par_h_realisee'),2)
    cmp_miss = df_out.loc[df_out['utl']=='not assigned'].groupby('cmp')['duree_assignee'].sum().rename('total_h_non_assignees')
    stat_cmp = pd.DataFrame([avg_lvl, cmp_miss]).T
    stat_cmp['total_h_non_assignees'] = stat_cmp['total_h_non_assignees'].fillna(0)
    stat_cmp.sort_values('total_h_non_assignees',ascending=False,inplace=True)
    stat_cmp.reset_index(inplace=True)
    return stat_cmp

def make_stat_utl(df_out, d_utl_to_dsp, utl_to_int):
    """
    Production de statistiques par utilisateur
    """
    avg_lvl = df_out[['utl','duree_assignee','lvl']].loc[df_out['utl']!='not assigned']
    avg_lvl['niveau_moyen_execution_tsk'] = avg_lvl['duree_assignee']*avg_lvl['lvl']
    avg_lvl_exe_tsk = np.round(avg_lvl.groupby('utl')['niveau_moyen_execution_tsk'].sum()/avg_lvl.groupby('utl')['duree_assignee'].sum(),1)
    avg_lvl_exe_tsk.rename('niveau_moyen_execution_tsk',inplace=True)
    tot_h = df_out.loc[df_out['utl']!='not assigned'].groupby('utl')['duree_assignee'].sum().rename('total_h_assignees')
    stat_utl = pd.DataFrame([avg_lvl_exe_tsk, tot_h]).T
    stat_utl['utl_int'] = stat_utl.index.map(utl_to_int)
    stat_utl['dsp_utl'] = stat_utl.utl_int.map(d_utl_to_dsp)
    stat_utl['taux_occupation'] = np.round(stat_utl['total_h_assignees'] / stat_utl['dsp_utl'], 2)
    stat_utl = stat_utl.reset_index().drop('utl_int',axis=1)
    return stat_utl

def make_stat_tsk(df_out, d_tsk_to_lgt, int_to_tsk):
    """
    Production de statistiques par tache
    """
    n_utl_per_tsk = df_out.loc[df_out['utl']!='not assigned'].groupby('tsk')['utl'].count().rename('n_utl_per_tsk').astype(int)
    tmp = pd.Series(d_tsk_to_lgt).sort_index()
    tmp.set_axis(list(int_to_tsk.values()),inplace=True)
    pct_per_tsk = ((df_out.loc[df_out['utl']!='not assigned'].groupby('tsk')['duree_assignee'].sum()/tmp).fillna(0).rename('pct_assignation_tache')*100).astype(int)
    stat_tsk = pd.DataFrame([n_utl_per_tsk, pct_per_tsk]).T
    stat_tsk['n_utl_per_tsk'] =  stat_tsk['n_utl_per_tsk'].fillna(0).astype(int)
    stat_tsk['pct_assignation_tache'] =  stat_tsk['pct_assignation_tache'].astype(int)
    stat_tsk.reset_index(inplace=True)
    stat_tsk.sort_values(by='pct_assignation_tache',inplace=True)
    stat_tsk.rename(mapper={"index":'utl'},axis=1,inplace=True)
    return stat_tsk

def make_stat_prj(df_out):
    """
    Production de statistiques par projet
    """
    unassigned_time_per_prj = df_out.groupby('prj')['duree_non_assignee'].sum().rename('total_h_non_assignees')
    n_missing_cmp_per_prj = df_out.loc[df_out['utl']=='not assigned'].groupby('prj')['cmp'].count().rename('n_missing_cmp_per_prj')
    stat_prj = pd.DataFrame([unassigned_time_per_prj, n_missing_cmp_per_prj]).T
    stat_prj.reset_index(inplace=True)
    stat_prj['n_missing_cmp_per_prj'] =  stat_prj['n_missing_cmp_per_prj'].fillna(0).astype(int)
    stat_prj.sort_values('total_h_non_assignees',ascending=False,inplace=True)
    return stat_prj



