import numpy as np

# CALCULS DE POTENTIELS : un potentiel


# Calcule le pourcentage de temps perdu sur les plages horaires utilisées
def V_TempsPerdu(taches, base_planning_array):
    temps_perdu = 0

    temps_total_dispo = 0

    index_creneau, index_tache = 0,0
    
    creneaux = base_planning_array[1,:]
    durees = taches[1,:]
    
    taches_traitees, creneaux_taches = [], []
    
    nb_taches, nb_creneaux = taches.shape[1], base_planning_array.shape[1]
    
    while index_tache < nb_taches and index_creneau < nb_creneaux:
        current_filled = 0
        j = index_tache
        filled = False
        temps_total_dispo  += creneaux[index_creneau] 
        while j < nb_taches and not filled :
            if durees[j] + current_filled <= creneaux[index_creneau] :
                taches_traitees.append(taches[0,j])
                creneaux_taches.append(base_planning_array[0,index_creneau])    
                current_filled += durees[j]                
                j += 1
            else :
                filled = True

        index_tache = j

        
        temps_total_dispo  += creneaux[index_creneau]
        temps_perdu  += max(creneaux[index_creneau] - current_filled, 0)
        index_creneau += 1
        
    chronologie = np.array([taches_traitees,creneaux_taches])

    prop_temps_perdu   = temps_perdu / temps_total_dispo        #proportion de temps perdu par rapport au temps total dispo
    
    return prop_temps_perdu, chronologie
    
# Calcule un potentiel correspondant au non respect des priorités
def V_Priorites(taches):
    prio = taches[2,:]
    target = np.sort(prio)
    
    return np.linalg.norm(target - prio, ord= 1) / len(np.unique(prio)) / len(prio) #(prio != target).sum()/len(prio)
    

# Calcule un potentiel correspondant au taux de dispersion moyen de chaque tâche
def V_Dispersion(taches):
    taches = taches[3,:]
    list_taches = np.unique(taches)
    pen = 0
    c = 0
    for t in list_taches :
        indexs = np.where(taches == t)[0]
        if len(indexs) > 1 :
            c+=1
            pen_local = 0
            for i in range(len(indexs) -1):
                if indexs[i+1] > indexs[i] + 1:
                    pen_local += 1
            pen_local /= len(indexs)
            pen += pen_local
    return pen/c if c > 0 else 0

