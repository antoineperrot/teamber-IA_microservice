import datetime
import numpy as np
import pandas as pd

# Calcule la base du planning, supprime les plages horaires < LONGUEUR MIN


# Reconstruit la base en prenant en compte des impératifs
def add_imperatifs(
    base: pd.DataFrame, imp: pd.DataFrame, DATE_DEBUT: str, LONGUEUR_MIN: float = 0.5
):
    df = pd.DataFrame.copy(base)
    for index, row in imp.iterrows():

        di = row["Date début"]  # début impératif
        fi = row["Date fin"]  # fin impératif

        ## un impératif recouvre entièrement une plage horaire :
        #  on la supprime alors
        indexNames = df.loc[(df["Date début"] >= di) & (df["Date fin"] <= fi)].index
        if len(indexNames) > 0:

            df.drop(indexNames, inplace=True)
            df.reset_index(inplace=True, drop=True)

        # un impératif est à cheval sur le début d'une plage horaire :
        # on décale alors le début de cette ph et la marge à la fin de cet
        # impératif
        indexNames = df.loc[
            (df["Date début"] < fi) & (fi < df["Date fin"]) & (di <= df["Date début"])
        ].index
        if len(indexNames) > 0:
            df.loc[indexNames, "Date début"] = fi

            df.reset_index(inplace=True, drop=True)

        # idem : à cheval fin ph
        indexNames = df.loc[
            (df["Date début"] < di) & (di < df["Date fin"]) & (fi >= df["Date fin"])
        ].index
        if len(indexNames) > 0:
            df.loc[indexNames, "Date fin"] = di

        # Un impératif tombe au milieu d'une ph : on la transforme en
        # deux ph, une avant et une après
        indexNames = df.loc[(df["Date début"] < di) & (df["Date fin"] > fi)].index
        if len(indexNames) > 0:
            tmp1 = pd.DataFrame.copy(df.loc[indexNames])
            tmp2 = pd.DataFrame.copy(df.loc[indexNames])
            df.drop(indexNames, inplace=True)
            tmp1["Date fin"] = di
            tmp2["Date début"] = fi
            df = pd.DataFrame.copy(pd.concat([df, tmp1, tmp2]))
            df.reset_index(inplace=True, drop=True)
            # df = pd.DataFrame.copy(pd.concat([df,tmp2]))

        # Réordonnement du dataframe par ordre chronologique :
        df.sort_values(by="Date début", inplace=True)

        # calcul des longueurs avec/sans marges des ph :
        df["Longueur"] = df["Date fin"] - df["Date début"]
        df["Longueur"] = df["Longueur"].astype("timedelta64[m]") / 60
        DATE_DEBUT = pd.to_datetime(DATE_DEBUT)
        df["Temps écoulé"] = (df["Date début"] - DATE_DEBUT) / np.timedelta64(1, "h")

        #         #Suppression des ph trop courtes :
        indexNames = df.loc[df["Longueur"] < LONGUEUR_MIN].index
        df.drop(indexNames, inplace=True)

        df = df.round(2)
        df.reset_index(inplace=True, drop=True)
        df["index"] = df.index

    return df


# (maths) Permute deux taches dans une liste de tache
def permute_tasks(tasks):
    y = np.copy(tasks)
    i = np.random.randint(tasks.shape[1])
    j = np.random.randint(tasks.shape[1])
    y[:, i] = tasks[:, j]
    y[:, j] = tasks[:, i]
    return y


# Découpe des tâches en morceaux n'excédant pas une durée choisie (mod_lenght en heure)
# ----> Avec mod_lenght = 1, une tâche de 3h30 est découpée
#       en 3 morceaux d'une heure et 1 d'une demi-heure
def split_tasks(df: pd.DataFrame, mod_lenght: float = 1):

    df["nb Morceaux ceil"] = np.ceil(df["Durée"] / mod_lenght).astype(int)
    df["nb Morceaux plein"] = (df["Durée"] // mod_lenght).astype(int)
    df["Restant"] = df["Durée"] - mod_lenght * df["nb Morceaux plein"]

    ilocs = np.sum(
        [
            [id_tache] * nb_morceau
            for (id_tache, nb_morceau) in zip(df["id tache"], df["nb Morceaux ceil"])
        ]
    )

    list_duree = np.array(
        np.sum(
            [
                [mod_lenght] * nb_morceau_plein + (restant != 0) * [restant]
                for duree, nb_morceau_plein, restant in zip(
                    df["Durée"], df["nb Morceaux plein"], df["Restant"]
                )
            ]
        )
    )

    new_df = df.loc[ilocs]
    new_df["Durée"] = list_duree
    new_df["id morceau"] = range(len(new_df))
    new_df.drop(
        ["nb Morceaux ceil", "nb Morceaux plein", "Restant"], axis=1, inplace=True
    )

    new_df.reset_index(drop=True, inplace=True)
    return new_df
