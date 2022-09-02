from scipy.optimize import linprog
from .tools import *
from .solution_interpreter import *
import pandas as pd

def solve_problem(tasks:pd.DataFrame, capacite_utilisateur:pd.DataFrame, matrice_competence:pd.DataFrame, matrice_projet:pd.DataFrame, curseur_politique:float = 1.0):
    # mettre ici un check de la validité des données. si succès, continuer.
    
    matrice_competence, matrice_projet, capacite_utilisateur = convert_to_arrays(matrice_competence, matrice_projet, capacite_utilisateur)

    arcs, c = make_arcs_and_c(tasks, matrice_competence, matrice_projet, curseur_politique)

    A, b = make_A_and_b(tasks, arcs, capacite_utilisateur)


    l = linprog(-c,A_eq=A,b_eq=b,method="simplex",options={'maxiter':1500})
    if l.status !=0 :
        l = linprog(-c, A_eq=A,b_eq=b,method='interior-point',options={'maxiter':1500})
        if l.status != 0:
            outcome = 'The system has no solution'
        else :
            outcome = 'success'
    else :
        outcome = 'success'
    
    solution = l.x
    output = {'solution':make_output_dataframe(solution, arcs).to_dict(),
    'statistics':make_statistics(capacite_utilisateur, solution, arcs)}
        
    return output

    

