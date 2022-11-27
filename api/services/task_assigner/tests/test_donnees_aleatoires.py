"""
Teste la validité de solutions calculées sur des données aléatoires.
"""
from module.tests.task_assigner import (
    mock_coherent_data,
    mock_random_parameters,
)
from modules.task_assigner import solveur
from module.tests.task_assigner import TestSolution

import unittest


class TestDonneesAleatoire(unittest.TestCase):
    def setUp(self) -> None:
        self.nombre_cas = 10
        self.jeux_de_donnees = [mock_coherent_data() for i in range(self.nombre_cas)]
        self.parametres = [mock_random_parameters() for i in range(self.nombre_cas)]

    def test_donnees_aleatoires(self):
        for jeu_de_donnees, parametre in zip(self.jeux_de_donnees, self.parametres):
            solution = solveur(*jeu_de_donnees, *parametre)
            test_solution = TestSolution(solution)
            test_solution.test_validite_mathematique()
            test_solution.test_validation_stat_cmp()
            test_solution.test_validation_stat_prj()
            test_solution.test_validation_stat_tsk()
            test_solution.test_validation_stat_utl()
