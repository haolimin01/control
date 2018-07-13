# some util function for Flask App


def get_value(json, key, default=None):
    try:
        value = json[key]
    except KeyError:
        value = default
    finally:
        return value

