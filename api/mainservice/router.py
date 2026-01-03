
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from proxy.app.dataclasses.mainservice_dataclass import (SetModeOut)
from proxy.app.services.mainservice import MainServiceManager
from api.common import process_method_result

router = APIRouter(
    prefix="/mainservice",
    tags=["mainservice"]
)


@router.post("/setmode")
async def setmode(data: dict = Body(...)):
    try:
        service_manager = MainServiceManager()
        params = data or {}
        method_result = await service_manager.SetMode(**params)
        return process_method_result(method_result, deserialization_class=SetModeOut)
    except Exception as e:
        logger.exception("Error in setmode handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
