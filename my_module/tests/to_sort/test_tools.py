# import sys
# sys.path.append('../src/')


def test_calcul_base_planning():
    import pandas as pd
    from my_module.tests.to_sort.test_data.reference_variables import (
        ref_plagehoraire_path,
        DATE_DEBUT,
        DATE_FIN,
        LONGUEUR_MIN,
        ref_base_path,
        read_base_or_imperatifs,
    )

    from module.planning_optimizer.tools import calcul_base_planning

    ph_df = pd.read_json(ref_plagehoraire_path)
    output = calcul_base_planning(
        ph_df, DATE_DEBUT, DATE_FIN, LONGUEUR_MIN=LONGUEUR_MIN
    )
    ref_base = read_base_or_imperatifs(ref_base_path)
    assert all(output == ref_base)


def test_add_imperatifs():
    from module.planning_optimizer.tools import add_imperatifs
    from my_module.tests.to_sort.test_data.reference_variables import (
        ref_imperatifs_path,
        ref_base_path,
        ref_base_sans_imperatifs_path,
        LONGUEUR_MIN,
        read_base_or_imperatifs,
    )

    ref_base = read_base_or_imperatifs(ref_base_path)
    ref_imperatifs = read_base_or_imperatifs(ref_imperatifs_path)
    ref_base_sans_imperatifs = read_base_or_imperatifs(ref_base_sans_imperatifs_path)

    output_func = add_imperatifs(ref_base, ref_imperatifs, LONGUEUR_MIN)

    assert all(output_func == ref_base_sans_imperatifs)


def test_split_tasks():
    import pandas as pd
    from my_module.tests.to_sort.test_data.reference_variables import (
        ref_tasks_path,
        mod_length,
        ref_splitted_tasks_path,
    )
    from module.planning_optimizer.tools import split_tasks

    tasks = pd.read_json(ref_tasks_path)
    output_func = split_tasks(tasks, mod_lenght=mod_length)
    ref_splitted_tasks = pd.read_json(ref_splitted_tasks_path)

    assert all(output_func == ref_splitted_tasks)
