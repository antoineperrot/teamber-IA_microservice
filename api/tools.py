import simplejson


def return_json(response):
    """
    Standard json encoder fails to encode np.NaN.
    This function replaces NaNs with "null", and returns a JSON formatted string.
    """
    return simplejson.dumps(response, ignore_nan=True)
