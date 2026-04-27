
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from proxy.app.dataclasses.envapp_dataclass import (GetLowerTankTempOut, GetUpperTankTempOut, GetTankPressureOut)
from proxy.app.services.envapp import EnvAppManager
from api.common import process_method_result

router = APIRouter(
    prefix="/envapp",
    tags=["envapp"]
)


@router.post("/getlowertanktemp")
async def getlowertanktemp(data: dict = Body(...)):
    try:
        service_manager = EnvAppManager()
        params = data or {}
        method_result = await service_manager.GetLowerTankTemp(**params)
        return process_method_result(method_result, deserialization_class=GetLowerTankTempOut)
    except Exception as e:
        logger.exception("Error in getlowertanktemp handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/gettankpressure")
async def gettankpressure(data: dict = Body(...)):
    try:
        service_manager = EnvAppManager()
        params = data or {}
        method_result = await service_manager.GetTankPressure(**params)
        return process_method_result(method_result, deserialization_class=GetTankPressureOut)
    except Exception as e:
        logger.exception("Error in gettankpressure handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/getuppertanktemp")
async def getuppertanktemp(data: dict = Body(...)):
    try:
        service_manager = EnvAppManager()
        params = data or {}
        method_result = await service_manager.GetUpperTankTemp(**params)
        return process_method_result(method_result, deserialization_class=GetUpperTankTempOut)
    except Exception as e:
        logger.exception("Error in getuppertanktemp handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
