from my_module.task_assigner.tools.id_remapping import make_list_ids, make_mapping_dicts_extern_to_local,\
                                                        make_mapping_dicts_local_to_extern, add_local_ids_in_dfs,\
                                                            make_usefull_mapping_dicts, remap_df_out
from my_module.task_assigner.tools.matrix_maker import make_mat_cmp, make_mat_prj, make_mat_spe
from my_module.task_assigner.tools.problem_formulation import make_A_and_b, make_arcs_and_cost_func
from my_module.task_assigner.solution_statistics.statistics import make_stat_cmp, make_stat_prj, make_stat_tsk, make_stat_utl

from typing import Tuple, List
import pandas as pd
import numpy as np
from scipy.optimize import linprog
from fastapi import HTTPException


def solveur(
    df_prj: pd.DataFrame,
    df_cmp: pd.DataFrame,
    df_tsk: pd.DataFrame,
    df_dsp: pd.DataFrame,
    curseur: float,
    contrainte_etre_sur_projet: bool,
    avantage_projet: float,
    data_generation=False,
):
    """
    Mettre data_generation=True pour générer des paire (donnees_entree, donnees_sorties) pour ensuite tester les fonctions.
    """
    try:
        # FAIT LA LISTE DE TOUS LES IDS (PRJ, CMP, TSK, UTL) CONTENUS DANS LES DONNEES RECUES
        id_utl, id_prj, id_cmp, id_tsk = make_list_ids(df_prj, df_cmp, df_tsk, df_dsp)

        # CONVERSION DES IDS Wandeed en Identifiant local
        (
            utl_to_int,
            prj_to_int,
            cmp_to_int,
            tsk_to_int,
        ) = make_mapping_dicts_extern_to_local(id_utl, id_prj, id_cmp, id_tsk)

        # CONVERSION DES Identifiant local en IDS Wandeed
        (
            int_to_utl,
            int_to_prj,
            int_to_cmp,
            int_to_tsk,
        ) = make_mapping_dicts_local_to_extern(id_utl, id_prj, id_cmp, id_tsk)

        # Comptage nombre cmp, utl, tsk, prj.
        n_utl = len(id_utl)
        n_prj = len(id_prj)
        n_cmp = len(id_cmp)
        n_tsk = len(id_tsk)

        # AJOUT DES VARIABLES LOCALES DANS LES DATAFRAMES
        df_rmd_prj, df_rmd_cmp, df_rmd_tsk, df_rmd_dsp = add_local_ids_in_dfs(
            df_prj,
            df_cmp,
            df_tsk,
            df_dsp,
            cmp_to_int,
            utl_to_int,
            tsk_to_int,
            prj_to_int,
        )

        # FABRICATION MATRICE PROJET
        mat_prj = make_mat_prj(df_rmd_prj, n_prj, n_utl)

        # FABRICATION MATRICE COMPETENCE
        mat_cmp = make_mat_cmp(df_rmd_cmp, n_cmp, n_utl)

        # FABRICATION MATRICE COMPETENCE
        mat_spe = make_mat_spe(mat_cmp)

        # FABRICATION MATRICE COMPROMIS COMPETENCE <--> SPECIALISATION
        mat_cpr = (1 - curseur) * mat_cmp + curseur * mat_spe

        # FABRICATION DE DICTIONNAIRE UTILES PAR LA SUITE
        (
            d_tsk_to_cmp,
            d_tsk_to_prj,
            d_tsk_to_lgt,
            d_utl_to_dsp,
        ) = make_usefull_mapping_dicts(df_rmd_tsk, df_rmd_dsp)

        # FABRICATION DES ARCS RELIANT TACHES A UTILISATEURS POTENTIELS, AINSI QUE FONCTION DE COUT
        arcs, cost_func, n_arcs = make_arcs_and_cost_func(
            n_tsk,
            n_utl,
            d_tsk_to_cmp,
            d_tsk_to_prj,
            mat_cmp,
            mat_prj,
            mat_cpr,
            contrainte_etre_sur_projet,
            avantage_projet,
        )

        # FABRICATION DES MATRICES A et B POUR RESOUDRE AX<=B
        A, b = make_A_and_b(n_tsk, n_utl, n_arcs, d_tsk_to_lgt, d_utl_to_dsp, arcs)

        # RESOLUTION DU PROBLEME DE PROGRAMMATION LINEAIRE
        solution_vector, outcome, method = solve_linear_programmation_problem(
            A, b, cost_func
        )

        # MISE EN FORME DE LA SOLUTION DANS UN DATAFRAME PANDAS
        df_out = make_output_dataframe(
            solution_vector,
            arcs,
            cost_func,
            d_tsk_to_lgt,
            d_tsk_to_cmp,
            d_tsk_to_prj,
            d_utl_to_dsp,
        )

        # REMAPPING DES ID LOCAUX EN ID WANDEED
        df_rmd_out = remap_df_out(
            df_out, int_to_tsk, int_to_utl, int_to_prj, int_to_cmp
        )

        # Production de statistiques par compétences
        stat_cmp = make_stat_cmp(df_rmd_out)

        # Production de statistiques par utilisateur
        stat_utl = make_stat_utl(df_rmd_out, d_utl_to_dsp, utl_to_int)

        # Production de statistiques par tachez
        stat_tsk = make_stat_tsk(df_rmd_out, d_tsk_to_lgt, int_to_tsk)

        # Production de statistiques par projet
        stat_prj = make_stat_prj(df_rmd_out)

        # SORTIE API
        solution = {
            "solution_brute": df_rmd_out.to_dict(),
            "statistics": {
                "cmp": stat_cmp.to_dict(),
                "utl": stat_utl.to_dict(),
                "tsk": stat_tsk.to_dict(),
                "prj": stat_prj.to_dict(),
            },
        }
    except:
        raise HTTPException(
            status_code=500, detail="Le solveur a échoué à produire une solution."
        )
    return solution


def solve_linear_programmation_problem(A: np.ndarray,
                                       b: np.ndarray,
                                       cost_func: np.ndarray)\
        -> Tuple[np.ndarray, str, str]:
    """
    RESOLUTION DU PROBLEME DE PROGRAMMATION LINEAIRE
    """
    method = "simplex"
    l = linprog(
        -cost_func, A_eq=A, b_eq=b, method="simplex", options={"maxiter": 10000}
    )
    if l.status != 0:
        l = linprog(
            -cost_func,
            A_eq=A,
            b_eq=b,
            method="interior-point",
            options={"maxiter": 10000},
        )
        outcome = l.message
        method = "interior-point"
    else:
        outcome = l.message

    solution_vector = l.x
    return solution_vector, outcome, method


def make_output_dataframe(
    solution_vector: np.ndarray,
    arcs: List[tuple],
    cost_func: np.ndarray,
    d_tsk_to_lgt: dict,
    d_tsk_to_cmp: dict,
    d_tsk_to_prj: dict,
    d_utl_to_dsp: dict,
) -> pd.DataFrame:
    """
    MET EN FORME LA SOLUTION DANS UN DATAFRAME PANDAS
    """
    out = pd.DataFrame()
    for j in range(len(arcs)):
        if solution_vector[j] > 0:
            tsk, utl = arcs[j]
            lvl = cost_func[j]
            out = out.append(
                pd.DataFrame(
                    {
                        "prj": [d_tsk_to_prj[tsk]],
                        "tsk": [tsk],
                        "utl": [utl],
                        "duree_assignee": [solution_vector[j]],
                        "tsk_lgt": [d_tsk_to_lgt[tsk]],
                        "duree_non_assignee": [d_tsk_to_lgt[tsk] - solution_vector[j]],
                        "dsp_utl": [d_utl_to_dsp[utl]],
                        "cmp": [d_tsk_to_cmp[tsk]],
                        "lvl": [lvl],
                    }
                )
            )

    out.loc[out["utl"] == "not assigned", "lvl"] = None
    out.sort_values(by=["prj", "tsk", "utl"], inplace=True)
    out.reset_index(drop=True, inplace=True)
    return out

