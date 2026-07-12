import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')

_defaults: dict = {}
if os.path.exists(config_path):
    with open(config_path, 'r') as file:
        _defaults = json.load(file)


def _get(key: str, cast=str):
    env_val = os.environ.get(key)
    if env_val is not None:
        return cast(env_val)
    if key in _defaults:
        return _defaults[key]
    raise KeyError(f"Missing config value: {key}")


MULTICAST_GROUP = _get('MULTICAST_GROUP')
INTERFACE_IP = _get('INTERFACE_IP')
INTERFACE_IP_FINAL = _get('INTERFACE_IP_FINAL')
SD_PORT = _get('SD_PORT', int)
NEXT_PORT = _get('NEXT_PORT', int)
