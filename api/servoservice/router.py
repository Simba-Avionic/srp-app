
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from proxy.app.dataclasses.servoservice_dataclass import (SetOxidizerVentValveOut, SetOxidizerDumpValveOut, SetOxidizerMainValveOut, SetPressureFeedVentValveOut, SetPressureFeedMainValveOut)
from proxy.app.services.servoservice import ServoServiceManager
from api.common import process_method_result

router = APIRouter(
    prefix="/servoservice",
    tags=["servoservice"]
)


@router.post("/setoxidizerdumpvalve")
async def setoxidizerdumpvalve(data: dict = Body(...)):
    try:
        service_manager = ServoServiceManager()
        params = data or {}
        method_result = await service_manager.SetOxidizerDumpValve(**params)
        return process_method_result(method_result, deserialization_class=SetOxidizerDumpValveOut)
    except Exception as e:
        logger.exception("Error in setoxidizerdumpvalve handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/setoxidizermainvalve")
async def setoxidizermainvalve(data: dict = Body(...)):
    try:
        service_manager = ServoServiceManager()
        params = data or {}
        method_result = await service_manager.SetOxidizerMainValve(**params)
        return process_method_result(method_result, deserialization_class=SetOxidizerMainValveOut)
    except Exception as e:
        logger.exception("Error in setoxidizermainvalve handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/setoxidizerventvalve")
async def setoxidizerventvalve(data: dict = Body(...)):
    try:
        service_manager = ServoServiceManager()
        params = data or {}
        method_result = await service_manager.SetOxidizerVentValve(**params)
        return process_method_result(method_result, deserialization_class=SetOxidizerVentValveOut)
    except Exception as e:
        logger.exception("Error in setoxidizerventvalve handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/setpressurefeedmainvalve")
async def setpressurefeedmainvalve(data: dict = Body(...)):
    try:
        service_manager = ServoServiceManager()
        params = data or {}
        method_result = await service_manager.SetPressureFeedMainValve(**params)
        return process_method_result(method_result, deserialization_class=SetPressureFeedMainValveOut)
    except Exception as e:
        logger.exception("Error in setpressurefeedmainvalve handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/setpressurefeedventvalve")
async def setpressurefeedventvalve(data: dict = Body(...)):
    try:
        service_manager = ServoServiceManager()
        params = data or {}
        method_result = await service_manager.SetPressureFeedVentValve(**params)
        return process_method_result(method_result, deserialization_class=SetPressureFeedVentValveOut)
    except Exception as e:
        logger.exception("Error in setpressurefeedventvalve handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
