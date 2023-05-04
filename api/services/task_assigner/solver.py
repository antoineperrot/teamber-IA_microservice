"""
Module du solveur de task assigner
"""
import unittest
import numpy as np
import pandas as pd
from scipy.optimize import linprog

from api.loggers import logger_task_assigner
from api.services.task_assigner.lib_task_assigner.solution_statistics.statistics import (
    make_stat_cmp,
    make_stat_prj,
    make_stat_tsk,
    make_stat_utl,
)
from api.services.task_assigner.lib_task_assigner.tools.contrainte_projet import ContrainteEtreSurProjet
from api.services.task_assigner.lib_task_assigner.tools.id_remapping import (
    make_list_ids,
    make_mapping_dicts_extern_to_local,
    make_mapping_dicts_local_to_extern,
    add_local_ids_in_dfs,
    make_usefull_mapping_dicts,
    remap_df_out,
)
from api.services.task_assigner.lib_task_assigner.tools.matrix_maker import (
    make_mat_cmp,
    make_mat_prj,
    make_mat_spe,
)
from api.services.task_assigner.lib_task_assigner.tools.problem_formulation import (
    make_matrix_a_and_b,
    make_arcs_and_cost_func,
)
from api.string_keys import *


class SolverCrashException(Exception):
    """Exception à lever lorsque le solveur crash"""
    def __init__(self):
        self.msg = "Crash du solveur."

    def __repr__(self):
        return self.msg


def solveur_task_assigner(
    df_prj: pd.DataFrame,
    df_cmp: pd.DataFrame,
    df_tsk: pd.DataFrame,
    df_dsp: pd.DataFrame,
    curseur: float,
    contrainte_etre_sur_projet: ContrainteEtreSurProjet,
    avantage_projet: float,
) -> dict:
    """ Solveur de la fonctionnalité de task assigner """
    logger_task_assigner.info("Lancement du solveur")

    logger_task_assigner.debug("FAIT LA LISTE DE TOUS LES IDS (PRJ, CMP, TSK, UTL) CONTENUS DANS LES DONNEES RECUES")
    id_utl, id_prj, id_cmp, id_tsk = make_list_ids(df_prj=df_prj,
                                                   df_cmp=df_cmp,
                                                   df_tsk=df_tsk,
                                                   df_dsp=df_dsp)

    logger_task_assigner.debug("CONVERSION DES IDS Wandeed en Identifiant local")
    (
        mapping_utl_to_int,
        mapping_prj_to_int,
        mapping_cmp_to_int,
        mapping_tsk_to_int,
    ) = make_mapping_dicts_extern_to_local(id_utl=id_utl,
                                           id_prj=id_prj,
                                           id_cmp=id_cmp,
                                           id_tsk=id_tsk)

    logger_task_assigner.debug("CONVERSION DES Identifiant local en IDS Wandeed")
    (
        mapping_int_to_utl,
        mapping_int_to_prj,
        mapping_int_to_cmp,
        mapping_int_to_tsk,
    ) = make_mapping_dicts_local_to_extern(id_utl=id_utl,
                                           id_prj=id_prj,
                                           id_cmp=id_cmp,
                                           id_tsk=id_tsk)

    logger_task_assigner.debug("Comptage nombre cmp, utl, tsk, prj.")
    n_utl = len(id_utl)
    n_prj = len(id_prj)
    n_cmp = len(id_cmp)
    n_tsk = len(id_tsk)

    logger_task_assigner.debug("AJOUT DES VARIABLES LOCALES DANS LES DATAFRAMES")
    df_rmd_prj, df_rmd_cmp, df_rmd_tsk, df_rmd_dsp = add_local_ids_in_dfs(
        df_prj,
        df_cmp,
        df_tsk,
        df_dsp,
        mapping_cmp_to_int=mapping_cmp_to_int,
        mapping_utl_to_int=mapping_utl_to_int,
        mapping_tsk_to_int=mapping_tsk_to_int,
        mapping_prj_to_int=mapping_prj_to_int,
    )

    logger_task_assigner.debug("FABRICATION MATRICE PROJET")
    mat_prj = make_mat_prj(df_prj=df_rmd_prj,
                           n_prj=n_prj,
                           n_utl=n_utl)

    logger_task_assigner.debug("FABRICATION MATRICE COMPETENCE")
    mat_cmp = make_mat_cmp(df_cmp=df_rmd_cmp,
                           n_cmp=n_cmp,
                           n_utl=n_utl)

    logger_task_assigner.debug("FABRICATION MATRICE SPECIALISATION")
    mat_spe = make_mat_spe(mat_cmp=mat_cmp)

    logger_task_assigner.debug("FABRICATION MATRICE COMPROMIS COMPETENCE <--> SPECIALISATION")
    mat_cpr = (1 - curseur) * mat_cmp + curseur * mat_spe

    logger_task_assigner.debug("FABRICATION DE DICTIONNAIRE UTILES PAR LA SUITE")
    (
        mapping_tsk_to_cmp,
        mapping_tsk_to_prj,
        mapping_tsk_to_lgt,
        mapping_utl_to_dsp,
    ) = make_usefull_mapping_dicts(df_tsk=df_rmd_tsk,
                                   df_dsp=df_rmd_dsp)

    logger_task_assigner.debug("FABRICATION DES ARCS RELIANT TACHES A"
                               " UTILISATEURS POTENTIELS, AINSI QUE FONCTION DE COUT")
    arcs, cost_func, n_arcs = make_arcs_and_cost_func(
        n_tsk=n_tsk,
        n_utl=n_utl,
        mapping_tsk_to_cmp=mapping_tsk_to_cmp,
        mapping_tsk_to_prj=mapping_tsk_to_prj,
        mat_cmp=mat_cmp,
        mat_prj=mat_prj,
        mat_cpr=mat_cpr,
        contrainte_etre_sur_projet=contrainte_etre_sur_projet,
        avantage_projet=avantage_projet,
    )

    logger_task_assigner.debug("FABRICATION DES MATRICES A et B POUR RESOUDRE AX<=B")
    matrix_a, b = make_matrix_a_and_b(n_tsk=n_tsk,
                                      n_utl=n_utl,
                                      n_arcs=n_arcs,
                                      mapping_tsk_to_lgt=mapping_tsk_to_lgt,
                                      mapping_utl_to_dsp=mapping_utl_to_dsp,
                                      arcs=arcs)

    logger_task_assigner.debug("RESOLUTION DU PROBLEME DE PROGRAMMATION LINEAIRE")
    solution_vector, outcome, method = solve_linear_programation_problem(
        matrix_a=matrix_a,
        b=b,
        cost_func=cost_func
    )
    # vérif validité solution :
    test = unittest.TestCase()
    #test.assertLessEqual(solution_vector[:-n_tsk].sum(), df_dsp[key_user_dispo].sum())
    test.assertAlmostEqual(solution_vector[:n_arcs].sum(), df_tsk[key_duree_evenement].sum())

    logger_task_assigner.debug("MISE EN FORME DE LA SOLUTION DANS UN DATAFRAME PANDAS")
    df_out = make_output_dataframe(
        solution_vector=solution_vector,
        arcs=arcs,
        cost_func=cost_func,
        mapping_tsk_to_lgt=mapping_tsk_to_lgt,
        mapping_tsk_to_cmp=mapping_tsk_to_cmp,
        mapping_tsk_to_prj=mapping_tsk_to_prj,
        mapping_utl_to_dsp=mapping_utl_to_dsp,
        avantage_projet=avantage_projet,
        contrainte_etre_sur_projet=contrainte_etre_sur_projet
    )

    logger_task_assigner.debug("REMAPPING DES ID LOCAUX EN ID WANDEED")
    df_rmd_out = remap_df_out(
        df_out=df_out,
        mapping_int_to_tsk=mapping_int_to_tsk,
        mapping_int_to_utl=mapping_int_to_utl,
        mapping_int_to_prj=mapping_int_to_prj,
        mapping_int_to_cmp=mapping_int_to_cmp
    )

    logger_task_assigner.debug("Production de statistiques par compétences")
    stat_cmp = make_stat_cmp(df_out=df_rmd_out)

    logger_task_assigner.debug("Production de statistiques par utilisateur")
    stat_utl = make_stat_utl(df_out=df_rmd_out,
                             mapping_utl_to_dsp=mapping_utl_to_dsp,
                             mapping_utl_to_int=mapping_utl_to_int)

    logger_task_assigner.debug("Production de statistiques par tachez")
    stat_tsk = make_stat_tsk(df_out=df_rmd_out,
                             mapping_tsk_to_lgt=mapping_tsk_to_lgt,
                             mapping_int_to_tsk=mapping_int_to_tsk)

    logger_task_assigner.debug("Production de statistiques par projet")
    stat_prj = make_stat_prj(df_out=df_rmd_out)

    logger_task_assigner.debug("SORTIE API")
    solution = {
        "solution_brute": df_rmd_out.to_dict(),
        "statistics": {
            "cmp": stat_cmp.to_dict(),
            "utl": stat_utl.to_dict(),
            "tsk": stat_tsk.to_dict(),
            "prj": stat_prj.to_dict(),
        },
    }

    return solution


def solve_linear_programation_problem(
    matrix_a: np.ndarray, b: np.ndarray, cost_func: np.ndarray
) -> tuple[np.ndarray, str, str]:
    """
    RESOLUTION DU PROBLEME DE PROGRAMMATION LINEAIRE
    """
    method = "simplex"
    linprog_solver = linprog(
        -cost_func, A_eq=matrix_a, b_eq=b, method="simplex", options={"maxiter": 10000}
    )
    if linprog_solver.status != 0:
        logger_task_assigner.warning("resolution problème linéaire: échec de la résolution par la méthode du simplexe."
                                     f" Message: {linprog_solver.message}")
        linprog_solver = linprog(
            -cost_func,
            A_eq=matrix_a,
            b_eq=b,
            method="interior-point",
            options={"maxiter": 10000},
        )
        if linprog_solver.status != 0:
            logger_task_assigner.warning(
                "resolution problème linéaire: échec de la résolution par la méthode des points intérieurs."
                f" Message: {linprog_solver.message}")

            raise NoSolutionFoundException(msg=linprog_solver.message)
        outcome = linprog_solver.message
        method = "interior-point"
    else:
        outcome = linprog_solver.message

    solution_vector = linprog_solver.x
    return solution_vector, outcome, method


class NoSolutionFoundException(Exception):
    """Exception à lever lorsque le solveur scipy ne trouve pas de solution au problème"""
    def __init__(self, msg: str):
        self.msg = f"Le solveur n'a pas pu déterminer de solution. Message du solveur: {msg}"

    def __repr__(self):
        return self.msg


def make_output_dataframe(
    solution_vector: np.ndarray,
    arcs: list[tuple],
    cost_func: np.ndarray,
    mapping_tsk_to_lgt: dict,
    mapping_tsk_to_cmp: dict,
    mapping_tsk_to_prj: dict,
    mapping_utl_to_dsp: dict,
    avantage_projet: float,
    contrainte_etre_sur_projet: ContrainteEtreSurProjet
) -> pd.DataFrame:
    """
    MET EN FORME LA SOLUTION DANS UN DATAFRAME PANDAS
    """
    out = pd.DataFrame()
    for j in range(len(arcs)):
        if solution_vector[j] > 0:
            tsk, utl = arcs[j]

            lvl = cost_func[j]
            if lvl > 0 and contrainte_etre_sur_projet == ContrainteEtreSurProjet.DE_PREFERENCE:
                lvl -= avantage_projet
            out = pd.concat(
                [
                    out,
                    pd.DataFrame(
                        {
                            "prj": [mapping_tsk_to_prj[tsk]],
                            "tsk": [tsk],
                            "utl": [utl],
                            "duree_assignee": [solution_vector[j]],
                            "tsk_lgt": [mapping_tsk_to_lgt[tsk]],
                            "duree_non_assignee": [
                                mapping_tsk_to_lgt[tsk] - solution_vector[j]
                            ],
                            "dsp_utl": [mapping_utl_to_dsp[utl]],
                            "cmp": [mapping_tsk_to_cmp[tsk]],
                            "lvl": [lvl],
                        }
                    ),
                ]
            )

    out.loc[out["utl"] == "not assigned", "lvl"] = None
    out.sort_values(by=["prj", "tsk", "utl"], inplace=True)
    out.reset_index(drop=True, inplace=True)
    return out
