import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from socketio import AsyncServer
from socketio import ASGIApp
from someipy.logging import set_someipy_log_level

from api.save_to_file.router import save_router
from proxy.app.services.service_discovery import initialize_service_discovery

# engine
from api.engineservice.socketio import register_engineservice_socketio
from api.engineservice.router import router as engine_router
from proxy.app.services.engineservice import initialize_engineservice

# envapp
from api.envapp.socketio import register_envapp_socketio
from proxy.app.services.envapp import initialize_envapp

# file logger
from api.fileloggerapp.router import router as filelogger_router
from proxy.app.services.fileloggerapp import initialize_fileloggerapp

# servo
from api.servoservice.router import router as servo_router
from api.servoservice.socketio import register_servoservice_socketio
from proxy.app.services.servoservice import initialize_servoservice



sio = AsyncServer(async_mode='asgi', logger=True, engineio_logger=True)
app = FastAPI()
asgi_app = ASGIApp(sio, other_asgi_app=app)


# Register routes and Socket.IO handlers
app.include_router(engine_router)
app.include_router(save_router)
app.include_router(servo_router)
app.include_router(filelogger_router)

register_servoservice_socketio(sio)
register_engineservice_socketio(sio)
register_envapp_socketio(sio)

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
    await initialize_envapp(sd)

async def run_servo_service_manager(sd):
    await initialize_servoservice(sd)

async def run_fileloggerapp_manager(sd):
    await initialize_fileloggerapp(sd)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        asgi_app,
        host="0.0.0.0",
        port=5000,
        log_level="debug",
        loop="asyncio"
    )