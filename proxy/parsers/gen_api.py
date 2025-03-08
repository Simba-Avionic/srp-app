import os

from proxy.app.services.engineservice import EngineServiceManager
from proxy.app.services.envapp import EnvAppManager
from proxy.app.services.servoservice import ServoServiceManager
from proxy.app.services.fileloggerapp import FileLoggerAppManager

API_BASE_DIR = os.path.join(os.path.dirname(__file__), "../../api")


def create_api_directory(manager_name):
    manager_dir = os.path.join(API_BASE_DIR, manager_name)
    os.makedirs(manager_dir, exist_ok=True)

    init_file = os.path.join(manager_dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write(f"# Package for {manager_name} API\n")

    return manager_dir


def generate_router_code(manager_name, manager):
    valid_methods = []
    for method_name in dir(manager):
        method = getattr(manager, method_name)
        if callable(method) and method_name[0].isupper():
            valid_methods.append(method_name)

    if not valid_methods:
        return ""

    deserialization_classes = {f"{method}Out" for method in valid_methods}

    imports_code = f"""
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from proxy.app.dataclasses.{manager_name}_dataclass import ("""

    if deserialization_classes:
        imports_code += ", ".join(deserialization_classes) + ")\n"
    else:
        imports_code = ""

    imports_code += f"from proxy.app.services.{manager_name} import {type(manager).__name__}\n"
    imports_code += "from api.common import process_method_result\n\n"

    methods_code = ""
    for method_name in valid_methods:
        deserialization_class = f"{method_name}Out"
        methods_code += f"""
@router.post("/{method_name.lower()}")
async def {method_name.lower()}(data: dict = Body(...)):
    try:
        service_manager = {type(manager).__name__}()
        params = data or {{}}
        method_result = await service_manager.{method_name}(**params)
        return process_method_result(method_result, deserialization_class={deserialization_class})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={{"error": str(e)}}
        )
"""

    router_code = (
        f"{imports_code}"
        f"router = APIRouter(\n"
        f"    prefix=\"/{manager_name}\",\n"
        f"    tags=[\"{manager_name}\"]\n"
        f")\n\n"
        f"{methods_code}"
    )
    return router_code


def generate_socketio_code(manager_name, manager):
    handlers_code = ""

    for method_name in dir(manager):
        if callable(getattr(manager, method_name)) and method_name.startswith("get"):
            event_name = method_name[4:].lower()
            handlers_code += f"""
    @sio.on('{event_name}', namespace=namespace)
    async def {method_name}(sid, data):
        try:
            manager = {type(manager).__name__}()
            response = manager.{method_name}()
            await sio.emit('{event_name}', 
                          {{'event_name': '{event_name}', 'response': response}},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {{'error': str(e)}},
                          room=sid,
                          namespace=namespace)
    """

    return f"""
from socketio import AsyncServer
from proxy.app.services.{manager_name} import {type(manager).__name__}

namespace = '/{manager_name}'

def register_{manager_name}_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {{"message": "Connected to {manager_name} namespace"}},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        print(f"Client {{sid}} disconnected from {manager_name} namespace")

    {handlers_code}
"""


def write_code_to_files(manager_name, router_code, socketio_code):
    manager_dir = create_api_directory(manager_name)

    router_file = os.path.join(manager_dir, "router.py")
    with open(router_file, "w") as f:
        f.write(router_code)

    socketio_file = os.path.join(manager_dir, "socketio.py")
    with open(socketio_file, "w") as f:
        f.write(socketio_code)


def generate_service_code(manager):
    manager_name = type(manager).__name__.replace("Manager", "").lower()
    router_code = generate_router_code(manager_name, manager)
    socketio_code = generate_socketio_code(manager_name, manager)
    write_code_to_files(manager_name, router_code, socketio_code)


if __name__ == "__main__":
    manager = FileLoggerAppManager()
    generate_service_code(manager)