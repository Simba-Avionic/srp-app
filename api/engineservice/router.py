
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from proxy.app.dataclasses.engineservice_dataclass import (SetVentValveOut, SetModeOut, StartOut, GetModeOut)
from proxy.app.services.engineservice import EngineServiceManager
from api.common import process_method_result

router = APIRouter(
    prefix="/engineservice",
    tags=["engineservice"]
)


@router.post("/getmode")
async def getmode(data: dict = Body(...)):
    try:
        service_manager = EngineServiceManager()
        params = data or {}
        method_result = await service_manager.GetMode(**params)
        return process_method_result(method_result, deserialization_class=GetModeOut)
    except Exception as e:
        logger.exception("Error in getmode handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/setmode")
async def setmode(data: dict = Body(...)):
    try:
        service_manager = EngineServiceManager()
        params = data or {}
        method_result = await service_manager.SetMode(**params)
        return process_method_result(method_result, deserialization_class=SetModeOut)
    except Exception as e:
        logger.exception("Error in setmode handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/setventvalve")
async def setventvalve(data: dict = Body(...)):
    try:
        service_manager = EngineServiceManager()
        params = data or {}
        method_result = await service_manager.SetVentValve(**params)
        return process_method_result(method_result, deserialization_class=SetVentValveOut)
    except Exception as e:
        logger.exception("Error in setventvalve handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/start")
async def start(data: dict = Body(...)):
    try:
        service_manager = EngineServiceManager()
        params = data or {}
        method_result = await service_manager.Start(**params)
        return process_method_result(method_result, deserialization_class=StartOut)
    except Exception as e:
        logger.exception("Error in start handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
