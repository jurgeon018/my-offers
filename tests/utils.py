import json
import os


def load_data(module, filename):
    filepath = os.path.join(os.path.dirname(module), 'data', filename)
    with open(filepath) as fp:
        return json.load(fp)
