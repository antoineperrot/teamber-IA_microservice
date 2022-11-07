# from my_module.task_assigner import *
import pickle
import os
from .task_assigner import *


import pandas as pd
import numpy as np


class step:
    def __init__(self, x: tuple, y: tuple, func: object, test_nature="standard"):
        self.x = x
        self.y = y
        self.cmd = (
            "from " + func.__module__ + " import " + func.__name__ + " as func_to_test"
        )
        self.module = func.__module__
        self.name = func.__name__
        self.complete_name = self.module + "." + self.name

    def fx(self):
        try:
            exec(self.cmd, globals())
        except:
            raise ImportError(self.cmd)

        try:
            fx = func_to_test(*self.x)
        except:
            raise AssertionError(
                f"{self.complete_name} n'a pas pu être appliquée aux données synthétiques."
            )

        if not isinstance(fx, tuple):
            fx = [fx]

        return fx

    def test(self):
        print("Testing:", self.complete_name)
        fx = self.fx()
        if len(fx) != len(self.y):
            raise AssertionError(
                f"Le nombre de variables en sortie de {self.complete_name} a changé. Attendu : {len(self.y)}, Obtenu : {len(fx)}"
            )
        for output, expected_output in zip(fx, self.y):
            if (
                isinstance(expected_output, dict)
                or isinstance(expected_output, list)
                or isinstance(expected_output, int)
                or isinstance(expected_output, str)
            ):
                assert (
                    output == expected_output
                ), f"{self.complete_name} ne reproduit plus les résultats attendus."
            elif isinstance(expected_output, pd.core.frame.DataFrame):
                assert all(
                    output == expected_output
                ), f"{self.complete_name} ne reproduit plus les résultats attendus."
            elif isinstance(expected_output, np.ndarray):
                assert (
                    output == expected_output
                ).all(), (
                    f"{self.complete_name} ne reproduit plus les résultats attendus."
                )
            else:
                raise AssertionError("Une variable n'a pas pu être testée.")


class Exp:
    def __init__(self, list_of_steps):
        self.steps = list_of_steps

    def test(self):
        for step in self.steps:
            step.test()


def test_task_assigner_on_synthetic_data(
    path_synthetic_data_test="my_module/task_assigner/synthetic_data_for_testing/",
):
    for i, file in enumerate(os.listdir(path_synthetic_data_test)):
        exp = pickle.load(open(path_synthetic_data_test + file, "rb"))
        print(
            "\n"
            + "#" * 30
            + f" TEST DATASET {i+1}/{len(os.listdir(path_synthetic_data_test))} "
            + "#" * 30
        )
        exp.test()
        print("\n")


def generate_synthetic_testing_data_task_assigner(
    n_exp=10, path_synthetic_data_test="task_assigner/synthetic_data_for_testing/"
):
    """
    Génère des expériences à partir de données aléatoires qui seront ensuite à reproduire par les tests.
    :n_exp: integer = 10, nombre d'expériences à créer.
    
    """
    data = mock_coherent_data()
    df_prj, df_cmp, df_tsk, df_dsp = data
    parameters = mock_random_parameters()
    curseur, contrainte_etre_sur_projet, avantage_projet = parameters

    ## CLEANING FOLDER before adding experiences
    for file in os.listdir(path_synthetic_data_test):
        os.remove(path_synthetic_data_test + file)

    for i in range(n_exp):
        steps = []

        # FAIT LA LISTE DE TOUS LES IDS (PRJ, CMP, TSK, UTL) CONTENUS DANS LES DONNEES RECUES
        id_utl, id_prj, id_cmp, id_tsk = make_list_ids(df_prj, df_cmp, df_tsk, df_dsp)

        steps.append(
            step(
                (df_prj, df_cmp, df_tsk, df_dsp),
                (id_utl, id_prj, id_cmp, id_tsk),
                make_list_ids,
            )
        )

        # CONVERSION DES IDS Wandeed en Identifiant local
        (
            utl_to_int,
            prj_to_int,
            cmp_to_int,
            tsk_to_int,
        ) = make_mapping_dicts_extern_to_local(id_utl, id_prj, id_cmp, id_tsk)

        steps.append(
            step(
                (id_utl, id_prj, id_cmp, id_tsk),
                (utl_to_int, prj_to_int, cmp_to_int, tsk_to_int),
                make_mapping_dicts_extern_to_local,
            )
        )

        # CONVERSION DES Identifiant local en IDS Wandeed
        (
            int_to_utl,
            int_to_prj,
            int_to_cmp,
            int_to_tsk,
        ) = make_mapping_dicts_local_to_extern(id_utl, id_prj, id_cmp, id_tsk)

        steps.append(
            step(
                (id_utl, id_prj, id_cmp, id_tsk),
                (int_to_utl, int_to_prj, int_to_cmp, int_to_tsk),
                make_mapping_dicts_local_to_extern,
            )
        )

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

        steps.append(
            step(
                (
                    df_prj,
                    df_cmp,
                    df_tsk,
                    df_dsp,
                    cmp_to_int,
                    utl_to_int,
                    tsk_to_int,
                    prj_to_int,
                ),
                (df_rmd_prj, df_rmd_cmp, df_rmd_tsk, df_rmd_dsp),
                add_local_ids_in_dfs,
            )
        )

        # FABRICATION MATRICE PROJET
        mat_prj = make_mat_prj(df_rmd_prj, n_prj, n_utl)

        steps.append(step((df_rmd_prj, n_prj, n_utl), (mat_prj,), make_mat_prj))

        # FABRICATION MATRICE COMPETENCE
        mat_cmp = make_mat_cmp(df_rmd_cmp, n_cmp, n_utl)

        steps.append(step((df_rmd_cmp, n_cmp, n_utl), (mat_cmp,), make_mat_cmp))

        # FABRICATION MATRICE COMPETENCE
        mat_spe = make_mat_spe(mat_cmp)

        steps.append(step((mat_cmp,), (mat_spe,), make_mat_spe))

        # FABRICATION MATRICE COMPROMIS COMPETENCE <--> SPECIALISATION
        mat_cpr = (1 - curseur) * mat_cmp + curseur * mat_spe

        # FABRICATION DE DICTIONNAIRE UTILES PAR LA SUITE
        (
            d_tsk_to_cmp,
            d_tsk_to_prj,
            d_tsk_to_lgt,
            d_utl_to_dsp,
        ) = make_usefull_mapping_dicts(df_rmd_tsk, df_rmd_dsp)

        steps.append(
            step(
                (df_rmd_tsk, df_rmd_dsp,),
                (d_tsk_to_cmp, d_tsk_to_prj, d_tsk_to_lgt, d_utl_to_dsp,),
                make_usefull_mapping_dicts,
            )
        )

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

        steps.append(
            step(
                (
                    n_tsk,
                    n_utl,
                    d_tsk_to_cmp,
                    d_tsk_to_prj,
                    mat_cmp,
                    mat_prj,
                    mat_cpr,
                    contrainte_etre_sur_projet,
                    avantage_projet,
                ),
                (arcs, cost_func, n_arcs,),
                make_arcs_and_cost_func,
            )
        )

        # FABRICATION DES MATRICES A et B POUR RESOUDRE AX<=B
        A, b = make_A_and_b(n_tsk, n_utl, n_arcs, d_tsk_to_lgt, d_utl_to_dsp, arcs)

        steps.append(
            step(
                (n_tsk, n_utl, n_arcs, d_tsk_to_lgt, d_utl_to_dsp, arcs,),
                (A, b,),
                make_A_and_b,
            )
        )

        # RESOLUTION DU PROBLEME DE PROGRAMMATION LINEAIRE
        solution_vector, outcome, method = solve_linear_programmation_problem(
            A, b, cost_func
        )

        steps.append(
            step(
                (A, b, cost_func),
                (solution_vector, outcome, method,),
                solve_linear_programmation_problem,
            )
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

        steps.append(
            step(
                (
                    solution_vector,
                    arcs,
                    cost_func,
                    d_tsk_to_lgt,
                    d_tsk_to_cmp,
                    d_tsk_to_prj,
                    d_utl_to_dsp,
                ),
                (df_out,),
                make_output_dataframe,
            )
        )

        # REMAPPING DES ID LOCAUX EN ID WANDEED
        df_rmd_out = remap_df_out(
            df_out, int_to_tsk, int_to_utl, int_to_prj, int_to_cmp
        )

        steps.append(
            step(
                (df_out, int_to_tsk, int_to_utl, int_to_prj, int_to_cmp),
                (df_rmd_out,),
                remap_df_out,
            )
        )

        # Production de statistiques par compétences
        stat_cmp = make_stat_cmp(df_rmd_out)

        steps.append(step((df_rmd_out,), (stat_cmp,), make_stat_cmp))

        # Production de statistiques par utilisateur
        stat_utl = make_stat_utl(df_rmd_out, d_utl_to_dsp, utl_to_int)

        steps.append(
            step((df_rmd_out, d_utl_to_dsp, utl_to_int,), (stat_utl,), make_stat_utl)
        )

        # Production de statistiques par tache
        stat_tsk = make_stat_tsk(df_rmd_out, d_tsk_to_lgt, int_to_tsk)

        steps.append(
            step((df_rmd_out, d_tsk_to_lgt, int_to_tsk,), (stat_tsk,), make_stat_tsk)
        )

        # Production de statistiques par projet
        stat_prj = make_stat_prj(df_rmd_out)

        steps.append(step((df_rmd_out,), (stat_prj,), make_stat_prj))

        exp = Exp(steps)

        pickle.dump(exp, open(path_synthetic_data_test + f"exp_{i}", "wb"))
