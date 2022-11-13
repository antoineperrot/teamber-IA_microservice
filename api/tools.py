"""
Contient des petites fonctions utiles, notemment:
les fonctions de split des données pour planning_optimizer et task_assigner
une fois les données reçues de get_data_planning_optimizer et get_data_task_assigner.
"""
import simplejson


def return_json(response):
    """
    Standard json encoder fails to encode np.NaN.
    This function replaces NaNs with "null", and returns a JSON formatted string.
    """
    return simplejson.dumps(response, ignore_nan=True)
