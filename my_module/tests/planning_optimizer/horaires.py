import pandas as pd
import unittest
from my_module.planning_optimizer.tools.horaires import find_first_plage_horaire
from my_module.planning_optimizer.tools.horaires import avance_cuseur_temps


class TestFindPremierePlageHoraire(unittest.TestCase):
    def setUp(self):
        self.df_hors = []
        self.dates_debut = []

        self.df_hors.append(pd.DataFrame({'eeh_sfkperiode': {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 4},
                                          'eeh_xheuredebut': {0: '06:30',
                                                              1: '11:30',
                                                              2: '06:30',
                                                              3: '11:30',
                                                              4: '06:30',
                                                              5: '11:30',
                                                              6: '06:30',
                                                              7: '10:30',
                                                              8: '07:00'},
                                          'eeh_xheurefin': {0: '10:30',
                                                            1: '15:30',
                                                            2: '10:30',
                                                            3: '15:30',
                                                            4: '10:30',
                                                            5: '15:30',
                                                            6: '10:30',
                                                            7: '15:30',
                                                            8: '10:00'}}))

        self.dates_debut.append(pd.Timestamp('2022-09-01 00:00:00+0000', tz='UTC'))

        self.df_hors.append(pd.DataFrame({'eeh_sfkperiode': {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 4},
                                          'eeh_xheuredebut': {0: '06:30',
                                                              1: '11:30',
                                                              2: '06:30',
                                                              3: '11:30',
                                                              4: '06:30',
                                                              5: '11:30',
                                                              6: '06:30',
                                                              7: '10:30',
                                                              8: '07:00'},
                                          'eeh_xheurefin': {0: '10:30',
                                                            1: '15:30',
                                                            2: '10:30',
                                                            3: '15:30',
                                                            4: '10:30',
                                                            5: '15:30',
                                                            6: '10:30',
                                                            7: '15:30',
                                                            8: '10:00'}}))

        self.dates_debut.append(pd.Timestamp("2022-09-05T12:00:00.000Z"))

        self.df_hors.append(pd.DataFrame({'eeh_sfkperiode': {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 4},
                                          'eeh_xheuredebut': {0: '06:30',
                                                              1: '11:30',
                                                              2: '06:30',
                                                              3: '11:30',
                                                              4: '06:30',
                                                              5: '11:30',
                                                              6: '06:30',
                                                              7: '10:30',
                                                              8: '07:00'},
                                          'eeh_xheurefin': {0: '10:30',
                                                            1: '15:30',
                                                            2: '10:30',
                                                            3: '15:30',
                                                            4: '10:30',
                                                            5: '15:30',
                                                            6: '10:30',
                                                            7: '15:30',
                                                            8: '10:00'}}))

        self.dates_debut.append(pd.Timestamp("2022-09-05T17:00:00.000Z"))
        self.expected_results = [6, 1, 2]

    def test(self):
        for df_hor, date_debut, expected_result in zip(self.df_hors, self.dates_debut, self.expected_results):
            output_func = find_first_plage_horaire(df_hor, date_debut)
            self.assertEqual(output_func, expected_result)


class TestAvanceCurseurTemps(unittest.TestCase):
    def setUp(self):
        self.phs = []
        self.curseurs_temps = []
        self.expected_results = []

        # test 1
        self.phs.append(pd.Series({'eeh_sfkperiode': 0, 'eeh_xheuredebut': '06:30', 'eeh_xheurefin': '10:30'}))
        self.curseurs_temps.append(pd.Timestamp('2022-09-10 17:00:00+0000', tz='UTC'))
        self.expected_results.append(pd.Timestamp('2022-09-12 10:30:00+0000', tz='UTC'))

        # test 2
        self.phs.append(pd.Series({'eeh_sfkperiode': 1, 'eeh_xheuredebut': '11:30', 'eeh_xheurefin': '15:30'}))
        self.curseurs_temps.append(pd.Timestamp('2022-09-13 12:00:00+0000', tz='UTC'))
        self.expected_results.append(pd.Timestamp('2022-09-13 15:30:00+0000', tz='UTC'))

    def test(self):
        for ph, curseur_temps, expected_result in zip(self.phs, self.curseurs_temps, self.expected_results):
            output_func = avance_cuseur_temps(curseur_temps, ph)
            self.assertEqual(output_func, expected_result)
