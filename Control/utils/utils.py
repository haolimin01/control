# some util function for Flask App
import json


def get_value(json, key, default=None):
    try:
        value = json[key]
    except KeyError:
        value = default
    finally:
        return value


def send_msg(error, detail):
    data = {
        'error': error,
        'detail': detail
    }
    return json.dumps(data, ensure_ascii=False) + '\n'


def send_index(author, email, about):
    data = {
        'author': author,
        'email': email,
        'about': about
    }
    return json.dumps(data, ensure_ascii=False) + '\n'

