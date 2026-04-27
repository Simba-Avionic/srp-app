
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from proxy.app.dataclasses.fcfileloggerapp_dataclass import (StopOut, StartOut)
from proxy.app.services.fcfileloggerapp import FcFileLoggerAppManager
from api.common import process_method_result

router = APIRouter(
    prefix="/fcfileloggerapp",
    tags=["fcfileloggerapp"]
)


@router.post("/start")
async def start(data: dict = Body(...)):
    try:
        service_manager = FcFileLoggerAppManager()
        params = data or {}
        method_result = await service_manager.Start(**params)
        return process_method_result(method_result, deserialization_class=StartOut)
    except Exception as e:
        logger.exception("Error in start handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/stop")
async def stop(data: dict = Body(...)):
    try:
        service_manager = FcFileLoggerAppManager()
        params = data or {}
        method_result = await service_manager.Stop(**params)
        return process_method_result(method_result, deserialization_class=StopOut)
    except Exception as e:
        logger.exception("Error in stop handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
