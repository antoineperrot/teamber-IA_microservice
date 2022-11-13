
import pandas as pd
from test_data.reference_data.reference_variables import *


def to_json(path):
    return pd.read_json(path).to_json()


from module.planning_optimizer import Planning


p = Planning(
    plages_horaire_json_file=to_json(ref_plagehoraire_path),
    tasks_json_file=to_json(ref_tasks_path),
    imperatifs_json_file=to_json(ref_imperatifs_path),
    DATE_DEBUT=DATE_DEBUT,
    DATE_FIN=DATE_FIN,
    split_task_size=mod_length,
    longueur_min_plage=LONGUEUR_MIN,
    longueur_max_plage=LONGUEUR_MAX,
    seed=seed,
)


def test_correct_base_sans_imperatifs_calculation():
    assert all(p.base == read_base_or_imperatifs(ref_base_sans_imperatifs_path))


def test_optimization():
    p.optimize()
    assert p.score < 0.07
