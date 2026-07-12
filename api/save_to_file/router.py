import csv
import asyncio
import os
from typing import Callable
from loguru import logger

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime

from proxy.app.services.engineservice import EngineServiceManager
from proxy.app.services.envapp import EnvAppManager
from proxy.app.services.secenvapp import SecEnvAppManager
from proxy.app.services.servoservice import ServoServiceManager
from proxy.app.services.secservoservice import SecServoServiceManager
from proxy.app.services.sysstatservice import SysStatServiceManager
from proxy.app.services.envappfc import EnvAppFcManager
from proxy.app.services.recoveryservice import RecoveryServiceManager
from proxy.app.services.gpsservice import GPSServiceManager
from proxy.app.services.primerservice import PrimerServiceManager
from proxy.app.services.fcsysstatservice import FcSysStatServiceManager
from proxy.app.services.mainservice import MainServiceManager
from proxy.app.services.fcfileloggerapp import FcFileLoggerAppManager

current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_file_dir))
csv_dir = os.path.join(project_root, 'desktop', 'data', 'csv')
csv_filename = os.path.join(csv_dir, 'data.csv')

os.makedirs(csv_dir, exist_ok=True)

logger.info(f"CSV file will be saved to: {csv_filename}")

csv_lock = asyncio.Lock()

managers = [
    FcFileLoggerAppManager(),
    EngineServiceManager(),
    EnvAppManager(),
    SecEnvAppManager(),
    ServoServiceManager(),
    SecServoServiceManager(),
    SysStatServiceManager(),
    EnvAppFcManager(),
    RecoveryServiceManager(),
    GPSServiceManager(),
    PrimerServiceManager(),
    FcSysStatServiceManager(),
    MainServiceManager(),
]

save_task = None
collect_data_flag = False
first_write = True

# (column_name, getter) — unikalne nazwy kolumn, ta sama kolejność przy zapisie
_data_columns: list[tuple[str, Callable[[], object]]] = []


def _build_data_columns() -> list[tuple[str, Callable[[], object]]]:
    columns: list[tuple[str, Callable[[], object]]] = []
    for manager in managers:
        manager_name = type(manager).__name__.replace("Manager", "").lower()
        for method_name in sorted(dir(manager)):
            if not method_name.startswith("get"):
                continue
            method = getattr(manager, method_name, None)
            if not callable(method):
                continue
            event_name = method_name[4:].lower()
            column_name = f"{manager_name}_{event_name}"
            columns.append((column_name, method))
    return columns


_data_columns = _build_data_columns()
header = ['timestamp'] + [name for name, _ in _data_columns]


def _format_value(value) -> str:
    if value is None:
        return ''
    return str(value)


def _collect_row() -> list[str]:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    row = [timestamp]
    for _, getter in _data_columns:
        try:
            row.append(_format_value(getter()))
        except Exception as e:
            logger.exception("Error reading value from {}: {}", getter, e)
            row.append('')
    return row


async def write_row_to_csv(row, is_header=False):
    global first_write
    try:
        async with csv_lock:
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if is_header and first_write:
                    writer.writerow(header)
                    logger.info(f"Wrote CSV header with {len(header)} columns")
                    first_write = False
                elif not is_header:
                    writer.writerow(row)
                file.flush()
                os.fsync(file.fileno())
    except Exception as e:
        logger.exception("Error writing to CSV file '{}': {}", csv_filename, e)
        raise


async def save_to_csv(data_generator):
    global collect_data_flag, first_write
    row_count = 0

    try:
        logger.info(f"Starting to save data to CSV file: {csv_filename}")
        if first_write:
            await write_row_to_csv(None, is_header=True)

        async for row in data_generator:
            if not collect_data_flag:
                logger.info("collect_data_flag is False, stopping save loop")
                break
            await write_row_to_csv(row)
            row_count += 1
            if row_count % 100 == 0:
                non_empty = sum(1 for cell in row[1:] if cell != '')
                logger.info(f"Saved {row_count} rows (last row non-empty fields: {non_empty})")

        logger.info(f"Finished saving. Total rows saved: {row_count}")
    except Exception as e:
        logger.exception("Error in save_to_csv: {}", e)
    finally:
        collect_data_flag = False
        logger.info("Save task finished, collect_data_flag reset to False")


async def collect_manager_data():
    logger.info("Starting data collection loop")
    row_count = 0
    while collect_data_flag:
        row = _collect_row()
        row_count += 1
        if row_count % 100 == 0:
            non_empty = sum(1 for cell in row[1:] if cell != '')
            logger.debug(f"Collected {row_count} rows (non-empty fields: {non_empty})")
        yield row
        await asyncio.sleep(0.1)

    logger.info(f"Stopped data collection. Total rows collected: {row_count}")


save_router = APIRouter(prefix="/save", tags=["save"])


@save_router.post("/start")
async def start_collecting():
    global collect_data_flag, save_task, first_write

    if collect_data_flag and save_task and not save_task.done():
        return {"status": "Already collecting data", "file": csv_filename}

    if save_task and save_task.done():
        save_task = None

    collect_data_flag = True
    data_generator = collect_manager_data()
    save_task = asyncio.create_task(save_to_csv(data_generator))
    logger.info(f"Started collecting data to file: {csv_filename}")
    return {"status": "Started collecting data", "file": csv_filename}


@save_router.post("/stop")
async def stop_collecting():
    global collect_data_flag, save_task

    collect_data_flag = False

    if save_task and not save_task.done():
        try:
            await asyncio.wait_for(save_task, timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for save task to finish")
            save_task.cancel()
        except Exception as e:
            logger.exception("Error stopping save task: {}", e)

    save_task = None
    logger.info("Stopped collecting data")
    return {"status": "Stopped collecting data"}


@save_router.post("/reset")
async def reset_csv_file():
    global first_write, collect_data_flag, save_task

    if collect_data_flag:
        return {"status": "error", "message": "Stop collecting before reset"}

    if os.path.exists(csv_filename):
        os.remove(csv_filename)

    first_write = True
    logger.info("CSV file reset: {}", csv_filename)
    return {"status": "CSV file reset", "file": csv_filename}


@save_router.get("/data")
async def get_csv_data():
    if not os.path.exists(csv_filename):
        return {"rows": []}

    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return {"rows": list(reader)}


@save_router.get("/download")
async def download_csv():
    if not os.path.exists(csv_filename):
        raise HTTPException(status_code=404, detail="CSV file not found")

    return FileResponse(
        csv_filename,
        media_type="text/csv",
        filename="data.csv",
    )


@save_router.get("/status")
async def get_save_status():
    row_count = 0
    if os.path.exists(csv_filename):
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            row_count = max(0, sum(1 for _ in file) - 1)

    return {
        "collecting": collect_data_flag,
        "file": csv_filename,
        "exists": os.path.exists(csv_filename),
        "size_bytes": os.path.getsize(csv_filename) if os.path.exists(csv_filename) else 0,
        "row_count": row_count,
        "task_running": save_task is not None and not save_task.done(),
    }
