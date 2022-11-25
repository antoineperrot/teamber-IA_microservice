import pandas as pd
from pandas import Timestamp
import unittest
from module.planning_optimizer.tools.horaires import find_next_ph
from module.planning_optimizer.tools.horaires import avance_cuseur_temps
from module.planning_optimizer.tools.horaires import make_df_ph


class TestFindNextPlageHoraire(unittest.TestCase):
    def setUp(self):
        self.df_hors = []
        self.curseurs_temps = []

        # TODO : rajouter un test pour quand curseur temps = fin de la précédente plage horaire.
        # TODO : rajouter un test pour quand heure curseur temps = début dune plage horaire

        self.df_hors.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": {
                        0: 0,
                        1: 0,
                        2: 1,
                        3: 1,
                        4: 2,
                        5: 2,
                        6: 3,
                        7: 3,
                        8: 4,
                    },
                    "eeh_xheuredebut": {
                        0: "06:30",
                        1: "11:30",
                        2: "06:30",
                        3: "11:30",
                        4: "06:30",
                        5: "11:30",
                        6: "06:30",
                        7: "10:30",
                        8: "07:00",
                    },
                    "eeh_xheurefin": {
                        0: "10:30",
                        1: "15:30",
                        2: "10:30",
                        3: "15:30",
                        4: "10:30",
                        5: "15:30",
                        6: "10:30",
                        7: "15:30",
                        8: "10:00",
                    },
                }
            )
        )

        self.curseurs_temps.append(pd.Timestamp("2022-09-01 00:00:00+0000", tz="UTC"))

        self.df_hors.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": {
                        0: 0,
                        1: 0,
                        2: 1,
                        3: 1,
                        4: 2,
                        5: 2,
                        6: 3,
                        7: 3,
                        8: 4,
                    },
                    "eeh_xheuredebut": {
                        0: "06:30",
                        1: "11:30",
                        2: "06:30",
                        3: "11:30",
                        4: "06:30",
                        5: "11:30",
                        6: "06:30",
                        7: "10:30",
                        8: "07:00",
                    },
                    "eeh_xheurefin": {
                        0: "10:30",
                        1: "15:30",
                        2: "10:30",
                        3: "15:30",
                        4: "10:30",
                        5: "15:30",
                        6: "10:30",
                        7: "15:30",
                        8: "10:00",
                    },
                }
            )
        )

        self.curseurs_temps.append(pd.Timestamp("2022-09-05T12:00:00.000Z"))

        self.df_hors.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": {
                        0: 0,
                        1: 0,
                        2: 1,
                        3: 1,
                        4: 2,
                        5: 2,
                        6: 3,
                        7: 3,
                        8: 4,
                    },
                    "eeh_xheuredebut": {
                        0: "06:30",
                        1: "11:30",
                        2: "06:30",
                        3: "11:30",
                        4: "06:30",
                        5: "11:30",
                        6: "06:30",
                        7: "10:30",
                        8: "07:00",
                    },
                    "eeh_xheurefin": {
                        0: "10:30",
                        1: "15:30",
                        2: "10:30",
                        3: "15:30",
                        4: "10:30",
                        5: "15:30",
                        6: "10:30",
                        7: "15:30",
                        8: "10:00",
                    },
                }
            )
        )

        self.curseurs_temps.append(pd.Timestamp("2022-09-05T17:00:00.000Z"))
        self.expected_results = [6, 1, 2]

    def test(self):
        for df_hor, curseur_temps, expected_result in zip(
            self.df_hors, self.curseurs_temps, self.expected_results
        ):
            output_func = find_next_ph(df_hor, curseur_temps)
            self.assertEqual(output_func, expected_result)


class TestAvanceCurseurTemps(unittest.TestCase):
    def setUp(self):
        self.phs = []
        self.curseurs_temps = []
        self.dates_fins_sprint = []
        self.expected_results = []

        # test 1
        self.phs.append(
            pd.Series(
                {
                    "eeh_sfkperiode": 0,
                    "eeh_xheuredebut": "06:30",
                    "eeh_xheurefin": "10:30",
                }
            )
        )
        self.curseurs_temps.append(pd.Timestamp("2022-09-10 17:00:00+0000", tz="UTC"))
        self.expected_results.append(pd.Timestamp("2022-09-12 10:30:00+0000", tz="UTC"))
        self.dates_fins_sprint.append(pd.Timestamp("2022-12-01T00:00:00.000Z"))

        # test 2
        self.phs.append(
            pd.Series(
                {
                    "eeh_sfkperiode": 1,
                    "eeh_xheuredebut": "11:30",
                    "eeh_xheurefin": "15:30",
                }
            )
        )
        self.curseurs_temps.append(pd.Timestamp("2022-09-13 12:00:00+0000", tz="UTC"))
        self.expected_results.append(pd.Timestamp("2022-09-13 15:30:00+0000", tz="UTC"))
        self.dates_fins_sprint.append(pd.Timestamp("2022-12-01T00:00:00.000Z"))

    def test(self):
        for ph, curseur_temps, date_fin_sprint, expected_result in zip(
            self.phs, self.curseurs_temps, self.dates_fins_sprint, self.expected_results
        ):
            output_func = avance_cuseur_temps(curseur_temps, date_fin_sprint, ph)
            self.assertEqual(output_func, expected_result)


class TestMakeDfPh(unittest.TestLoader):
    def setUp(self):
        self.dates_debut = []
        self.dates_fin = []
        self.df_horaires = []
        self.expected_results = []

        # cas 1
        self.dates_debut.append("2022-10-01T06:00:00.000Z")
        self.dates_fin.append("2022-10-06T08:00:00.000Z")
        self.df_horaires.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": {
                        0: 0,
                        1: 0,
                        2: 1,
                        3: 1,
                        4: 2,
                        5: 2,
                        6: 3,
                        7: 3,
                        8: 4,
                    },
                    "eeh_xheuredebut": {
                        0: "06:30",
                        1: "11:30",
                        2: "06:30",
                        3: "11:30",
                        4: "06:30",
                        5: "11:30",
                        6: "06:30",
                        7: "10:30",
                        8: "07:00",
                    },
                    "eeh_xheurefin": {
                        0: "10:30",
                        1: "15:30",
                        2: "10:30",
                        3: "15:30",
                        4: "10:30",
                        5: "15:30",
                        6: "10:30",
                        7: "15:30",
                        8: "10:00",
                    },
                }
            )
        )
        self.expected_results.append(
            pd.DataFrame(
                {
                    "timestamp_debut": {
                        0: Timestamp("2022-10-03 06:30:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 08:00:00+0000", tz="UTC"),
                    },
                }
            )
        )

        # cas 2
        self.dates_debut.append("2022-10-03T06:31:00.000Z")
        self.dates_fin.append("2022-10-06T08:00:00.000Z")
        self.df_horaires.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": {
                        0: 0,
                        1: 0,
                        2: 1,
                        3: 1,
                        4: 2,
                        5: 2,
                        6: 3,
                        7: 3,
                        8: 4,
                    },
                    "eeh_xheuredebut": {
                        0: "06:30",
                        1: "11:30",
                        2: "06:30",
                        3: "11:30",
                        4: "06:30",
                        5: "11:30",
                        6: "06:30",
                        7: "10:30",
                        8: "07:00",
                    },
                    "eeh_xheurefin": {
                        0: "10:30",
                        1: "15:30",
                        2: "10:30",
                        3: "15:30",
                        4: "10:30",
                        5: "15:30",
                        6: "10:30",
                        7: "15:30",
                        8: "10:00",
                    },
                }
            )
        )
        self.expected_results.append(
            pd.DataFrame(
                {
                    "timestamp_debut": {
                        0: Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 08:00:00+0000", tz="UTC"),
                    },
                }
            )
        )

        # cas 3
        self.dates_debut.append("2022-10-03T06:31:00.000Z")
        self.dates_fin.append("2022-10-06T15:30:00.000Z")
        self.df_horaires.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": {
                        0: 0,
                        1: 0,
                        2: 1,
                        3: 1,
                        4: 2,
                        5: 2,
                        6: 3,
                        7: 3,
                        8: 4,
                    },
                    "eeh_xheuredebut": {
                        0: "06:30",
                        1: "11:30",
                        2: "06:30",
                        3: "11:30",
                        4: "06:30",
                        5: "11:30",
                        6: "06:30",
                        7: "10:30",
                        8: "07:00",
                    },
                    "eeh_xheurefin": {
                        0: "10:30",
                        1: "15:30",
                        2: "10:30",
                        3: "15:30",
                        4: "10:30",
                        5: "15:30",
                        6: "10:30",
                        7: "15:30",
                        8: "10:00",
                    },
                }
            )
        )
        self.expected_results.append(
            pd.DataFrame(
                {
                    "timestamp_debut": {
                        0: Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                        7: Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                        7: Timestamp("2022-10-06 15:30:00+0000", tz="UTC"),
                    },
                }
            )
        )

        # cas 4
        self.dates_debut.append("2022-10-03T06:31:00.000Z")
        self.dates_fin.append("2022-10-06T10:30:00.000Z")
        self.df_horaires.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": {
                        0: 0,
                        1: 0,
                        2: 1,
                        3: 1,
                        4: 2,
                        5: 2,
                        6: 3,
                        7: 3,
                        8: 4,
                    },
                    "eeh_xheuredebut": {
                        0: "06:30",
                        1: "11:30",
                        2: "06:30",
                        3: "11:30",
                        4: "06:30",
                        5: "11:30",
                        6: "06:30",
                        7: "10:30",
                        8: "07:00",
                    },
                    "eeh_xheurefin": {
                        0: "10:30",
                        1: "15:30",
                        2: "10:30",
                        3: "15:30",
                        4: "10:30",
                        5: "15:30",
                        6: "10:30",
                        7: "15:30",
                        8: "10:00",
                    },
                }
            )
        )
        self.expected_results.append(
            pd.DataFrame(
                {
                    "timestamp_debut": {
                        0: Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                    },
                }
            )
        )

        # cas 5
        self.dates_debut.append("2022-10-03T06:31:00.000Z")
        self.dates_fin.append("2022-10-07T07:00:00.000Z")
        self.df_horaires.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": {
                        0: 0,
                        1: 0,
                        2: 1,
                        3: 1,
                        4: 2,
                        5: 2,
                        6: 3,
                        7: 3,
                        8: 4,
                    },
                    "eeh_xheuredebut": {
                        0: "06:30",
                        1: "11:30",
                        2: "06:30",
                        3: "11:30",
                        4: "06:30",
                        5: "11:30",
                        6: "06:30",
                        7: "10:30",
                        8: "07:00",
                    },
                    "eeh_xheurefin": {
                        0: "10:30",
                        1: "15:30",
                        2: "10:30",
                        3: "15:30",
                        4: "10:30",
                        5: "15:30",
                        6: "10:30",
                        7: "15:30",
                        8: "10:00",
                    },
                }
            )
        )
        self.expected_results.append(
            pd.DataFrame(
                {
                    "timestamp_debut": {
                        0: Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                        7: Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                        7: Timestamp("2022-10-06 15:30:00+0000", tz="UTC"),
                    },
                }
            )
        )

    def test(self):
        for date_debut, date_fin, df_hor, expected_result in zip(
            self.dates_debut, self.dates_fin, self.df_horaires, self.expected_results
        ):
            output_func = make_df_ph(df_hor, date_debut, date_fin)
            pd.testing.assert_frame_equal(output_func, expected_result)
