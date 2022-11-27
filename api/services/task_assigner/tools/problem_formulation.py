from typing import Tuple, List
import numpy as np
from modules.task_assigner.tools.contrainte_projet import ContrainteEtreSurProjet


def make_arcs_and_cost_func(
    n_tsk: int,
    n_utl: int,
    d_tsk_to_cmp: dict,
    d_tsk_to_prj: dict,
    mat_cmp: np.ndarray,
    mat_prj: np.ndarray,
    mat_cpr: np.ndarray,
    contrainte_etre_sur_projet: ContrainteEtreSurProjet,
    avantage_projet: float,
    penalty=-100,
) -> Tuple[List[tuple], np.ndarray, int]:
    """
    FABRICATION DES ARCS RELIANT TACHES A UTILISATEURS POTENTIELS, AINSI QUE FONCTION DE COUT
    """
    arcs = []
    cost_func = []
    for tsk in range(n_tsk):
        for utl in range(n_utl):
            cmp = d_tsk_to_cmp[tsk]
            prj = d_tsk_to_prj[tsk]
            lvl = mat_cmp[cmp, utl]
            score_cpr = mat_cpr[cmp, utl]  # score compromis
            utl_on_prj = mat_prj[prj, utl]
            if lvl >= 0:
                if (
                    contrainte_etre_sur_projet == ContrainteEtreSurProjet.OUI
                    and utl_on_prj
                ):
                    arcs.append(tuple((tsk, utl)))
                    cost_func.append(score_cpr)
                elif contrainte_etre_sur_projet == ContrainteEtreSurProjet.NON:
                    arcs.append(tuple((tsk, utl)))
                    cost_func.append(score_cpr)
                elif (
                    contrainte_etre_sur_projet == ContrainteEtreSurProjet.DE_PREFERENCE
                ):
                    arcs.append(tuple((tsk, utl)))
                    cost_func.append(score_cpr + avantage_projet)

    # chaque tache a également la possibilité de ne pas être assignée, ce qui est fortement pénalisé
    for tsk in range(n_tsk):
        arcs.append(tuple((tsk, "not assigned")))
        cost_func.append(penalty)

    # ajout des variables df'écart (slack variables)
    cost_func += [0] * n_utl
    cost_func = np.array(cost_func)
    n_arcs = len(arcs)
    return arcs, cost_func, n_arcs


def make_A_and_b(
    n_tsk: int,
    n_utl: int,
    n_arcs: int,
    d_tsk_to_lgt: dict,
    d_utl_to_dsp: dict,
    arcs: List[tuple],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    FABRICATION DES MATRICES A et B POUR RESOUDRE AX<=B
    """

    # equality constraints :
    A = np.zeros((n_tsk + n_utl, n_arcs + n_utl))
    b = np.zeros(n_tsk + n_utl)

    # contrainte d'égalité : distribution de toutes les heures
    for tsk in range(n_tsk):
        for idx_arc, arc in enumerate(arcs):
            if arc[0] == tsk:
                A[tsk, idx_arc] = 1
        b[tsk] = d_tsk_to_lgt[tsk]

    # contraintes d'inégalités : respect des disponibilités de travail
    for utl in range(n_utl):
        for j in range(n_arcs - n_tsk):
            arc = arcs[j]
            utl_2 = arc[1]
            if utl_2 == utl:
                A[n_tsk + utl, j] = 1
        A[n_tsk + utl, n_arcs + utl] = 1  # variable d'écart (slack variable)
        b[n_tsk + utl] = d_utl_to_dsp[utl]

    return A, b
