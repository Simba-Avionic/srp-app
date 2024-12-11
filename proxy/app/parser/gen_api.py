import os

from proxy.app.parser.services.engineservice import EngineServiceManager

API_BASE_DIR = os.path.join(os.path.dirname(__file__), "../api")


def create_api_directory(manager_name):
    manager_dir = os.path.join(API_BASE_DIR, manager_name)
    os.makedirs(manager_dir, exist_ok=True)

    init_file = os.path.join(manager_dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write(f"# Package for {manager_name} API\n")

    return manager_dir


def generate_blueprint_code(manager_name, manager):
    methods_code = ""
    imports_code = """
import sys
import os

from flask import Blueprint, jsonify, request
"""

    for method_name in dir(manager):
        method = getattr(manager, method_name)
        if callable(method) and method_name[0].isupper():
            deserialization_class = f"{method_name}Out"
            imports_code += f"from proxy.app.parser.custom_dataclasses.{manager_name}service_dataclass import {deserialization_class}\n"

            methods_code += f"""
@{manager_name}_bp.route('/{method_name.lower()}', methods=['POST'])
async def {method_name.lower()}():
    try:
        data = request.get_json()
        service_manager = EngineServiceManager()
        params = data if data else {{}}  
        method_result = await service_manager.{method_name}(**params)
        return process_method_result(method_result, deserialization_class={deserialization_class})
    except Exception as e:
        return jsonify({{"error": str(e)}}), 500
"""

    return f"""{imports_code}
{manager_name}_bp = Blueprint('{manager_name}', __name__)

from proxy.app.parser.services.{manager_name}service import {type(manager).__name__}

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api"))
sys.path.append(base_path)
from common import process_method_result

{methods_code}
"""


def generate_socketio_code(manager_name, manager):
    handlers_code = ""

    for event_name in dir(manager):
        if callable(getattr(manager, event_name)) and not event_name.startswith("_") and "callback" in event_name:
            words = event_name.split('_')
            first_word = words[1]
            handlers_code += f"""
    @socketio.on('{first_word}', namespace=namespace)
    def {event_name}(message):
        try:
            manager = {type(manager).__name__}()
            response = manager.get_{first_word}()
            emit('{first_word}', {{'event_name': '{event_name}', 'response': response}})
        except Exception as e:
            emit('event_error', {{'error': str(e)}})
"""

    return f"""
from flask_socketio import emit
from proxy.app.parser.services.{manager_name}service import {type(manager).__name__}

namespace = '/{manager_name}'

def register_socketio_handlers(socketio):
    @socketio.on('connect', namespace=namespace)
    def connect():
        emit('connected', {{"message": "Connected to {manager_name} namespace"}})

    @socketio.on('disconnect', namespace=namespace)
    def disconnect():
        print("Client disconnected from {manager_name} namespace")

    {handlers_code}
"""


def write_code_to_files(manager_name, blueprint_code, socketio_code):
    manager_dir = create_api_directory(manager_name)

    blueprint_file = os.path.join(manager_dir, "blueprint.py")
    with open(blueprint_file, "w") as f:
        f.write(blueprint_code)

    socketio_file = os.path.join(manager_dir, "socketio.py")
    with open(socketio_file, "w") as f:
        f.write(socketio_code)


def generate_service_code(manager_name, manager):
    blueprint_code = generate_blueprint_code(manager_name, manager)
    socketio_code = generate_socketio_code(manager_name, manager)
    write_code_to_files(manager_name, blueprint_code, socketio_code)


if __name__ == "__main__":
    manager = EngineServiceManager()
    generate_service_code("engine", manager)
