import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .tools.potentiels import *
from .tools.tools import *


class Planning(object):
    # Création de l'objet
    def __init__(
        self,
        plages_horaire_json_file: str,
        tasks_json_file: str,
        imperatifs_json_file: str,
        DATE_DEBUT: str,
        DATE_FIN: str,
        split_task_size: float = 1.0,
        longueur_min_plage: float = 0.5,
        longueur_max_plage: float = 3.0,
        seed=None,
    ):

        if seed is not None:
            np.random.seed(seed)

        self.plages_horaires = pd.read_json(plages_horaire_json_file)
        self.tasks_json_file = tasks_json_file
        self.imperatifs_json_file = imperatifs_json_file
        self.list_df_imperatifs = []
        self.df_imperatifs = None

        self.DATE_DEBUT = DATE_DEBUT
        self.DATE_FIN = DATE_FIN
        self.split_task_size = split_task_size  # exemple : si vaut 1 (heure), alors une tache de 3.5h est découpée en 3x 1h + 1x 0.5h, puis ces morceaux sont réarrangés

        self.longueur_min_plage = longueur_min_plage
        self.longueur_max_plage = longueur_max_plage
        self.penalties = np.array([1 / 6, 2 / 3, 1 / 6])
        self.has_tasks = False
        self.has_base = False
        self.has_scores = False
        self.initialised = False

        self._load_tasks()
        self._initialise_sprint()
        self._load_imperatifs()

    # Pour changer les paramètres d'optimisation :
    def set_penalties(self, new_penalties):
        if np.sum(new_penalties) == 0:
            self.penalties = np.array([1 / 3, 1 / 3, 1 / 3])
        else:
            self.penalties = np.array(new_penalties) / np.sum(new_penalties)
        if self.has_tasks:
            self._update_scores()

    # Ajout des tâches à planifier
    def _load_tasks(self):
        df_tasks = pd.read_json(self.tasks_json_file)
        df_tasks = split_tasks(df_tasks, self.split_task_size)
        self.tasks = df_tasks[["id morceau", "Durée", "Priorité", "id tache"]].values.T
        self.df_tasks = df_tasks.set_index("id morceau")
        self.total_time_tasks = self.tasks[1, :].sum()
        self.has_tasks = True
        self.min_tasks = (
            self.tasks
        )  # Calcul de la base de planning et des potentiels initiaux

    # Créé la base d'une planning et initialise les scores si des tâches ont été ajoutées.
    def _initialise_sprint(self):

        self.base = calcul_base_planning(
            self.plages_horaires, self.DATE_DEBUT, self.DATE_FIN
        )

        self.temps_total_dispo = self.base["Longueur"].sum()
        if self.temps_total_dispo == 0:
            print(
                f"L'utilisateur n'a aucune disponibilité à la période de projection indiquée."
            )

        self.base_array = self.base[["index", "Longueur"]].values.T

        if self.has_tasks:
            self._update_scores()
            self.min_chronologie = self.chronologie

        # self.prop_temps_perdu, self.chronologie = V_TempsPerdu(self.tasks, self.base_array)
        # self.score_priorites = V_Priorites(self.tasks)

        self.temps_total_dispo = self.base["Longueur"].sum()
        self.initialised = True
        self.has_new_imp = False

    # Ajout d'impératifs à prendre en compte
    def _load_imperatifs(self):
        df = pd.read_json(self.imperatifs_json_file)  # reading json file

        # converting time columns :
        df["Date début"] = pd.to_datetime(df["Date début"], unit="ms")
        df["Date fin"] = pd.to_datetime(df["Date fin"], unit="ms")

        self.base = add_imperatifs(
            self.base, df, self.DATE_DEBUT, self.longueur_min_plage
        )  # enlève les moments de disponibilités correspondants aux impératifs
        self.list_df_imperatifs.append(df)
        self.df_imperatifs = pd.concat(self.list_df_imperatifs)

        # maths : tableau numpy des plages horaires successives
        self.base_array = self.base[["index", "Longueur"]].values.T
        self.temps_total_dispo = self.base["Longueur"].sum()
        if self.has_tasks:
            self._update_scores()
            self.min_chronologie = self.chronologie

    # (maths) Met à jour les potentiels s'il y eu des changements
    def _update_scores(self):
        self.score_temps_perdu, self.chronologie = V_TempsPerdu(
            self.tasks, self.base_array
        )
        self.score_priorites = V_Priorites(self.tasks)
        self.score_dispersion = V_Dispersion(self.tasks)
        self.score = np.vdot(
            self.penalties,
            [self.score_temps_perdu, self.score_priorites, self.score_dispersion],
        )

    # Affiche les scores pour les différents indicateurs :
    def show_scores(self):
        if self.has_tasks:
            print(
                "Pourcentage temps perdu : {:.2f}%".format(self.score_temps_perdu * 100)
            )
            print("Non respect priorités : {:.2f}%".format(self.score_priorites * 100))
            print("Score dispersion : {:.2f}%".format(self.score_dispersion * 100))
        else:
            print(
                "Impossible d'afficher les scores, veuillez ajouter des tâches au planning."
            )

    # (maths) Propose un arrangement voisin des taches et stocke ses potentiels
    def _build_neighbour(self):
        self.next_tasks = permute_tasks(self.tasks)
        self.next_score_temps_perdu, self.next_chronologie = V_TempsPerdu(
            self.next_tasks, self.base_array
        )
        self.next_score_priorites = V_Priorites(self.next_tasks)
        self.next_score_dispersion = V_Dispersion(self.next_tasks)
        self.next_score = np.vdot(
            self.penalties,
            [
                self.next_score_temps_perdu,
                self.next_score_priorites,
                self.next_score_dispersion,
            ],
        )

    # (maths) Remplace l'arrangement courant par l'arrangement voisin
    def _replace(self):
        self.tasks = self.next_tasks
        self.score_temps_perdu = self.next_score_temps_perdu
        self.chronologie = self.next_chronologie
        self.score_priorites = self.next_score_priorites
        self.score_dispersion = self.next_score_dispersion
        self.score = self.next_score

    # (maths) Stocke l'arrangement conduisant à l'énergie totale la plus faible
    def _replace_min(self):
        self.min_tasks = self.tasks
        self.min_chronologie = self.chronologie

    # (maths) Remplace l'arrangement courant par l'arrangement "minimal" rencontré

    def _apply_min(self):
        self.tasks = self.min_tasks
        self.chronologie = self.chronologie
        self._update_scores()

    # (maths) Renvoie les potentiels de l'arrangement courant ou voisin selon la valeur
    # du paramètre voisin
    def get_potentiels(self, voisin=False):
        if not voisin:
            return [self.score_temps_perdu, self.score_priorites, self.score_dispersion]
        else:
            return [
                self.next_score_temps_perdu,
                self.next_score_priorites,
                self.next_score_dispersion,
            ]

    # Exporte le planning en fichier excel et retourne le dataframe correspondant
    def make_planning(self):
        df = pd.DataFrame()
        if self.has_tasks:
            self._apply_min()

            plages = np.unique(self.chronologie[1, :])
            for plage in plages:

                tmp2 = np.array(
                    [
                        self.chronologie[0, i]
                        if self.chronologie[1, i] == plage
                        else -1
                        for i in range(self.chronologie.shape[1])
                    ]
                )
                tmp2 = tmp2[tmp2 >= 0]

                p = self.base.loc[[plage]]
                t = self.df_tasks.loc[tmp2]

                d = p["Date début"].values[0]

                t["Durée cumulée"] = pd.to_timedelta(t["Durée"].cumsum(), unit="h")
                t["Durée"] = pd.to_timedelta(t["Durée"], unit="h")

                t["Date fin"] = d + t["Durée cumulée"]

                t["Date début"] = t["Date fin"] - t["Durée"]
                t.drop(["Durée", "Durée cumulée"], axis=1, inplace=True)
                df = pd.concat([df, t])

            df = df[["Objet", "Priorité", "Date début", "Date fin"]]

        DF = pd.concat([df, self.df_imperatifs])
        DF.sort_values(by="Date début", inplace=True)
        DF.reset_index(inplace=True)
        DF = DF[["Objet", "Priorité", "Date début", "Date fin"]]

        ### ON RECOLLE LES MORCEAUX DE TACHES SI POSSIBLE :
        df = DF.loc[
            [0],
        ]
        index_df = 0
        index_DF = 1
        while index_DF < len(DF):
            while (
                DF.loc[index_DF, "Date début"] == df.loc[index_df, "Date fin"]
                and DF.loc[index_DF, "Objet"] == df.loc[index_df, "Objet"]
            ):

                df.loc[index_df, "Date fin"] = DF.loc[index_DF, "Date fin"]
                index_DF += 1
            if index_DF < len(DF):
                df = df.append(DF.loc[[index_DF],]).reset_index(drop=True)
                index_df += 1
                index_DF += 1

        ###EXPORT :
        self.result = df
        return df

    # (maths) Optimise le planning
    def optimize(
        self,
        ITERATIONS_PAR_TACHE=150,
        TEMPERATURE_INITIALE=1,
        TEMPERATURE_MIN=1e-5,
        show=False,
    ):
        N_ITERATIONS = self.tasks.shape[1] * ITERATIONS_PAR_TACHE
        Proba = np.zeros(N_ITERATIONS)
        E = np.zeros(N_ITERATIONS)
        E[0] = self.score
        Emin = np.copy(E)
        Vp = np.zeros(N_ITERATIONS)
        Vtp = np.zeros(N_ITERATIONS)
        Vd = np.zeros(N_ITERATIONS)
        Vp[0], Vtp[0], Vd[0] = (
            self.score_priorites,
            self.score_temps_perdu,
            self.score_dispersion,
        )
        T = TEMPERATURE_INITIALE
        decay = 1 - np.exp(
            np.log(TEMPERATURE_MIN / TEMPERATURE_INITIALE) / N_ITERATIONS
        )
        for i in range(1, N_ITERATIONS):
            T = T * (1 - decay) if T > TEMPERATURE_MIN else TEMPERATURE_MIN
            self._build_neighbour()
            Ey = self.next_score
            DELTA = Ey - E[i - 1]
            Proba[i] = min(1, np.exp(-DELTA / T))
            if np.random.rand() < Proba[i]:
                self._replace()
                E[i] = Ey
            else:
                E[i] = E[i - 1]

            if E[i] < Emin[i - 1]:
                self._replace_min()
                Emin[i] = E[i]
            else:
                Emin[i] = Emin[i - 1]
            Vp[i], Vtp[i], Vd[i] = (
                self.score_priorites,
                self.score_temps_perdu,
                self.score_dispersion,
            )
        if show:
            plt.figure(figsize=(16, 7))
            col = "cornflowerblue"

            ax1 = plt.subplot(121, title="Energie totale")
            ax1.grid()
            ax1.plot(range(N_ITERATIONS), Emin, c="magenta", label="Emin")
            ax1.plot(range(N_ITERATIONS), E, label="Etotale", c=col)
            ax1.legend(loc="upper right")
            ax1.set_xlabel("Itérations")

            """
            ax2 = plt.subplot(122, title='Evolution probabilité acceptation (moving average)')
            ax2.grid()
            ax2.scatter(range(N_ITERATIONS),Proba,marker='.',linewidth=.5,c=col)
            ax2.set_xlabel('Itérations')
            plt.show()
            """
            ax3 = plt.subplot(122, title="Différents potentiels")
            ax3.plot(range(N_ITERATIONS), Vp, label="Priorités")
            ax3.plot(range(N_ITERATIONS), Vtp, label="Temps perdu")
            ax3.plot(range(N_ITERATIONS), Vd, label="Dispersion")
            ax3.legend()
            ax3.grid()
            plt.show()

    # Fait l'inventaire des tâches non planifiées
    def not_scheduled(self):
        tasks = self.tasks[0, :]
        c = self.chronologie[0, :]
        not_scheduled = []
        for t in tasks:
            if t not in c:
                not_scheduled.append(int(t))
        if len(not_scheduled) > 0:
            notScheduledTasks = self.df_tasks.loc[not_scheduled]
            notScheduledTasks = pd.DataFrame(
                notScheduledTasks.groupby(
                    ["id tache", "Objet", "Priorité"], as_index=False
                )["Durée"].sum()
            )
            return notScheduledTasks
        else:
            print("Toutes les tâches ont pu être planifiées.")
            return None
