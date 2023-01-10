import numpy as np

# CALCULS DE POTENTIELS : un potentiel


# Calcule le pourcentage de temps perdu sur les plages horaires utilisées
def energy_waisted_time(ordo_length: list[float], sections_lengths: list[float]):
    """
    Calcule le temps perdu pour un ordonnancement donné.

    :param ordo_length: liste des durées successives des tâches
    :param sections_lengths: liste des durées successives des sections temporelle de travail.

    :return ratio_waisted_time: float, proportion du temps total travaillé sur le temps total disponible.
    """
    n_tasks, n_sections = len(ordo_length), len(sections_lengths)

    wasted_time = 0
    total_available_time = 0
    i_section, i_length = 0, 0
    while i_length < n_tasks and i_section < n_sections:
        current_section_used_time = 0
        j = i_length
        current_section_is_filled = False
        total_available_time += sections_lengths[i_section]
        while j < n_tasks and not current_section_is_filled:
            if (
                ordo_length[j] + current_section_used_time
                <= sections_lengths[i_section]
            ):
                current_section_used_time += ordo_length[j]
                j += 1
            else:
                current_section_is_filled = True

        i_length = j

        total_available_time += sections_lengths[i_section]
        wasted_time += max(sections_lengths[i_section] - current_section_used_time, 0)
        i_section += 1

    ratio_wasted_time = wasted_time / total_available_time

    return ratio_wasted_time


# Calcule un potentiel correspondant au non respect des priorités
def energy_key_project_prioritys(ordo_prio):
    target = np.sort(ordo_prio)
    energy = (
        np.linalg.norm(target - ordo_prio, ord=1)
        / len(np.unique(ordo_prio))
        / len(ordo_prio)
    )
    return energy


# Calcule un potentiel correspondant au taux de dispersion moyen de chaque tâche
def energy_dispersion(ordo_evt):
    """
    Calcule une énergie de dispersion, quantifiant si une tâche est réalisée d'un bloc (energie = 0),
    ou à plusieurs occasions (energie > 0).
    """
    list_evt = np.unique(ordo_evt)
    pen = 0
    c = 0
    for t in list_evt:
        indexs = np.where(ordo_evt == t)[0]
        if len(indexs) > 1:
            c += 1
            pen_local = 0
            for i in range(len(indexs) - 1):
                if indexs[i + 1] > indexs[i] + 1:
                    pen_local += 1
            pen_local /= len(indexs)
            pen += pen_local
    out = pen / c if c > 0 else 0
    return out
