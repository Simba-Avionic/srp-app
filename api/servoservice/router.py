
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from proxy.app.dataclasses.servoservice_dataclass import (ReadMainServoValueOut, SetMainServoValueOut, ReadVentServoValueOut, SetVentServoValueOut)
from proxy.app.services.servoservice import ServoServiceManager
from api.common import process_method_result

router = APIRouter(
    prefix="/servoservice",
    tags=["servoservice"]
)


@router.post("/readmainservovalue")
async def readmainservovalue(data: dict = Body(...)):
    try:
        service_manager = ServoServiceManager()
        params = data or {}
        method_result = await service_manager.ReadMainServoValue(**params)
        return process_method_result(method_result, deserialization_class=ReadMainServoValueOut)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/readventservovalue")
async def readventservovalue(data: dict = Body(...)):
    try:
        service_manager = ServoServiceManager()
        params = data or {}
        method_result = await service_manager.ReadVentServoValue(**params)
        return process_method_result(method_result, deserialization_class=ReadVentServoValueOut)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/setmainservovalue")
async def setmainservovalue(data: dict = Body(...)):
    try:
        service_manager = ServoServiceManager()
        params = data or {}
        method_result = await service_manager.SetMainServoValue(**params)
        return process_method_result(method_result, deserialization_class=SetMainServoValueOut)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/setventservovalue")
async def setventservovalue(data: dict = Body(...)):
    try:
        service_manager = ServoServiceManager()
        params = data or {}
        method_result = await service_manager.SetVentServoValue(**params)
        return process_method_result(method_result, deserialization_class=SetVentServoValueOut)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
