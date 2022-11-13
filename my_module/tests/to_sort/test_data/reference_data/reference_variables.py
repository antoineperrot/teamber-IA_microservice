DATE_DEBUT = "2020-05-11 08:30:00"
DATE_FIN = "2020-05-15 18:00:00"
LONGUEUR_MIN = 0.5
LONGUEUR_MAX = 3.0
mod_length = 1.0
seed = 1

test_data_path = "test_data/"
ref_path = "reference_data/"

ref_plagehoraire_path = test_data_path + ref_path + "horaires.json"
ref_tasks_path = test_data_path + ref_path + "taches.json"
ref_imperatifs_path = test_data_path + ref_path + "imperatifs.json"
ref_base_path = test_data_path + ref_path + "base.json"
ref_base_sans_imperatifs_path = test_data_path + ref_path + "base_sans_imperatifs.json"
ref_splitted_tasks_path = test_data_path + ref_path + "splitted_tasks.json"
ref_optimized_planning = test_data_path + ref_path + "optimized_planning.json"

import pandas as pd


def read_base_or_imperatifs(path_to_json_file):
    df = pd.read_json(path_to_json_file)
    df["Date début"] = pd.to_datetime(df["Date début"], unit="ms")
    df["Date fin"] = pd.to_datetime(df["Date fin"], unit="ms")
    return df
