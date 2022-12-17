import unittest

import pandas as pd

from api.services.planning_optimizer.solver.planning.horaires import (
    find_next_ph,
    avance_cuseur_temps,
    make_base,
    find_sections_ends,
    compute_availabilities,
)


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
                        0: pd.Timestamp("2022-10-03 06:30:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: pd.Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 08:00:00+0000", tz="UTC"),
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
                        0: pd.Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: pd.Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 08:00:00+0000", tz="UTC"),
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
                        0: pd.Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                        7: pd.Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: pd.Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                        7: pd.Timestamp("2022-10-06 15:30:00+0000", tz="UTC"),
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
                        0: pd.Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: pd.Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
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
                        0: pd.Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                        7: pd.Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                    },
                    "timestamp_fin": {
                        0: pd.Timestamp("2022-10-03 10:30:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 15:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 10:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 15:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 10:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 15:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                        7: pd.Timestamp("2022-10-06 15:30:00+0000", tz="UTC"),
                    },
                }
            )
        )

    def test(self):
        for date_debut, date_fin, df_hor, expected_result in zip(
            self.dates_debut, self.dates_fin, self.df_horaires, self.expected_results
        ):
            output_func = make_base(df_hor, date_debut, date_fin)
            pd.testing.assert_frame_equal(output_func, expected_result)


class TestFindSectionsEnds(unittest.TestCase):
    def setUp(self):
        self.date_end = pd.Timestamp("2022-09-09 16:00:00+0000")
        self.imperatifs = pd.DataFrame(
            {
                "evt_spkevenement": {
                    0: 1040,
                    1: 3302,
                    2: 3449,
                    3: 4743,
                    4: 7069,
                    5: 7105,
                    6: 9323,
                },
                "evt_sfkprojet": {
                    0: 1404,
                    1: 2140,
                    2: 3790,
                    3: 4896,
                    4: 5363,
                    5: 8423,
                    6: 8534,
                },
                "lgl_sfkligneparent": {
                    0: 2283,
                    1: 2283,
                    2: 2283,
                    3: 2283,
                    4: 2283,
                    5: 2283,
                    6: 2283,
                },
                "evt_xdate_debut": {
                    0: pd.Timestamp("2022-09-05 08:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 15:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 09:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-07 07:00:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-07 07:30:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-07 13:00:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-08 14:30:00+0000", tz="UTC"),
                },
                "evt_xdate_fin": {
                    0: pd.Timestamp("2022-09-05 09:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 17:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 10:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-07 08:15:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-07 08:45:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-07 14:10:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-08 15:30:00+0000", tz="UTC"),
                },
            }
        )

        self.expected_result = pd.DataFrame(
            {
                "start": {
                    0: pd.Timestamp("2022-09-05 09:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 17:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 10:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-07 08:45:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-07 14:10:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-08 15:30:00+0000", tz="UTC"),
                },
                "end": {
                    0: pd.Timestamp("2022-09-05 15:00:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-06 09:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-07 07:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-07 13:00:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-08 14:30:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-09 16:00:00+0000", tz="UTC"),
                },
            }
        )

    def test_find_sections_ends(self):
        output_func = find_sections_ends(self.imperatifs, self.date_end)

        pd.testing.assert_frame_equal(output_func, self.expected_result)


class TestComputeAvailabilities(unittest.TestCase):
    def setUp(self):
        self.date_start = "2022-09-05 09:00:00+0000"
        self.date_end = "2022-09-09 16:00:00+0000"
        self.min_duration_section = 0.5
        self.horaires = pd.DataFrame(
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
        self.imperatifs = pd.DataFrame(
            {
                "evt_spkevenement": {
                    0: 1040,
                    1: 3302,
                    2: 3449,
                    3: 4743,
                    4: 7069,
                    5: 7105,
                    6: 9323,
                },
                "evt_sfkprojet": {
                    0: 1404,
                    1: 2140,
                    2: 3790,
                    3: 4896,
                    4: 5363,
                    5: 8423,
                    6: 8534,
                },
                "lgl_sfkligneparent": {
                    0: 2283,
                    1: 2283,
                    2: 2283,
                    3: 2283,
                    4: 2283,
                    5: 2283,
                    6: 2283,
                },
                "evt_xdate_debut": {
                    0: pd.Timestamp("2022-09-05 08:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 15:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 09:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-07 07:00:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-07 07:30:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-07 13:00:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-08 14:30:00+0000", tz="UTC"),
                },
                "evt_xdate_fin": {
                    0: pd.Timestamp("2022-09-05 09:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 17:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 10:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-07 08:15:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-07 08:45:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-07 14:10:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-08 15:30:00+0000", tz="UTC"),
                },
            }
        )

        self.expected_result = pd.DataFrame(
            {
                "timestamp_debut": {
                    0: pd.Timestamp("2022-09-05 09:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 11:30:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 06:30:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-06 10:00:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-06 11:30:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-07 06:30:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-07 08:45:00+0000", tz="UTC"),
                    7: pd.Timestamp("2022-09-07 11:30:00+0000", tz="UTC"),
                    8: pd.Timestamp("2022-09-07 14:10:00+0000", tz="UTC"),
                    9: pd.Timestamp("2022-09-08 06:30:00+0000", tz="UTC"),
                    10: pd.Timestamp("2022-09-08 10:30:00+0000", tz="UTC"),
                    11: pd.Timestamp("2022-09-09 07:00:00+0000", tz="UTC"),
                },
                "timestamp_fin": {
                    0: pd.Timestamp("2022-09-05 10:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 15:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 09:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-06 10:30:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-06 15:30:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-07 07:00:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-07 10:30:00+0000", tz="UTC"),
                    7: pd.Timestamp("2022-09-07 13:00:00+0000", tz="UTC"),
                    8: pd.Timestamp("2022-09-07 15:30:00+0000", tz="UTC"),
                    9: pd.Timestamp("2022-09-08 10:30:00+0000", tz="UTC"),
                    10: pd.Timestamp("2022-09-08 14:30:00+0000", tz="UTC"),
                    11: pd.Timestamp("2022-09-09 10:00:00+0000", tz="UTC"),
                },
                "durée": {
                    0: 1.0,
                    1: 3.5,
                    2: 2.5,
                    3: 0.5,
                    4: 4.0,
                    5: 0.5,
                    6: 1.75,
                    7: 1.5,
                    8: 1.3333333333333333,
                    9: 4.0,
                    10: 4.0,
                    11: 3.0,
                },
            }
        )

    def test_compute_availabilities(self):
        output_func = compute_availabilities(
            self.horaires,
            self.imperatifs,
            self.date_start,
            self.date_end,
            self.min_duration_section,
        )
