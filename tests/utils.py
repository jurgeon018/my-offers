import json
import os
from typing import Dict


def _get_filepath(module, filename):
    return os.path.join(os.path.dirname(module), 'data', filename)


def load_json_data(module, filename) -> Dict:
    with open(_get_filepath(module, filename)) as fp:
        return json.load(fp)


def save_json_data(module, filename, data: Dict) -> None:
    with open(_get_filepath(module, filename), 'w') as fp:
        return json.dump(fp, data, indent=2, sort_keys=True)


def load_data(module, filename):
    with open(_get_filepath(module, filename)) as fp:
        return fp.read()


def save_data(module, filename: str, data: str) -> None:
    with open(_get_filepath(module, filename), 'w') as fp:
        fp.write(data)
