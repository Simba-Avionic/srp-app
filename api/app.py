import logging
import asyncio
from contextlib import asynccontextmanager
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from socketio import AsyncServer
from socketio import ASGIApp
from someipy.logging import set_someipy_log_level
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger as loguru_logger

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

class _LoguruHandler(logging.Handler):
    def emit(self, record):
        try:
            level = record.levelname
            log = loguru_logger.bind(logger_name=record.name)
            log.log(level, record.getMessage())
        except Exception:
            pass

root_logger = logging.getLogger()
root_logger.handlers = [_LoguruHandler()]
root_logger.setLevel(logging.INFO)

socketio_logger = logging.getLogger("socketio")
socketio_logger.setLevel(logging.WARNING)
engineio_logger = logging.getLogger("engineio")
engineio_logger.setLevel(logging.WARNING)

for _name in ["someipy", "someipy.client_service_instance", "someipy.service_discovery", "someipy.server_service_instance"]:
    logging.getLogger(_name).setLevel(logging.INFO)

from proxy.app.services.service_discovery import initialize_service_discovery
from api.save_to_file.router import save_router

# engine
from api.engineservice.router import router as engineservice_router
from api.engineservice.socketio import register_engineservice_socketio
from proxy.app.services.engineservice import initialize_engineservice

# env (oxidizer EC)
from api.envapp.socketio import register_envapp_socketio
from proxy.app.services.envapp import initialize_envapp

# env (sec EC)
from api.secenvapp.socketio import register_secenvapp_socketio
from proxy.app.services.secenvapp import initialize_secenvapp

# sys stat (oxidizer EC)
from api.sysstatservice.socketio import register_sysstatservice_socketio
from proxy.app.services.sysstatservice import initialize_sysstatservice

# file logger (oxidizer EC)
from api.fileloggerapp.router import router as fileloggerapp_router
from api.fileloggerapp.socketio import register_fileloggerapp_socketio
from proxy.app.services.fileloggerapp import initialize_fileloggerapp

# primer
from api.primerservice.router import router as primerservice_router
from api.primerservice.socketio import register_primerservice_socketio
from proxy.app.services.primerservice import initialize_primerservice

# servo (oxidizer EC)
from api.servoservice.router import router as servoservice_router
from api.servoservice.socketio import register_servoservice_socketio
from proxy.app.services.servoservice import initialize_servoservice

# servo (sec EC)
from api.secservoservice.router import router as secservoservice_router
from api.secservoservice.socketio import register_secservoservice_socketio
from proxy.app.services.secservoservice import initialize_secservoservice

# fc radio (old)
from api.fcradioservice.socketio import register_fcradioservice_socketio
from proxy.app.services.fcradioservice import initialize_fcradioservice

# fc radio
from api.radioservice.socketio import register_radioservice_socketio
from proxy.app.services.radioservice import initialize_radioservice

# fc env
from api.envappfc.socketio import register_envappfc_socketio
from proxy.app.services.envappfc import initialize_envappfc

# fc sys stat
from api.fcsysstatservice.socketio import register_fcsysstatservice_socketio
from proxy.app.services.fcsysstatservice import initialize_fcsysstatservice

# fc file logger
from api.fcfileloggerapp.router import router as fcfileloggerapp_router
from api.fcfileloggerapp.socketio import register_fcfileloggerapp_socketio
from proxy.app.services.fcfileloggerapp import initialize_fcfileloggerapp

# fc gps
from api.gpsservice.socketio import register_gpsservice_socketio
from proxy.app.services.gpsservice import initialize_gpsservice

# fc main
from api.mainservice.router import router as mainservice_router
from api.mainservice.socketio import register_mainservice_socketio
from proxy.app.services.mainservice import initialize_mainservice

# fc recovery
from api.recoveryservice.router import router as recoveryservice_router
from api.recoveryservice.socketio import register_recoveryservice_socketio
from proxy.app.services.recoveryservice import initialize_recoveryservice

# fc apogee detect
from api.apogeedetectservice.socketio import register_apogeedetectservice_socketio
from proxy.app.services.apogeedetectservice import initialize_apogeedetectservice


sio = AsyncServer(
    async_mode='asgi',
    logger=socketio_logger,
    engineio_logger=engineio_logger,
    cors_allowed_origins="*"
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
asgi_app = ASGIApp(sio, other_asgi_app=app)

# Routers
app.include_router(save_router)
app.include_router(engineservice_router)
app.include_router(fileloggerapp_router)
app.include_router(primerservice_router)
app.include_router(servoservice_router)
app.include_router(secservoservice_router)
app.include_router(fcfileloggerapp_router)
app.include_router(mainservice_router)
app.include_router(recoveryservice_router)

# Socket.IO namespaces
register_engineservice_socketio(sio)
register_envapp_socketio(sio)
register_secenvapp_socketio(sio)
register_sysstatservice_socketio(sio)
register_fileloggerapp_socketio(sio)
register_primerservice_socketio(sio)
register_servoservice_socketio(sio)
register_secservoservice_socketio(sio)
register_fcradioservice_socketio(sio)
register_radioservice_socketio(sio)
register_envappfc_socketio(sio)
register_fcsysstatservice_socketio(sio)
register_fcfileloggerapp_socketio(sio)
register_gpsservice_socketio(sio)
register_mainservice_socketio(sio)
register_recoveryservice_socketio(sio)
register_apogeedetectservice_socketio(sio)


@app.middleware("http")
async def log_requests(request, call_next):
    from time import perf_counter
    start = perf_counter()
    response = await call_next(request)
    duration_ms = (perf_counter() - start) * 1000
    logging.getLogger("api.request").info(
        "%s %s -> %s in %.2f ms",
        request.method, request.url.path, response.status_code, duration_ms
    )
    return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    global sd_instance
    sd_instance = await initialize_service_discovery()
    set_someipy_log_level(logging.INFO)

    engine_task        = asyncio.create_task(run_engineservice(sd_instance))
    envapp_task        = asyncio.create_task(run_envapp(sd_instance))
    secenvapp_task     = asyncio.create_task(run_secenvapp(sd_instance))
    sysstat_task       = asyncio.create_task(run_sysstatservice(sd_instance))
    filelogger_task    = asyncio.create_task(run_fileloggerapp(sd_instance))
    primer_task        = asyncio.create_task(run_primerservice(sd_instance))
    servo_task         = asyncio.create_task(run_servoservice(sd_instance))
    secservo_task      = asyncio.create_task(run_secservoservice(sd_instance))
    fcradio_task       = asyncio.create_task(run_fcradioservice(sd_instance))
    radio_task         = asyncio.create_task(run_radioservice(sd_instance))
    envappfc_task      = asyncio.create_task(run_envappfc(sd_instance))
    fcsysstat_task     = asyncio.create_task(run_fcsysstatservice(sd_instance))
    fcfilelogger_task  = asyncio.create_task(run_fcfileloggerapp(sd_instance))
    gps_task           = asyncio.create_task(run_gpsservice(sd_instance))
    main_task          = asyncio.create_task(run_mainservice(sd_instance))
    recovery_task      = asyncio.create_task(run_recoveryservice(sd_instance))
    apogee_task        = asyncio.create_task(run_apogeedetectservice(sd_instance))

    yield

    all_tasks = (
        engine_task, envapp_task, secenvapp_task, sysstat_task,
        filelogger_task, primer_task, servo_task, secservo_task,
        fcradio_task, radio_task, envappfc_task, fcsysstat_task,
        fcfilelogger_task, gps_task, main_task, recovery_task, apogee_task,
    )
    for t in all_tasks:
        t.cancel()
    for t in all_tasks:
        try:
            await t
        except asyncio.CancelledError:
            pass

    await sd_instance.shutdown()


app.router.lifespan_context = lifespan


async def run_engineservice(sd):        await initialize_engineservice(sd)
async def run_envapp(sd):               await initialize_envapp(sd)
async def run_secenvapp(sd):            await initialize_secenvapp(sd)
async def run_sysstatservice(sd):       await initialize_sysstatservice(sd)
async def run_fileloggerapp(sd):        await initialize_fileloggerapp(sd)
async def run_primerservice(sd):        await initialize_primerservice(sd)
async def run_servoservice(sd):         await initialize_servoservice(sd)
async def run_secservoservice(sd):      await initialize_secservoservice(sd)
async def run_fcradioservice(sd):       await initialize_fcradioservice(sd)
async def run_radioservice(sd):         await initialize_radioservice(sd)
async def run_envappfc(sd):             await initialize_envappfc(sd)
async def run_fcsysstatservice(sd):     await initialize_fcsysstatservice(sd)
async def run_fcfileloggerapp(sd):      await initialize_fcfileloggerapp(sd)
async def run_gpsservice(sd):           await initialize_gpsservice(sd)
async def run_mainservice(sd):          await initialize_mainservice(sd)
async def run_recoveryservice(sd):      await initialize_recoveryservice(sd)
async def run_apogeedetectservice(sd):  await initialize_apogeedetectservice(sd)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(asgi_app, host="0.0.0.0", port=5000, log_level="debug", loop="asyncio")
