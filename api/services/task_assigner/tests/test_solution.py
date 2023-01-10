import unittest

import pandas as pd


# class TestSolution(unittest.TestCase):
#     def __init__(self, solution: dict):
#         super(TestSolution, self).__init__()
#         self.solution = solution
#
#     def test_validite_mathematique(self):
#         solution_brute = pd.DataFrame(self.solution["solution_brute"])
#         self.assertTrue(
#             all(solution_brute["duree_assignee"] >= 0),
#             msg="Un nombre d'heure négatif a été assigné.",
#         )
#         self.assertTrue(
#             all(solution_brute["duree_assignee"] <= solution_brute["tsk_lgt"]),
#             msg="La durée assignée pour certaines tâches excède celle leur durée.",
#         )
#
#     def test_validation_stat_cmp(self):
#         stat_cmp = pd.DataFrame(self.solution["statistics"]["cmp"])
#         self.assertTrue(
#             all(stat_cmp["total_h_non_assignees"] >= 0),
#             msg="ValueError dans total_h_non_assignee",
#         )
#         self.assertTrue(
#             all(
#                 stat_cmp[~stat_cmp["niveau_cmp_moyen_par_h_realisee"].isna()][
#                     "niveau_cmp_moyen_par_h_realisee"
#                 ]
#                 <= 3
#             ),
#             msg="Mauvais calcul du niveau moyen d'exécution dune tache : > 3.",
#         )
#         self.assertTrue(
#             all(
#                 stat_cmp[~stat_cmp["niveau_cmp_moyen_par_h_realisee"].isna()][
#                     "niveau_cmp_moyen_par_h_realisee"
#                 ]
#                 >= 0
#             ),
#             msg="Mauvais calcul du niveau moyen d'exécution dune tache : < 0.",
#         )
#
#     def test_validation_stat_utl(self):
#         stat_utl = pd.DataFrame(self.solution["statistics"]["utl"])
#         self.assertTrue(
#             all(stat_utl.taux_occupation.apply(pd.notna)),
#             msg="TypeError: les données de taux d'occupation contiennent des NaN.",
#         )
#         self.assertTrue(
#             all(
#                 stat_utl.taux_occupation.apply(
#                     lambda x: isinstance(x, (float, int)) and 0 <= x <= 1
#                 )
#             ),
#             msg="TypeError: les données de taux d'occupation sont incorrectes.",
#         )
#         self.assertTrue(
#             all(stat_utl.dsp_utl.apply(pd.notna)),
#             msg="TypeError: les données de disponibilités totales contiennent des NaN.",
#         )
#         self.assertTrue(
#             all(
#                 stat_utl.dsp_utl.apply(
#                     lambda x: (isinstance(x, float) or isinstance(x, int)) and x >= 0
#                 )
#             ),
#             msg="TypeError: les données de disponibilités totales sont incorrectes.",
#         )
#         self.assertTrue(
#             all(stat_utl.dsp_utl.apply(lambda x: x >= 0)),
#             msg="TypeError: Certaines données de disponibilités totales sont négatives.",
#         )
#         self.assertTrue(
#             all(stat_utl["total_h_assignees"] <= stat_utl["dsp_utl"]),
#             msg="Certains utilisateurs sont trop chargés par rapport à leurs disponibiltés.",
#         )
#         self.assertTrue(
#             all(stat_utl["niveau_moyen_execution_tsk"] <= 3),
#             msg="Le calcul du niveau moyen d'exécution d'une tache par unité de temps est FAUX.",
#         )
#         self.assertTrue(
#             all(stat_utl["niveau_moyen_execution_tsk"] >= 0),
#             msg="Le calcul du niveau moyen d'exécution d'une tache par unité de temps est FAUX.",
#         )
#
#     def test_validation_stat_prj(self):
#         stat_prj = pd.DataFrame(self.solution["statistics"]["prj"])
#         self.assertTrue(
#             all(stat_prj["total_h_non_assignees"] >= 0),
#             msg="ValueError dans temps_total_non_assigne",
#         )
#         self.assertTrue(
#             all(stat_prj.n_missing_cmp_per_prj.apply(lambda x: isinstance(x, int))),
#             msg="ValueError: Le nombre de compétences manquantes par projet n'est pas toujours un entier.",
#         )
#
#     def test_validation_stat_tsk(self):
#         stat_tsk = pd.DataFrame(self.solution["statistics"]["tsk"])
#         self.assertTrue(
#             all(stat_tsk.n_utl_per_tsk.apply(lambda x: isinstance(x, int))),
#             msg="ValueError: Le nombre d'utilisateurs par tache n'est pas toujours un entier.",
#         )
