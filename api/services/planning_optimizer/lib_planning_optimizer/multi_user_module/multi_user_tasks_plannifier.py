import numpy as np
import pandas as pd


# TACHES MERE FILLE

# Planifie les tâches multi-utilisateurs à l'aide des 3 fonctions ci-dessus
def planifieTMF(TC, DATE_DEBUT, DATE_FIN, plannings, maxiter=100):
    N_utilisateurs = len(plannings)
    duree_sprint = pd.to_timedelta(
        pd.to_datetime(DATE_FIN) - pd.to_datetime(DATE_DEBUT)
    ) / np.timedelta64(1, "h")
    new_TC = pd.DataFrame.copy(TC)
    debut_MUT_ideal = (
        0  # int(new_TC['Priorité'].min() / T['Priorité'].max() * duree_sprint)
    )
    fin_MUT_ideal = duree_sprint  # int(new_TC['Priorité'].max() / T['Priorité'].max() * duree_sprint)
    Is = []
    d = []
    INDEX = []
    for index, row in new_TC.iterrows():
        duree = row["Durée"]

        a = plannings[row["id utilisateur"]].base["Temps écoulé"].values
        b = a + plannings[row["id utilisateur"]].base["Longueur"].values

        indexValides = np.where(b - (a + duree) >= 0)[0]
        if not len(indexValides) == 0:
            a = a[indexValides]
            b = b[indexValides] - duree
            d.append(duree)

            I = np.array([a, b]).T
            Is.append(I)
            INDEX.append(index)
        else:
            print(
                f'La tâche {row["Objet"]} ne rentre dans aucun créneau et ne sera pas planifiée.'
            )

    score_min = np.inf

    i = 0
    while i < maxiter:
        if i > 0.95 * maxiter and score_min / N_utilisateurs > 2:
            debut_MUT = debut_MUT_ideal + (i / maxiter) ** 3 * (0 - debut_MUT_ideal)
            fin_MUT = fin_MUT_ideal + (i / maxiter) ** 3 * (
                duree_sprint - fin_MUT_ideal
            )
        else:
            debut_MUT = debut_MUT_ideal
            fin_MUT = fin_MUT_ideal

        t = np.sort(np.random.randint(debut_MUT, fin_MUT, len(d))) / 1.0
        t = proj2(t, Is)
        t = proj1(t, d)

        if h(t, Is) < score_min:
            score_min = h(t, Is)
            tmin = t
            if score_min == 0:
                break
        i += 1
    print(
        "Non respect des horaires en heures pour la planification des tâches mere-fille :",
        score_min,
    )
    new_TC.loc[INDEX, "Date début"] = pd.to_datetime(DATE_DEBUT) + pd.to_timedelta(
        tmin, unit="h"
    )
    new_TC.loc[INDEX, "Date fin"] = new_TC.loc[INDEX, "Date début"] + pd.to_timedelta(
        new_TC["Durée"], unit="h"
    )
    new_TC.loc[INDEX, "Priorité"] = "TMF "
    return new_TC.loc[
        INDEX, ["Objet", "Priorité", "Date début", "Date fin", "id utilisateur"]
    ]


# (maths)
def proj1(t, d):
    n = len(t)
    proj = np.copy(t)
    for i in range(1, n):
        if proj[i] < proj[i - 1] + d[i - 1]:
            proj[i] = proj[i - 1] + d[i - 1]
    return proj


# (maths)
def proj2(t, Is):
    n = len(t)
    proj = np.copy(t)
    for i in range(n):
        if t[i] < 0:
            proj[i] = 0
        if t[i] > Is[i].max():
            proj[i] = Is[i].max()
        else:
            indexa = np.where(Is[i][:, 0] <= t[i])[0].max()
            indexb = np.where(t[i] <= Is[i][:, 1])[0].min()
            if indexa != indexb:
                x, y = np.where(np.abs(Is[i] - t[i]) == np.abs(Is[i] - t[i]).min())
                x = x[0]
                y = y[0]
                proj[i] = Is[i][x, y]
    return proj


# (maths)
def h(t, Is):
    n = len(t)
    proj = np.copy(t)
    penalty = 0
    for i in range(n):
        if t[i] < 0:
            penalty += np.abs(t[i])
        if t[i] > Is[i].max():
            penalty += np.abs(Is[i].max() - t[i])
        else:
            indexa = np.where(Is[i][:, 0] <= t[i])[0].max()
            indexb = np.where(t[i] <= Is[i][:, 1])[0].min()
            if indexa != indexb:
                penalty += np.abs(Is[i] - t[i]).min()

    return penalty
