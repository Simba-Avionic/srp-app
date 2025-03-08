
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from proxy.app.dataclasses.engineservice_dataclass import (SetModeOut, StartOut)
from proxy.app.services.engineservice import EngineServiceManager
from api.common import process_method_result

router = APIRouter(
    prefix="/engine",
    tags=["engine"]
)


@router.post("/setmode")
async def setmode(data: dict = Body(...)):
    try:
        service_manager = EngineServiceManager()
        params = data or {}
        method_result = await service_manager.SetMode(**params)
        return process_method_result(method_result, deserialization_class=SetModeOut)
    except Exception as e:
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
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
