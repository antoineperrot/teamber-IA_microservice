import numpy as np
import pandas as pd

def make_statistics(capacite_utilisateurs : np.array, solution:np.array, arcs:list):
    output = {'charge_utilisateurs':compute_charge_utilisateur(capacite_utilisateurs, solution, arcs),
        'total_heures_non_assignees':compute_heures_non_assignees(arcs, solution)
    }
    return output

def compute_charge_utilisateur(capacite_utilisateurs : np.array, solution:np.array, arcs:list):
    n_people = len(capacite_utilisateurs)
    charges_utilisateurs = np.zeros(n_people)
    for i in range(n_people):
        for j in range(len(arcs)):
            if arcs[j][1] == i :
                charges_utilisateurs[i] += solution[j]
    out_dict = {
        'user_id':list(range(len(capacite_utilisateurs))),
        'disposable_time_(h)':capacite_utilisateurs,
        'assigned_hours':charges_utilisateurs,
        'busy_time_percent':np.round(charges_utilisateurs/capacite_utilisateurs*100)
    }
    out = pd.DataFrame(out_dict).to_dict()
    return out

def compute_heures_non_assignees(arcs, solution):
    h_NA=0
    for j in range(len(arcs)):
        if arcs[j][1] =='not assigned' and solution[j] > 0 :
                h_NA += np.round(solution[j],2)
    return h_NA




