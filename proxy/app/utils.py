import json
import os
from proxy.app import settings


def get_config_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'config.json')


def increment_port():
    config_path = get_config_path()

    with open(config_path, 'r') as file:
        data = json.load(file)

    data['NEXT_PORT'] += 1

    with open(config_path, 'w') as file:
        json.dump(data, file, indent=4)

    settings.NEXT_PORT = data['NEXT_PORT']

