

import numpy as np
import pandas as pd


def make_data(n_tasks       = 50,n_people      = 10,
    n_competences = 7,
    n_projets     = 20, seed=0):

    info_data = {'nombre de taches':n_tasks,
    'nombre utilisateurs':n_people,
    'nombre competences':n_competences,
    'nombre projets':n_projets}


    np.random.seed(seed)
    # GENERATION DE TACHES A REPARTIR
    #durée des taches
    durations    = np.random.randint(2,12,n_tasks)             
    # compétence requise pour une tache
    competences  = np.random.randint(0,n_competences,n_tasks)  
    # projet auquel fait référence une tache
    projet_referent = np.random.randint(0,n_projets,n_tasks)   

    # dataframe des taches :
    tasks = pd.DataFrame.from_dict({
    'id':list(range(n_tasks)),
    'duree':durations,
    'projet':projet_referent,
    'competence':competences
    })

    # GENERATION DE DISPONIBILITES UTILISATEURS :
    # en moyenne 36h, avec un ecart type de 6h
    max_capacity = np.round(np.random.normal(35,6,n_people))
    capacite_utilisateur = pd.DataFrame.from_dict({
        'disposable_time':max_capacity
    })
    capacite_utilisateur.index.set_names('id_user',inplace=True)

    # GENERATION D UNE MATRICE DE COMPETENCES :

    matrice_competence = np.zeros((n_competences,n_people))
    for i in range(n_people):
        proba = min(np.random.exponential(.20),1)
        matrice_competence[:,i] = np.random.binomial(3,proba,n_competences)
    matrice_competence = pd.DataFrame(matrice_competence,dtype=int)
    matrice_competence.index.set_names('competence',inplace=True)
    matrice_competence.columns.set_names('id_user',inplace=True)

    # GENERATION DUNE MATRICE PROJET IMPLIQUANT ALEATOIREMENT
    # DES PERSONNES DANS DES PROJETS
    matrice_projet = np.random.randint(0,2,(n_projets,n_people))
    matrice_projet = pd.DataFrame(matrice_projet,dtype=int)
    matrice_projet.index.set_names('projet',inplace=True)
    matrice_projet.columns.set_names('id_user',inplace=True)

    data = {'tasks':tasks,
    'capacite_utilisateur':capacite_utilisateur,
    "matrice_competence":matrice_competence,
    'matrice_projet':matrice_projet,
    'info_data':info_data}

    return data
