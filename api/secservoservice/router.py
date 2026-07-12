
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from proxy.app.dataclasses.secservoservice_dataclass import (SetEtanolMainValveOut, SetEthanolVentValveOut)
from proxy.app.services.secservoservice import SecServoServiceManager
from api.common import process_method_result

router = APIRouter(
    prefix="/secservoservice",
    tags=["secservoservice"]
)


@router.post("/setetanolmainvalve")
async def setetanolmainvalve(data: dict = Body(...)):
    try:
        service_manager = SecServoServiceManager()
        params = data or {}
        method_result = await service_manager.SetEtanolMainValve(**params)
        return process_method_result(method_result, deserialization_class=SetEtanolMainValveOut)
    except Exception as e:
        logger.exception("Error in setetanolmainvalve handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/setethanolventvalve")
async def setethanolventvalve(data: dict = Body(...)):
    try:
        service_manager = SecServoServiceManager()
        params = data or {}
        method_result = await service_manager.SetEthanolVentValve(**params)
        return process_method_result(method_result, deserialization_class=SetEthanolVentValveOut)
    except Exception as e:
        logger.exception("Error in setethanolventvalve handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
