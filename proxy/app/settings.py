import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')

with open(config_path, 'r') as file:
    data = json.load(file)

MULTICAST_GROUP = data['MULTICAST_GROUP']
INTERFACE_IP = data['INTERFACE_IP']
INTERFACE_IP_FINAL = data['INTERFACE_IP_FINAL']
SD_PORT = data['SD_PORT']
NEXT_PORT = data['NEXT_PORT']
