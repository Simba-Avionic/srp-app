import logging
import asyncio
from contextlib import asynccontextmanager
import sys
import os
from loguru import logger as loguru_logger

# Dodaj folder nadrzędny do ścieżki
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from socketio import AsyncServer
from socketio import ASGIApp
from someipy.logging import set_someipy_log_level
from fastapi.middleware.cors import CORSMiddleware

# Configure Loguru rotating, compressed file logs (INFO+)
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "logs"), exist_ok=True)
logs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "app_{time}.log"))
loguru_logger.remove()
loguru_logger.add(
    logs_path,
    rotation="2 GB",
    compression="zip",
    level="ERROR",
    enqueue=True,
    backtrace=True,
    diagnose=False
)

# Bridge std logging (our modules) to Loguru
class _LoguruHandler(logging.Handler):
    def emit(self, record):
        try:
            level = record.levelname
            log = loguru_logger.bind(logger_name=record.name)
            log.log(level, record.getMessage())
        except Exception:
            pass

root_logger = logging.getLogger()
root_logger.handlers = [ _LoguruHandler() ]
root_logger.setLevel(logging.INFO)

# Quiet down verbose third-party loggers and pass them explicitly to AsyncServer
socketio_logger = logging.getLogger("socketio")
socketio_logger.setLevel(logging.WARNING)
engineio_logger = logging.getLogger("engineio")
engineio_logger.setLevel(logging.WARNING)

# Set someipy loggers to INFO (suppress DEBUG spam)
for _name in [
    "someipy",
    "someipy.client_service_instance",
    "someipy.service_discovery",
    "someipy.server_service_instance",
]:
    logging.getLogger(_name).setLevel(logging.INFO)

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
from api.fileloggerapp.socketio import register_fileloggerapp_socketio
from proxy.app.services.fileloggerapp import initialize_fileloggerapp

# servo
from api.servoservice.router import router as servo_router
from api.servoservice.socketio import register_servoservice_socketio
from proxy.app.services.servoservice import initialize_servoservice

#primerservice
from api.primerservice.router import router as primer_router
from api.primerservice.socketio import register_primerservice_socketio
from proxy.app.services.primerservice import initialize_primerservice

#sysstatservice
from api.sysstatservice.socketio import register_sysstatservice_socketio
from proxy.app.services.sysstatservice import initialize_sysstatservice

#envappfc
from api.envappfc.socketio import register_envappfc_socketio
from proxy.app.services.envappfc import initialize_envappfc

#recoveryservice
from api.recoveryservice.router import router as recovery_router
from api.recoveryservice.socketio import register_recoveryservice_socketio
from proxy.app.services.recoveryservice import initialize_recoveryservice

#gpsservice
from api.gpsservice.socketio import register_gpsservice_socketio
from proxy.app.services.gpsservice import initialize_gpsservice

#fcsysstatservice
from api.fcsysstatservice.socketio import register_fcsysstatservice_socketio
from proxy.app.services.fcsysstatservice import initialize_fcsysstatservice

# mainservice
from api.mainservice.socketio import register_mainservice_socketio
from api.mainservice.router import router as mainservice_router
from proxy.app.services.mainservice import initialize_mainservice

# fcfilelogger
from api.fcfileloggerapp.socketio import register_fcfileloggerapp_socketio
from api.fcfileloggerapp.router import router as fcfilelogger_router
from proxy.app.services.fcfileloggerapp import initialize_fcfileloggerapp


sio = AsyncServer(
    async_mode='asgi',
    logger=socketio_logger,
    engineio_logger=engineio_logger,
    cors_allowed_origins="*"
)
app = FastAPI()

# CORS for REST and preflight (dev: allow all; tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
asgi_app = ASGIApp(sio, other_asgi_app=app)


# Register routes and Socket.IO handlers
app.include_router(engine_router)
app.include_router(save_router)
app.include_router(servo_router)
app.include_router(filelogger_router)
app.include_router(primer_router)
app.include_router(recovery_router)
app.include_router(mainservice_router)
app.include_router(fcfilelogger_router)

register_servoservice_socketio(sio)
register_engineservice_socketio(sio)
register_envapp_socketio(sio)
register_primerservice_socketio(sio)
register_sysstatservice_socketio(sio)
register_envappfc_socketio(sio)
register_recoveryservice_socketio(sio)
register_gpsservice_socketio(sio)
register_fileloggerapp_socketio(sio)
register_fcsysstatservice_socketio(sio)
register_mainservice_socketio(sio)
register_fcfileloggerapp_socketio(sio)

@app.middleware("http")
async def log_requests(request, call_next):
    from time import perf_counter
    start = perf_counter()
    response = await call_next(request)
    duration_ms = (perf_counter() - start) * 1000
    # Use std logging which is bridged to loguru
    logging.getLogger("api.request").info(
        "%s %s -> %s in %.2f ms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms
    )
    return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async application lifespan management"""
    global sd_instance

    sd_instance = await initialize_service_discovery()
    set_someipy_log_level(logging.INFO)

    engine_task = asyncio.create_task(run_engine_service_manager(sd_instance))
    env_task = asyncio.create_task(run_env_service_manager(sd_instance))
    servo_task = asyncio.create_task(run_servo_service_manager(sd_instance))
    filelogger_task = asyncio.create_task(run_fileloggerapp_manager(sd_instance))
    primer_task = asyncio.create_task(run_primerservice_manager(sd_instance))
    sysstat_task = asyncio.create_task(run_sysstatservice_manager(sd_instance))
    envappfc_task = asyncio.create_task(run_envappfc_manager(sd_instance))
    recovery_task = asyncio.create_task(run_recoveryservice_manager(sd_instance))
    gps_task = asyncio.create_task(run_gpsservice_manager(sd_instance))
    mainserivce_task = asyncio.create_task(run_mainservice_manager(sd_instance))
    fcservice_task = asyncio.create_task(run_fcsysstatservice_manager(sd_instance))
    fcfilelogger_task = asyncio.create_task(run_fcsysstatservice_manager(sd_instance))


    yield

    # graceful shutdown
    for t in (engine_task, env_task, servo_task, filelogger_task, primer_task, sysstat_task, envappfc_task, gps_task, recovery_task, mainserivce_task, fcservice_task):
        t.cancel()
    for t in (engine_task, env_task, servo_task, filelogger_task, primer_task, sysstat_task, envappfc_task, gps_task, recovery_task, mainserivce_task, fcservice_task):
        try:
            await t
        except asyncio.CancelledError:
            pass

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

async def run_primerservice_manager(sd):
    await initialize_primerservice(sd)

async def run_sysstatservice_manager(sd):
    await initialize_sysstatservice(sd)

async def run_envappfc_manager(sd):
    await initialize_envappfc(sd)

async def run_recoveryservice_manager(sd):
    await initialize_recoveryservice(sd)

async def run_gpsservice_manager(sd):
    await initialize_gpsservice(sd)

async def run_mainservice_manager(sd):
    await initialize_mainservice(sd)

async def run_fcsysstatservice_manager(sd):
    await initialize_fcsysstatservice(sd)

async def fc_fileloggerservice_manager(sd):
    await initialize_fcfileloggerapp(sd)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        asgi_app,
        host="0.0.0.0",
        port=5000,
        log_level="debug",
        loop="asyncio"
    )