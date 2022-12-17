import pandas as pd

default_horaires = pd.DataFrame(
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
