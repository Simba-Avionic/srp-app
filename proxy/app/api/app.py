import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from socketio import AsyncServer
from socketio import ASGIApp
from someipy.logging import set_someipy_log_level

from proxy.app.api.engine.socketio import register_engine_socketio
from proxy.app.api.env.socketio import register_env_socketio
from proxy.app.api.engine.router import router as engine_router
from proxy.app.api.save_to_file.router import save_router
from proxy.app.parser.services.engineservice import initialize_engineservice
from proxy.app.parser.services.envservice import initialize_envservice
from proxy.app.parser.services.service_discovery import initialize_service_discovery

sio = AsyncServer(async_mode='asgi', logger=True, engineio_logger=True)
app = FastAPI()
asgi_app = ASGIApp(sio, other_asgi_app=app)


# Register routes and Socket.IO handlers
app.include_router(engine_router)
app.include_router(save_router)
register_engine_socketio(sio)
register_env_socketio(sio)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async application lifespan management"""
    global sd_instance

    sd_instance = await initialize_service_discovery()
    set_someipy_log_level(logging.DEBUG)

    asyncio.create_task(run_engine_service_manager(sd_instance))
    asyncio.create_task(run_env_service_manager(sd_instance))

    yield

    await sd_instance.shutdown()


app.router.lifespan_context = lifespan


async def run_engine_service_manager(sd):
    await initialize_engineservice(sd)


async def run_env_service_manager(sd):
    await initialize_envservice(sd)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        asgi_app,
        host="0.0.0.0",
        port=5000,
        log_level="debug",
        loop="asyncio"
    )