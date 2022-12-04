"""
Module de la classe d'optimisation des plannings.
"""
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .ordonnancement import Ordonnancement

import datetime


class SimulatedAnnealingPlanningOptimizer:
    def __init__(self,
                 availabilities: pd.DataFrame,
                 df_tsk: pd.DataFrame):

        self.availabilities = availabilities
        self.df_tsk = df_tsk

        self.preferences = [1 / 6, 2 / 3, 1 / 6]
        self.ordonnancement = Ordonnancement(df_tsk=df_tsk,
                                             availabilities=list(availabilities['durée'].values),
                                             preferences=self.preferences)
        self.statistics = None
        self.scheduled_tasks = None
        self.unfilled_tasks = None

    def optimize(self,
                 n_iterations_per_task: int = 250,
                 initial_temperature: float = 1,
                 min_temperature: float = 1e-5):
        """
        Optimise un ordonnancement des tâches par la méthode du recuit simulé.

        :param n_iterations_per_task: nombre d'itérations par tâches.
        :param initial_temperature: float, température initiale
        :param min_temperature: float, température minimale à atteindre
        """
        n_iterations = len(self.df_tsk) * n_iterations_per_task

        ordonnancement = self.ordonnancement
        ordonnancement_optimal = self.ordonnancement
        temp = initial_temperature
        statistics = {"temperature": [temp],
                      "energy": [ordonnancement.energy],
                      "energy_min": [ordonnancement_optimal.energy],
                      "proba": []}

        decay = 1 - np.exp(np.log(min_temperature / initial_temperature) / n_iterations)
        for i in range(1, n_iterations):
            temp = temp * (1 - decay) if temp > min_temperature else min_temperature
            ordonnancement_voisin = ordonnancement.build_neighbour()

            energy_delta = ordonnancement_voisin.energy - ordonnancement.energy
            proba_transition = min(1, np.exp(- energy_delta / temp))

            if np.random.rand() < proba_transition:
                ordonnancement = ordonnancement_voisin

            if ordonnancement.energy < ordonnancement_optimal.energy:
                ordonnancement_optimal = ordonnancement

            statistics['temperature'].append(temp)
            statistics['energy'].append(ordonnancement.energy)
            statistics['energy_min'].append(ordonnancement_optimal.energy)
            statistics['proba'].append(proba_transition)

        self.statistics = statistics
        self.ordonnancement = ordonnancement_optimal

    def schedule_tasks(self):
        """
        Construit le dataframe des tâches planifiées de manière optimale.
        """

        out = {"id_part": [],
               "start": [],
               "end": []}

        i_current_section = 0
        no_more_sections = i_current_section == len(self.availabilities)

        i_current_part = 0
        no_more_parts = i_current_part == len(self.df_tsk)

        while not no_more_parts and not no_more_sections:
            current_section_is_filled = False
            current_section_start = self.availabilities.iloc[i_current_section]['timestamp_debut']
            current_section_end = self.availabilities.iloc[i_current_section]['timestamp_fin']
            curseur_temps = current_section_start

            while not current_section_is_filled and not no_more_parts:
                id_part = self.ordonnancement.ordonnancement[i_current_part]
                part = self.df_tsk.iloc[i_current_part]
                length_part = datetime.timedelta(hours=part['length'])
                if curseur_temps + length_part > current_section_end:
                    current_section_is_filled = True
                    i_current_section += 1
                else:
                    out['id_part'].append(id_part)
                    out['start'].append(curseur_temps)
                    out['end'].append(curseur_temps + length_part)
                    i_current_part += 1
                    no_more_parts = i_current_part == len(self.df_tsk)
                    curseur_temps = curseur_temps + length_part

            no_more_sections = i_current_section == len(self.availabilities)

        out = pd.DataFrame(out)
        out = out.merge(self.df_tsk, on='id_part')
        out = out[['start', 'end', 'evt_spkevenement', 'evt_sfkprojet', 'priorite']]

        out_joined_parts = {'start': [],
                            "end": [],
                            "evt_spkevenement": [],
                            "evt_sfkprojet": [],
                            "priorite": []}

        i_current_part = 0
        i_next_current_part = min(i_current_part + 1, len(out))
        while i_current_part < len(out):
            current_part = out.iloc[i_current_part]
            if i_next_current_part - i_current_part > 1:
                next_current_part = out.iloc[i_next_current_part]

                while next_current_part['start'] == current_part['end'] and \
                        next_current_part['evt_spkevenement'] == current_part['evt_spkevenement']:
                    i_next_current_part = min(i_next_current_part + 1, len(out))
                    next_current_part = out.iloc[i_next_current_part]

            if i_next_current_part - i_current_part > 1:
                out_joined_parts['start'].append(current_part['start'])
                out_joined_parts['end'].append(next_current_part['end'])
                out_joined_parts['evt_spkevenement'].append(current_part['evt_spkevenement'])
                out_joined_parts['evt_sfkprojet'].append(current_part['evt_sfkprojet'])
                out_joined_parts['priorite'].append(current_part['priorite'])
                i_current_part = min(i_next_current_part + 1, len(out))
                i_next_current_part = min(i_current_part + 1, len(out))
            else:
                out_joined_parts['start'].append(current_part['start'])
                out_joined_parts['end'].append(current_part['end'])
                out_joined_parts['evt_spkevenement'].append(current_part['evt_spkevenement'])
                out_joined_parts['evt_sfkprojet'].append(current_part['evt_sfkprojet'])
                out_joined_parts['priorite'].append(current_part['priorite'])
                i_current_part = i_next_current_part
                i_next_current_part = min(i_current_part + 1, len(out))

        out_joined_parts = pd.DataFrame(out_joined_parts)
        self.scheduled_tasks = out_joined_parts
        return out_joined_parts

    def get_unfilled_task(self):
        """
        Retourne les tâches qui n'ont pas été complètement planifiées.
        """
        temp = self.scheduled_tasks
        temp['durée_effectuée'] = (self.scheduled_tasks['end'] - self.scheduled_tasks['start']) / \
                                   datetime.timedelta(hours=1)
        temp = temp[['evt_spkevenement', 'durée_effectuée']]
        temp = temp.groupby('evt_spkevenement').sum()

        sub_df_tsk = self.df_tsk
        sub_df_tsk = sub_df_tsk[['evt_spkevenement', "evt_dduree", "evt_sfkprojet"]]
        sub_df_tsk = sub_df_tsk.groupby('evt_spkevenement').sum()

        completion_tasks = sub_df_tsk.join(temp, how='outer')
        completion_tasks = completion_tasks.fillna(0.0)
        completion_tasks['completion'] = (np.round(completion_tasks['durée_effectuée'] /
                                                   completion_tasks['evt_dduree']*100)).astype(int)
        completion_tasks = completion_tasks.loc[completion_tasks['completion'] < 100]
        unfilled_tasks = completion_tasks.reset_index().sort_values(by=['completion', "evt_sfkprojet"],
                                                                    ascending=False).reset_index(drop=True)
        self.unfilled_tasks = unfilled_tasks
        return unfilled_tasks

    def plot_optimization_statistics(self):
        """
        Plot l'évolution de
        - la température
        - l'énergie
        - l'énergie de la solution optimale
        - la probabilité de transition.
        """
        fig, ax = plt.subplots(2, 2, figsize=(8, 8))

        for i, (key_stat, stat) in enumerate(self.statistics.items()):
            ax.flat[i].set_title(key_stat)
            if key_stat != "proba":
                ax.flat[i].plot(range(len(stat)), stat)
            else:
                ax.flat[i].scatter(range(len(stat)), stat)
