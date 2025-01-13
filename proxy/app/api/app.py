import logging
import asyncio
from threading import Thread

from flask import Flask
from flask_socketio import SocketIO
from someipy.logging import set_someipy_log_level

from proxy.app.api.engine.socketio import register_socketio_handlers
from proxy.app.api.engine.blueprint import engine_bp
from proxy.app.parser.services.engineservice import initialize_engineservice
from proxy.app.parser.services.envservice import initialize_envservice
from proxy.app.parser.services.service_discovery import initialize_service_discovery
from gevent import monkey
monkey.patch_socket()

app = Flask(__name__)
app.register_blueprint(engine_bp, url_prefix='/engine')
socketio = SocketIO(app, async_mode='gevent', message_queue="redis://")
register_socketio_handlers(socketio)

async def run_engine_service_manager(sd):
    await initialize_engineservice(sd)


async def run_env_service_manager(sd):
    await initialize_envservice(sd)


def run_flask_app():
    socketio.run(app, debug=True, use_reloader=False)


async def main():
    sd = await initialize_service_discovery()
    set_someipy_log_level(logging.DEBUG)

    flask_thread = Thread(target=run_flask_app, daemon=True)
    flask_thread.start()

    service_manager_task = asyncio.create_task(run_engine_service_manager(sd))
    service_manager_task1 = asyncio.create_task(run_env_service_manager(sd))

    await asyncio.gather(service_manager_task, service_manager_task1)


if __name__ == '__main__':
    asyncio.run(main())