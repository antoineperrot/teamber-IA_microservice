"""
Teste la validité de solutions calculées sur des données aléatoires.
"""
import unittest

from api.services.task_assigner.solver import solveur
from api.services.task_assigner.tests.data_mocker import (
    mock_coherent_data,
    mock_random_parameters,
)
from api.services.task_assigner.tests.test_solution import TestSolution


class TestDonneesAleatoire(unittest.TestCase):
    def setUp(self) -> None:
        self.nombre_cas = 10
        self.jeux_de_donnees = [mock_coherent_data() for _i in range(self.nombre_cas)]
        self.parametres = [mock_random_parameters() for _i in range(self.nombre_cas)]

    def test_donnees_aleatoires(self):
        for jeu_de_donnees, parametre in zip(self.jeux_de_donnees, self.parametres):
            solution = solveur(*jeu_de_donnees, *parametre)
            test_solution = TestSolution(solution)
            test_solution.test_validite_mathematique()
            test_solution.test_validation_stat_cmp()
            test_solution.test_validation_stat_prj()
            test_solution.test_validation_stat_tsk()
            test_solution.test_validation_stat_utl()
