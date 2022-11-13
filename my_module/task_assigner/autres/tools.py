import numpy as np
import pandas as pd


def convert_to_arrays(
    matrice_competence: pd.DataFrame,
    matrice_projet: pd.DataFrame,
    capacite_utilisateur: pd.DataFrame,
):
    matrice_competence = matrice_competence.values
    matrice_projet = matrice_projet.values
    capacite_utilisateur = capacite_utilisateur.values.T[0]
    return matrice_competence, matrice_projet, capacite_utilisateur


def make_arcs_and_c(
    tasks: pd.DataFrame,
    matrice_competence: np.array,
    matrice_projet: np.array,
    curseur_politique: float,
):
    matrice_specialisation = compute_matrice_specialisaton(matrice_competence)
    matrice_compromis = (
        matrice_specialisation * curseur_politique
        + (1 - curseur_politique) * matrice_competence
    )

    arcs = []
    costs = []
    n_tasks = len(tasks)
    n_people = matrice_competence.shape[1]
    competences = tasks["competence"].values.astype(int)
    projet_referent = tasks["projet"].values.astype(int)

    for i in range(n_tasks):
        for j in range(n_people):
            if (
                matrice_competence[competences[i], j] > 0
                and matrice_projet[projet_referent[i], j] == 1
            ):  # si une personne est capacité de résoudre la tache (niveau compétence >= 1 et quelle est sur le projet )
                arcs.append(tuple((i, j)))  # elle pourra se voir assigner la tache

                # avec une utilité dépendant de la politique sélectionnée par l'utilisateur
                score = matrice_compromis[competences[i], j]
                costs.append(score)

    # Chaque tâche à également la possibilité de ne pas être assignée, ce qui est fortement pénalisé.
    for i in range(n_tasks):
        arcs.append(tuple((i, "not assigned")))
        costs.append(-100)

    costs += [0] * n_people  # slack variables
    costs = np.array(costs)

    return arcs, costs


def make_A_and_b(tasks: pd.DataFrame, arcs: list, capacite_utilisateur: np.array):
    n_arcs = len(arcs)
    n_people = len(capacite_utilisateur)
    n_tasks = len(tasks)
    # equality constraints :
    durations = tasks["duree"].values
    A = np.zeros((n_tasks + n_people, n_arcs + n_people))
    b = np.zeros(n_tasks + n_people)

    for i in range(n_tasks):
        for j in range(n_arcs):
            if arcs[j][0] == i:
                A[i, j] = 1
        b[i] = durations[i]

    # inequality contraints:
    for i in range(n_people):
        for j in range(n_arcs):
            if arcs[j][1] == i:
                A[i + n_tasks, j] = 1
        A[i + n_tasks, n_arcs + i] = 1  # slack variable
        b[i + n_tasks] = capacite_utilisateur[i]

    return A, b


def make_output_dataframe(solution: np.array, arcs: list):
    out = pd.DataFrame()
    for j in range(len(arcs)):
        if solution[j] > 0:
            arc = arcs[j]
            out = out.append(
                pd.DataFrame(
                    {
                        "ID Task": [arc[0]],
                        "ID User": [arc[1]],
                        "Durée (h)": [solution[j]],
                    }
                )
            )
    out.reset_index(drop=True, inplace=True)
    return out


def compute_matrice_specialisaton(matrice_competence: np.array):
    # la matrice spécialité permet de mettre en avant le fait que certaines personnes
    # savent réaliser un nombre limité de taches, tandis que d'autres seront
    matrice_competence = matrice_competence.astype(float)
    matrice_competence[:, matrice_competence.sum(axis=0) == 0] = np.nan
    res = matrice_competence / matrice_competence.sum(axis=0)
    res[res == np.nan] = 0
    return res
