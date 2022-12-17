"""
Classe d'un ordonnancement.
"""
from random import choice

import numpy as np
import pandas as pd

from api.services.planning_optimizer.solver.tools.energies import energy_dispersion, energy_priorites, \
    energy_waisted_time


class Ordonnancement:
    """
    Classe Ordonnancement, représentant un ordonnancement possible des tâches dans un emploi du temps.
    """
    def __init__(self, availabilities, preferences,  df_tsk: pd.DataFrame | None  = None, ordonnancement=None):
        if ordonnancement is None and df_tsk is not None:
            self.tasks = df_tsk[["id_part", "length", "priorite", "evt_spkevenement"]].values
            self.ordonnancement = list(df_tsk['id_part'].values.astype(int))
        else:
            self.ordonnancement = ordonnancement
        self.availabilities = availabilities

        self.preferences = preferences
        self.energy: float = np.inf
        self.energies = {"dispersion": np.inf,
                         "priorités": np.inf,
                         "temps_perdu": np.inf}

    def build_neighbour(self):
        """
        Renvoie un objet Ordonnancement "voisin" de self, dans lequel deux tâches ont été permutées.
        """
        new_ordonnancement = self.ordonnancement.copy()
        index_1 = choice(list(range(len(self.ordonnancement))))
        index_2 = choice(list(range(len(self.ordonnancement))))

        new_ordonnancement[index_1] = self.ordonnancement[index_2]
        new_ordonnancement[index_2] = self.ordonnancement[index_1]
        neighbour_preferences = self.preferences.copy()
        neighbour = Ordonnancement(ordonnancement=new_ordonnancement,
                                   availabilities=self.availabilities,
                                   preferences=neighbour_preferences)
        neighbour.tasks = np.copy(self.tasks)

        return neighbour
    
    def get_fields(self):
        """
        Retourne les durées, priorités et événements succéssifs lié à l'ordonnancement.
        """
        length, priorite, evt = self.tasks[:, [1,2,3]].T
        ordo_length, ordo_priorite, ordo_evt = \
                length[self.ordonnancement], priorite[self.ordonnancement], evt[self.ordonnancement] 
        return ordo_length, ordo_priorite, ordo_evt
    
    def compute_energy(self):
        """
        Calcule les différentes energies associées à l'ordonancement 
        """
        ordo_length, ordo_priorite, ordo_evt = self.get_fields()
        
        e_dispersion = energy_dispersion(ordo_evt)
        e_priorite = energy_priorites(ordo_priorite)
        e_wasted_time = energy_waisted_time(ordo_length, self.availabilities)
        energies = [e_dispersion, e_priorite, e_wasted_time]

        self.energies["dispersion"] = e_dispersion,
        self.energies["priorités"]  = e_priorite,
        self.energies["temps_perdu"] = e_priorite
            
        self.energy = np.vdot(self.preferences, energies)

    def get_energy(self):
        self.compute_energy()
        return self.energy
        