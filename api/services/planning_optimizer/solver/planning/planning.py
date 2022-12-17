"""
Module de la classe d'optimisation des plannings.
"""
import datetime
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from api.services.planning_optimizer.solver.planning.solution_interpreter import schedule_events
from .ordonnancement import Ordonnancement


class SimulatedAnnealingPlanningOptimizer:
    def __init__(self,
                 availabilities: pd.DataFrame,
                 tasks: pd.DataFrame):

        self.availabilities = availabilities
        self.tasks = tasks

        self.preferences = [1 / 6, 2 / 3, 1 / 6]
        self.ordonnancement = Ordonnancement(df_tsk=tasks,
                                             availabilities=list(availabilities['durée'].values),
                                             preferences=self.preferences)
        self.statistics = None
        self.events = None
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
        n_iterations = len(self.tasks) * n_iterations_per_task

        ordonnancement = self.ordonnancement
        ordonnancement_optimal = self.ordonnancement
        temp = initial_temperature
        statistics = {"temperature": [temp],
                      "energy": [ordonnancement.get_energy()],
                      "energy_min": [ordonnancement_optimal.get_energy()],
                      "proba": []}

        decay = 1 - np.exp(np.log(min_temperature / initial_temperature) / n_iterations)
        for i in range(1, n_iterations):
            temp = temp * (1 - decay) if temp > min_temperature else min_temperature
            ordonnancement_voisin = ordonnancement.build_neighbour()

            energy_delta = ordonnancement_voisin.get_energy() - ordonnancement.energy
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

    def schedule_events(self) -> pd.DataFrame:
        """
        Construit le dataframe des tâches planifiées de manière optimale.
        """
        self.events = schedule_events(self.availabilities, self.tasks, self.ordonnancement)
        return self.events

    def get_unfilled_task(self):
        """
        Retourne les tâches qui n'ont pas été complètement planifiées.
        """
        temp = pd.DataFrame.copy(self.events)
        temp['start'] = temp['start'].apply(lambda x: datetime.datetime.fromisoformat(x))
        temp['end'] = temp['end'].apply(lambda x: datetime.datetime.fromisoformat(x))
        temp['durée_effectuée'] = np.round((temp['end'] - temp['start']) / datetime.timedelta(hours=1), 2)

        temp = temp[['evt_spkevenement', 'durée_effectuée']]
        temp = temp.groupby('evt_spkevenement').sum()

        sub_tasks = self.tasks
        sub_tasks = sub_tasks[['evt_spkevenement', "evt_dduree"]]
        sub_tasks = sub_tasks.groupby('evt_spkevenement').sum()

        completion_tasks = sub_tasks.join(temp, how='outer')
        completion_tasks = completion_tasks.fillna(0.0)
        completion_tasks['completion'] = (np.round(completion_tasks['durée_effectuée'] /
                                                   completion_tasks['evt_dduree']*100)).astype(int)
        completion_tasks = completion_tasks.loc[completion_tasks['completion'] < 100]

        sub_tasks2 = self.tasks[['evt_spkevenement', 'evt_sfkprojet', "priorite"]].groupby('evt_spkevenement').mean()

        completion_tasks = completion_tasks.join(sub_tasks2, how='outer')
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
