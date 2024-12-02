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

    for method_name in dir(manager):
        method = getattr(manager, method_name)
        if callable(method) and method_name[0].isupper():
            methods_code += f"""
@{manager_name}_bp.route('/{method_name}', methods=['POST'])
def {method_name}():
    data = request.json
    return jsonify({{"result": result}})
"""

    return f"""
from flask import Blueprint, jsonify, request
import asyncio

{manager_name}_bp = Blueprint('{manager_name}', __name__)
from proxy.app.parser.services.engineservice import EngineServiceManager as manager

{methods_code}
"""


def generate_socketio_code(manager_name, manager):
    handlers_code = ""
    for event_name in dir(manager):
        if callable(getattr(manager, event_name)) and not event_name.startswith("_") and "callback" in event_name:
            handlers_code += f"""
@socketio.on('{event_name}', namespace=namespace)
def {event_name}(message):
    try:
        response = manager.{event_name}(message)
        emit('event_response', {{"event_name": '{event_name}', "response": response}})
    except Exception as e:
        emit('event_error', {{"error": str(e)}})
"""

    return f"""
import socketio
from flask_socketio import emit
from proxy.app.parser.services.engineservice import EngineServiceManager as manager

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
