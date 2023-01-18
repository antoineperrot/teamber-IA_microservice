"""
Fonctions pour générer des données aléatoires.
"""
from random import choices

import numpy as np
import pandas as pd

from api.string_keys import *
from api.services.task_assigner.lib_task_assigner.tools import ContrainteEtreSurProjet


def generate_unique_ids(n: int) -> list[int]:
    """
    Génère des listes aléatoires d'id
    """
    ids = []
    for i in range(n):
        rdm_id = np.random.randint(1000, 10000)
        while rdm_id in ids:
            rdm_id = np.random.randint(10, 1000)
        ids.append(rdm_id)
    ids = np.sort(ids)
    return ids


def mock_coherent_data() -> tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame
]:
    """
    Génère des configurations aléatoires et cohérentes de tailles d'entreprise, nombre de projets, n de cmp, n de tsk.
    """
    p = 0.7
    nn = np.random.randint(7, 70)
    n_prj = np.random.binomial(nn * 0.3, p)
    n_utl = np.random.binomial(nn, p)
    n_tsk = 2 + np.random.binomial(nn * 3, p)
    n_cmp = np.random.binomial(nn * 0.4, p)

    # genere des ids unique pour chaque variable
    ids_utl = generate_unique_ids(n_utl)
    ids_cmp = generate_unique_ids(n_cmp)
    ids_tsk = generate_unique_ids(n_tsk)
    ids_prj = generate_unique_ids(n_prj)

    mat_cmp = np.zeros((n_cmp, n_utl))
    for i in range(n_utl):
        proba = min(np.random.exponential(0.20), 1)
        mat_cmp[:, i] = np.random.binomial(3, proba, n_cmp)

    df_cmp = pd.DataFrame(
        {key_emc_sfkarticle: [], key_emc_sniveau: [], key_emc_sfkutilisateur: []}
    )
    for cmp in range(n_cmp):
        for utl in range(n_utl):
            if mat_cmp[cmp, utl] > 0:
                df_cmp = pd.concat(
                    [
                        df_cmp,
                        pd.DataFrame(
                            {
                                key_emc_sfkarticle: [ids_cmp[cmp]],
                                key_emc_sniveau: [mat_cmp[cmp, utl]],
                                key_emc_sfkutilisateur: [ids_utl[utl]],
                            }
                        ),
                    ],
                    ignore_index=True,
                )
    df_cmp = df_cmp.astype(int)

    mat_prj = np.random.randint(0, 2, (n_prj, n_utl))
    df_prj = pd.DataFrame(
        {
            key_user: [],
            key_project: [],
        }
    )
    for prj in range(n_prj):
        for utl in range(n_utl):
            if mat_prj[prj, utl] > 0:
                df_prj = pd.concat(
                    [
                        df_prj,
                        pd.DataFrame(
                            {
                                key_user: [ids_utl[utl]],
                                key_project: [ids_prj[prj]],
                            }
                        ),
                    ],
                    ignore_index=True,
                )
    df_prj = df_prj.astype(int)

    df_tsk = pd.DataFrame(
        {
            key_duree_evenement: [],
            key_evenement: [],
            key_competence: [],
            key_evenement_project: [],
        }
    )
    for i, tsk in enumerate(ids_tsk):
        p = np.random.uniform(0.1, 0.4)
        duree = np.random.binomial(50, p) / 4

        df_tsk = pd.concat(
            [
                df_tsk,
                pd.DataFrame(
                    {
                        key_duree_evenement: [duree],
                        key_evenement: [tsk],
                        key_competence: [choices(ids_cmp)[0]],
                        key_evenement_project: [choices(ids_prj)[0]],
                    },
                ),
            ],
            ignore_index=True,
        )

    for key in df_tsk.columns[1:]:
        df_tsk[key] = df_tsk[key].astype(int)

    np_ = np.round(df_tsk[key_duree_evenement].sum() / n_utl, 2) * np.random.uniform(0.8, 1.2)

    df_dsp = pd.DataFrame(
        {
            key_user: [],
            key_user_dispo: [],
        }
    )
    for utl in range(n_utl):
        p = np.random.uniform(0.1, 0.9)
        n = np_ / p
        dispo = np.random.binomial(n, p)
        df_dsp = pd.concat(
            [
                df_dsp,
                pd.DataFrame(
                    {key_user: [ids_utl[utl]], key_user_dispo: [dispo]},
                ),
            ],
            ignore_index=True,
        )
    df_dsp = df_dsp.astype(int)

    return df_prj, df_cmp, df_tsk, df_dsp


def mock_random_parameters() -> tuple[float, ContrainteEtreSurProjet, float]:
    """
    Génère des paramètres aléatoires de préférences d'optimisation.
    """
    curseur = np.random.uniform(0, 1)
    contrainte_etre_sur_projet = ContrainteEtreSurProjet(
        choices(["oui", "de_preference", "non"])
    )
    avantage_projet = np.random.randint(1, 5) * 1.0
    return curseur, contrainte_etre_sur_projet, avantage_projet
