import csv
import asyncio
import os
from loguru import logger

from fastapi import BackgroundTasks, APIRouter
from datetime import datetime

from proxy.app.services.engineservice import EngineServiceManager
from proxy.app.services.envapp import EnvAppManager
from proxy.app.services.servoservice import ServoServiceManager
from proxy.app.services.sysstatservice import SysStatServiceManager
from proxy.app.services.envappfc import EnvAppFcManager
from proxy.app.services.recoveryservice import RecoveryServiceManager
from proxy.app.services.gpsservice import GPSServiceManager
from proxy.app.services.primerservice import PrimerServiceManager
from proxy.app.services.fcsysstatservice import FcSysStatServiceManager
from proxy.app.services.mainservice import MainServiceManager
from proxy.app.services.fcfileloggerapp import FcFileLoggerAppManager

# Get the project root directory (parent of 'api' directory)
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_file_dir))
csv_dir = os.path.join(project_root, 'desktop', 'data', 'csv')
csv_filename = os.path.join(csv_dir, 'data.csv')

# Ensure directory exists
os.makedirs(csv_dir, exist_ok=True)

logger.info(f"CSV file will be saved to: {csv_filename}")

csv_lock = asyncio.Lock()

managers = [FcFileLoggerAppManager() ,EngineServiceManager(), EnvAppManager(), ServoServiceManager(), SysStatServiceManager(), EnvAppFcManager(), RecoveryServiceManager(), GPSServiceManager(), PrimerServiceManager(), FcSysStatServiceManager(), MainServiceManager()]

# Task tracking
save_task = None


def generate_header():
    header = ['timestamp']
    for manager in managers:
        for method_name in dir(manager):
            if callable(getattr(manager, method_name)) and method_name.startswith("get"):
                event_name = method_name[4:].lower()
                header.append(event_name)
    return header


header = generate_header()
first_write = True


async def write_row_to_csv(row, is_header=False):
    """Write a single row to CSV file with proper error handling."""
    global first_write
    try:
        async with csv_lock:
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if is_header and first_write:
                    writer.writerow(header)
                    logger.info(f"Wrote CSV header with {len(header)} columns: {header}")
                    first_write = False
                elif not is_header:
                    writer.writerow(row)
                    logger.debug(f"Wrote CSV row: {row}")
                file.flush()
                os.fsync(file.fileno())
    except Exception as e:
        logger.exception("Error writing to CSV file '{}': {}", csv_filename, e)
        raise


async def save_to_csv(data_generator):
    """Save data from generator to CSV file."""
    global first_write
    
    try:
        logger.info(f"Starting to save data to CSV file: {csv_filename}")
        # Write header if first write
        if first_write:
            await write_row_to_csv(None, is_header=True)
        
        # Process data rows
        row_count = 0
        async for row in data_generator:
            if not collect_data_flag:
                logger.info("collect_data_flag is False, stopping save loop")
                break
            await write_row_to_csv(row)
            row_count += 1
            if row_count % 10 == 0:  # Log every 10 rows
                logger.info(f"Saved {row_count} rows to CSV")
        
        logger.info(f"Finished saving. Total rows saved: {row_count}")
    except Exception as e:
        logger.exception("Error in save_to_csv: {}", e)
    finally:
        logger.info("Stopped saving data to CSV")


collect_data_flag = False


async def collect_manager_data():
    logger.info("Starting data collection loop")
    row_count = 0
    while collect_data_flag:
        timestamp = datetime.now().strftime('%H:%M:%S.%f')
        current_row = [timestamp]

        for manager in managers:
            try:
                for method_name in dir(manager):
                    if callable(getattr(manager, method_name)) and method_name.startswith("get"):
                        value = getattr(manager, method_name)()
                        current_row.append(value)
            except Exception as e:
                logger.exception("Error collecting data from manager {}: {}", type(manager).__name__, e)

        if current_row:
            row_count += 1
            if row_count % 10 == 0:  # Log every 10 rows
                logger.debug(f"Collected {row_count} rows so far")
            yield current_row

        await asyncio.sleep(0.1)
    
    logger.info(f"Stopped data collection. Total rows collected: {row_count}")


save_router = APIRouter(prefix="/save", tags=["save"])


@save_router.post("/start")
async def start_collecting(background_tasks: BackgroundTasks):
    global collect_data_flag, save_task
    
    if collect_data_flag:
        return {"status": "Already collecting data", "file": csv_filename}
    
    collect_data_flag = True
    data_generator = collect_manager_data()
    save_task = asyncio.create_task(save_to_csv(data_generator))
    logger.info(f"Started collecting data to file: {csv_filename}")
    return {"status": "Started collecting data", "file": csv_filename}


@save_router.post("/stop")
async def stop_collecting():
    global collect_data_flag, save_task
    
    collect_data_flag = False
    
    # Wait for task to finish gracefully
    if save_task and not save_task.done():
        try:
            await asyncio.wait_for(save_task, timeout=2.0)
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for save task to finish")
        except Exception as e:
            logger.exception("Error stopping save task: {}", e)
    
    save_task = None
    logger.info("Stopped collecting data")
    return {"status": "Stopped collecting data"}