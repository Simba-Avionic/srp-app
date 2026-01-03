
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from proxy.app.dataclasses.envapp_dataclass import (CalPressureSensorOut)
from proxy.app.services.envapp import EnvAppManager
from api.common import process_method_result

router = APIRouter(
    prefix="/envapp",
    tags=["envapp"]
)


@router.post("/calpressuresensor")
async def calpressuresensor(data: dict = Body(...)):
    try:
        service_manager = EnvAppManager()
        params = data or {}
        method_result = await service_manager.CalPressureSensor(**params)
        return process_method_result(method_result, deserialization_class=CalPressureSensorOut)
    except Exception as e:
        logger.exception("Error in calpressuresensor handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
