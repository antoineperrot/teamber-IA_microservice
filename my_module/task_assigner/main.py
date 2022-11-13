def solve(
    df_prj,
    df_cmp,
    df_tsk,
    df_dsp,
    curseur,
    contrainte_etre_sur_projet,
    avantage_projet,
    data_generation=False,
):
    """Mettre data_generation=True pour générer des paire (donnees_entree, donnees_sorties) pour ensuite tester les fonctions."""
    # try:
    if True:
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
    try:
        pass
    except:
        raise HTTPException(
            status_code=500, detail="Le solveur a échoué à produire une solution."
        )
    return solution
