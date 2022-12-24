import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection


def make_timeline(availabilities: pd.DataFrame,
                  events: pd.DataFrame,
                  imperatifs: pd.DataFrame):
    """
    Dessine la timeline des événements planifiées, des disponibilités de travail et des impératifs.
    """
    data_availabilities = []

    for i, row in availabilities.iterrows():
        data_availabilities.append(
            (row['timestamp_debut'].to_pydatetime(),
             row['timestamp_fin'].to_pydatetime(),
             'availabilities'
             ))

    data_imperatifs = []

    for i, row in imperatifs.iterrows():
        data_imperatifs.append(
            (row['evt_xdate_debut'].to_pydatetime(),
             row['evt_xdate_fin'].to_pydatetime(),
             'imperatif'
             ))

    data_work = []

    for i, row in events.iterrows():
        data_work.append(
            (row['start'].to_pydatetime(),
             row['end'].to_pydatetime(),
             'work'
             ))

    data = data_work + data_imperatifs + data_availabilities

    cats = {"imperatif": 1, "availabilities": 2, "work": 3}
    colormapping = {"availabilities": "C0", "imperatif": "C1", "work": "C2"}

    verts = []
    colors = []
    for d in data:
        v = [(mdates.date2num(d[0]), cats[d[2]] - .4),
             (mdates.date2num(d[0]), cats[d[2]] + .4),
             (mdates.date2num(d[1]), cats[d[2]] + .4),
             (mdates.date2num(d[1]), cats[d[2]] - .4),
             (mdates.date2num(d[0]), cats[d[2]] - .4)]
        verts.append(v)
        colors.append(colormapping[d[2]])

    bars = PolyCollection(verts, facecolors=colors)

    fig, ax = plt.subplots(figsize=(14, 3))
    ax.add_collection(bars)
    ax.autoscale()
    loc = mdates.MinuteLocator(byminute=[0, 15, 30, 45])
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["imperatif", "availabilities", "work"])

    fig.tight_layout()
    return fig
