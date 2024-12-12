import logging
import asyncio

from flask import Flask
from flask_socketio import SocketIO
from someipy.logging import set_someipy_log_level

from proxy.app.api.engine.socketio import register_socketio_handlers
from proxy.app.api.engine.blueprint import engine_bp
from proxy.app.parser.services.engineservice import initialize_engineservice
from proxy.app.parser.services.envservice import initialize_envservice
from proxy.app.parser.services.service_discovery import initialize_service_discovery


async def run_engine_service_manager(sd):
    await initialize_engineservice(sd)


async def run_env_service_manager(sd):
    await initialize_envservice(sd)


def run_flask_app():
    app = Flask(__name__)
    app.register_blueprint(engine_bp, url_prefix='/engine')
    socketio = SocketIO(app, async_mode='gevent')
    register_socketio_handlers(socketio)
    socketio.run(app, debug=True, use_reloader=False)


async def main():
    sd = await initialize_service_discovery()
    set_someipy_log_level(logging.FATAL)
    service_manager_task = asyncio.create_task(run_engine_service_manager(sd))
    service_manager_task1 = asyncio.create_task(run_env_service_manager(sd))
    flask_task = asyncio.to_thread(run_flask_app)
    await asyncio.gather(service_manager_task, service_manager_task1 , flask_task)


if __name__ == '__main__':
    asyncio.run(main())