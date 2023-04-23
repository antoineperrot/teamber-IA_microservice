import datetime
import unittest

import pandas as pd
from api.string_keys import *
from api.services.planning_optimizer.lib_planning_optimizer.planning.horaires import (
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
                    key_day_plage_horaire: {
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
                    key_debut_plage_horaire: {
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
                    key_fin_plage_horaire: {
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
                    key_day_plage_horaire: {
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
                    key_debut_plage_horaire: {
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
                    key_fin_plage_horaire: {
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
                    key_day_plage_horaire: {
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
                    key_debut_plage_horaire: {
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
                    key_fin_plage_horaire: {
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
                    key_day_plage_horaire: 0,
                    key_debut_plage_horaire: "06:30",
                    key_fin_plage_horaire: "10:30",
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
                    key_day_plage_horaire: 1,
                    key_debut_plage_horaire: "11:30",
                    key_fin_plage_horaire: "15:30",
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
        """setup"""

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
                    key_day_plage_horaire: {
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
                    key_debut_plage_horaire: {
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
                    key_fin_plage_horaire: {
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
                    KEY_TIMESTAMP_DEBUT: {
                        0: pd.Timestamp("2022-10-03 06:30:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                    },
                    KEY_TIMESTAMP_FIN: {
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
                    key_day_plage_horaire: {
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
                    key_debut_plage_horaire: {
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
                    key_fin_plage_horaire: {
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
                    KEY_TIMESTAMP_DEBUT: {
                        0: pd.Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                    },
                    KEY_TIMESTAMP_FIN: {
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
                    key_day_plage_horaire: {
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
                    key_debut_plage_horaire: {
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
                    key_fin_plage_horaire: {
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
                    KEY_TIMESTAMP_DEBUT: {
                        0: pd.Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                        7: pd.Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                    },
                    KEY_TIMESTAMP_FIN: {
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
                    key_day_plage_horaire: {
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
                    key_debut_plage_horaire: {
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
                    key_fin_plage_horaire: {
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
                    KEY_TIMESTAMP_DEBUT: {
                        0: pd.Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                    },
                    KEY_TIMESTAMP_FIN: {
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
                    key_day_plage_horaire: {
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
                    key_debut_plage_horaire: {
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
                    key_fin_plage_horaire: {
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
                    KEY_TIMESTAMP_DEBUT: {
                        0: pd.Timestamp("2022-10-03 06:31:00+0000", tz="UTC"),
                        1: pd.Timestamp("2022-10-03 11:30:00+0000", tz="UTC"),
                        2: pd.Timestamp("2022-10-04 06:30:00+0000", tz="UTC"),
                        3: pd.Timestamp("2022-10-04 11:30:00+0000", tz="UTC"),
                        4: pd.Timestamp("2022-10-05 06:30:00+0000", tz="UTC"),
                        5: pd.Timestamp("2022-10-05 11:30:00+0000", tz="UTC"),
                        6: pd.Timestamp("2022-10-06 06:30:00+0000", tz="UTC"),
                        7: pd.Timestamp("2022-10-06 10:30:00+0000", tz="UTC"),
                    },
                    KEY_TIMESTAMP_FIN: {
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
            pd.testing.assert_frame_equal(output_func, expected_result, check_dtype=False)


class TestFindSectionsEnds(unittest.TestCase):
    def setUp(self):
        self.date_start = pd.Timestamp("2022-09-05 07:00:00+0000")
        self.date_end = pd.Timestamp("2022-09-09 16:00:00+0000")
        self.imperatifs = pd.DataFrame(
            {
                key_evenement: {
                    0: 1040,
                    1: 3302,
                    2: 3449,
                    3: 4743,
                    4: 7069,
                    5: 7105,
                    6: 9323,
                },
                key_evenement_project: {
                    0: 1404,
                    1: 2140,
                    2: 3790,
                    3: 4896,
                    4: 5363,
                    5: 8423,
                    6: 8534,
                },
                key_competence: {
                    0: 2283,
                    1: 2283,
                    2: 2283,
                    3: 2283,
                    4: 2283,
                    5: 2283,
                    6: 2283,
                },
                key_evenement_date_debut: {
                    0: pd.Timestamp("2022-09-05 08:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 15:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 09:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-07 07:00:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-07 07:30:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-07 13:00:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-08 14:30:00+0000", tz="UTC"),
                },
                key_evenement_date_fin: {
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
                KEY_START: {
                    0: pd.Timestamp("2022-09-05 07:00:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 09:30:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-05 17:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-06 10:00:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-07 08:45:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-07 14:10:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-08 15:30:00+0000", tz="UTC"),
                },
                KEY_END: {
                    0: pd.Timestamp("2022-09-05 08:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 15:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 09:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-07 07:00:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-07 13:00:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-08 14:30:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-09 16:00:00+0000", tz="UTC"),
                },
            }
        )

    def test_find_sections_ends(self):
        output_func = find_sections_ends(imperatifs=self.imperatifs,
                                         date_start=self.date_start,
                                         date_end=self.date_end)

        pd.testing.assert_frame_equal(output_func, self.expected_result, check_dtype=False)


class TestComputeAvailabilities(unittest.TestCase):
    def setUp(self):
        self.date_start = datetime.datetime(2022, 9, 5, 9, 0, 0) #"2022-09-05 09:00:00+0000"
        self.date_end = datetime.datetime(2022, 9, 9, 16, 0, 0) #"2022-09-09 16:00:00+0000"
        self.min_duration_section = 0.5
        self.horaires = pd.DataFrame(
            {
                key_day_plage_horaire: {
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
                key_debut_plage_horaire: {
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
                key_fin_plage_horaire: {
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
                key_evenement: {
                    0: 1040,
                    1: 3302,
                    2: 3449,
                    3: 4743,
                    4: 7069,
                    5: 7105,
                    6: 9323,
                },
                key_evenement_project: {
                    0: 1404,
                    1: 2140,
                    2: 3790,
                    3: 4896,
                    4: 5363,
                    5: 8423,
                    6: 8534,
                },
                key_competence: {
                    0: 2283,
                    1: 2283,
                    2: 2283,
                    3: 2283,
                    4: 2283,
                    5: 2283,
                    6: 2283,
                },
                key_evenement_date_debut: {
                    0: pd.Timestamp("2022-09-05 08:30:00+0000", tz="UTC"),
                    1: pd.Timestamp("2022-09-05 15:00:00+0000", tz="UTC"),
                    2: pd.Timestamp("2022-09-06 09:00:00+0000", tz="UTC"),
                    3: pd.Timestamp("2022-09-07 07:00:00+0000", tz="UTC"),
                    4: pd.Timestamp("2022-09-07 07:30:00+0000", tz="UTC"),
                    5: pd.Timestamp("2022-09-07 13:00:00+0000", tz="UTC"),
                    6: pd.Timestamp("2022-09-08 14:30:00+0000", tz="UTC"),
                },
                key_evenement_date_fin: {
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
                KEY_TIMESTAMP_DEBUT: {
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
                KEY_TIMESTAMP_FIN: {
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
                KEY_DUREE: {
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

    def test_compute_availabilities_2(self):
        date_start = datetime.datetime(2023, 1, 16, 5, 0, 0) # "2023-01-16T05:00:00"
        date_end = datetime.datetime(2023, 1, 16, 18, 1, 55) #.fromisoformat("2023-01-16T18:01:55")
        min_duration_section = 0.001

        horaires = pd.DataFrame({key_day_plage_horaire: {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 4},
                     key_debut_plage_horaire: {0: '06:30',
                      1: '11:30',
                      2: '06:30',
                      3: '11:30',
                      4: '06:30',
                      5: '11:30',
                      6: '06:30',
                      7: '11:30',
                      8: '07:00'},
                     key_fin_plage_horaire: {0: '10:30',
                      1: '15:30',
                      2: '10:30',
                      3: '15:30',
                      4: '10:30',
                      5: '15:30',
                      6: '10:30',
                      7: '15:30',
                      8: '10:00'}})

        imperatifs = pd.DataFrame.from_dict({key_evenement: {0: 3161,
                                              1: 6673,
                                              2: 1232,
                                              3: 2186,
                                              4: 1036,
                                              5: 5544,
                                              6: 6362},
                                             key_evenement_project: {0: 6063,
                                              1: 8646,
                                              2: 4321,
                                              3: 4947,
                                              4: 1696,
                                              5: 6471,
                                              6: 7457},
                                             'lgl_sfkligneparent': {0: 9006,
                                              1: 9006,
                                              2: 9006,
                                              3: 9006,
                                              4: 9006,
                                              5: 9006,
                                              6: 9006},
                                             key_evenement_date_debut: {0: pd.Timestamp('2023-01-16 07:15:00', tz="UTC"),
                                              1: pd.Timestamp('2023-01-16 07:20:00', tz="UTC"),
                                              2: pd.Timestamp('2023-01-16 08:35:00', tz="UTC"),
                                              3: pd.Timestamp('2023-01-16 09:45:00', tz="UTC"),
                                              4: pd.Timestamp('2023-01-16 10:05:00', tz="UTC"),
                                              5: pd.Timestamp('2023-01-16 12:50:00', tz="UTC"),
                                              6: pd.Timestamp('2023-01-16 17:35:00', tz="UTC")},
                                             key_evenement_date_fin: {0: pd.Timestamp('2023-01-16 07:55:00', tz="UTC"),
                                              1: pd.Timestamp('2023-01-16 07:55:00', tz="UTC"),
                                              2: pd.Timestamp('2023-01-16 09:10:00', tz="UTC"),
                                              3: pd.Timestamp('2023-01-16 10:30:00', tz="UTC"),
                                              4: pd.Timestamp('2023-01-16 10:30:00', tz="UTC"),
                                              5: pd.Timestamp('2023-01-16 13:15:00', tz="UTC"),
                                              6: pd.Timestamp('2023-01-16 18:20:00', tz="UTC")}})

        expected_result = pd.DataFrame.from_dict({KEY_TIMESTAMP_DEBUT: {0: pd.Timestamp('2023-01-16 06:30:00', tz="UTC"),
                                                  1: pd.Timestamp('2023-01-16 07:55:00', tz="UTC"),
                                                  2: pd.Timestamp('2023-01-16 09:10:00', tz="UTC"),
                                                  3: pd.Timestamp('2023-01-16 11:30:00', tz="UTC"),
                                                  4: pd.Timestamp('2023-01-16 13:15:00', tz="UTC")},
                                                 KEY_TIMESTAMP_FIN: {0: pd.Timestamp('2023-01-16 07:15:00', tz="UTC"),
                                                  1: pd.Timestamp('2023-01-16 08:35:00', tz="UTC"),
                                                  2: pd.Timestamp('2023-01-16 09:45:00', tz="UTC"),
                                                  3: pd.Timestamp('2023-01-16 12:50:00', tz="UTC"),
                                                  4: pd.Timestamp('2023-01-16 15:30:00', tz="UTC")},
                                                 KEY_DUREE: {0: 0.75,
                                                  1: 0.6666666666666666,
                                                  2: 0.5833333333333334,
                                                  3: 1.3333333333333333,
                                                  4: 2.25}})
        output_func = compute_availabilities(
            working_times=horaires,
            imperatifs=imperatifs,
            date_start=date_start,
            date_end=date_end,
            min_duration_section=min_duration_section,
        )

        pd.testing.assert_frame_equal(output_func, expected_result, check_dtype=False)

