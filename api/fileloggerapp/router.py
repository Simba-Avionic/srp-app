
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from proxy.app.dataclasses.fileloggerapp_dataclass import (StopOut, StartOut)
from proxy.app.services.fileloggerapp import FileLoggerAppManager
from api.common import process_method_result

router = APIRouter(
    prefix="/fileloggerapp",
    tags=["fileloggerapp"]
)


@router.post("/start")
async def start(data: dict = Body(...)):
    try:
        service_manager = FileLoggerAppManager()
        params = data or {}
        method_result = await service_manager.Start(**params)
        return process_method_result(method_result, deserialization_class=StartOut)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/stop")
async def stop(data: dict = Body(...)):
    try:
        service_manager = FileLoggerAppManager()
        params = data or {}
        method_result = await service_manager.Stop(**params)
        return process_method_result(method_result, deserialization_class=StopOut)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
