
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from proxy.app.dataclasses.primerservice_dataclass import (StartPrimeOut, OffPrimeOut, OnPrimeOut)
from proxy.app.services.primerservice import PrimerServiceManager
from api.common import process_method_result

router = APIRouter(
    prefix="/primerservice",
    tags=["primerservice"]
)


@router.post("/offprime")
async def offprime(data: dict = Body(...)):
    try:
        service_manager = PrimerServiceManager()
        params = data or {}
        method_result = await service_manager.OffPrime(**params)
        return process_method_result(method_result, deserialization_class=OffPrimeOut)
    except Exception as e:
        logger.exception("Error in offprime handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/onprime")
async def onprime(data: dict = Body(...)):
    try:
        service_manager = PrimerServiceManager()
        params = data or {}
        method_result = await service_manager.OnPrime(**params)
        return process_method_result(method_result, deserialization_class=OnPrimeOut)
    except Exception as e:
        logger.exception("Error in onprime handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/startprime")
async def startprime(data: dict = Body(...)):
    try:
        service_manager = PrimerServiceManager()
        params = data or {}
        method_result = await service_manager.StartPrime(**params)
        return process_method_result(method_result, deserialization_class=StartPrimeOut)
    except Exception as e:
        logger.exception("Error in startprime handler: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
