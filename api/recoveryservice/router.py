
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from proxy.app.dataclasses.recoveryservice_dataclass import (UnreefeParachuteOut, OpenReefedParachuteOut)
from proxy.app.services.recoveryservice import RecoveryServiceManager
from api.common import process_method_result

router = APIRouter(
    prefix="/recoveryservice",
    tags=["recoveryservice"]
)


@router.post("/openreefedparachute")
async def openreefedparachute(data: dict = Body(...)):
    try:
        service_manager = RecoveryServiceManager()
        params = data or {}
        method_result = await service_manager.OpenReefedParachute(**params)
        return process_method_result(method_result, deserialization_class=OpenReefedParachuteOut)
    except Exception as e:
        logger.exception("Error in openreefedparachute handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/unreefeparachute")
async def unreefeparachute(data: dict = Body(...)):
    try:
        service_manager = RecoveryServiceManager()
        params = data or {}
        method_result = await service_manager.UnreefeParachute(**params)
        return process_method_result(method_result, deserialization_class=UnreefeParachuteOut)
    except Exception as e:
        logger.exception("Error in unreefeparachute handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
