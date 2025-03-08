import csv
import asyncio
import os

from fastapi import BackgroundTasks, APIRouter
from datetime import datetime

from proxy.app.services.engineservice import EngineServiceManager
from proxy.app.services.envapp import EnvAppManager

current_dir = os.getcwd()

csv_filename = os.path.join(current_dir,  '..','desktop', 'data', 'csv', 'data.csv')

csv_filename = os.path.abspath(csv_filename)

csv_lock = asyncio.Lock()

managers = [EngineServiceManager(), EnvAppManager()]


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


async def save_to_csv(data_generator):
    global first_write
    async with csv_lock:
        with open(csv_filename, mode='a', newline='', buffering=1) as file:
            writer = csv.writer(file)

            if first_write:
                writer.writerow(header)
                first_write = False

            async for row in data_generator:
                writer.writerow(row)
                file.flush()
                os.fsync(file.fileno())


collect_data_flag = False


async def collect_manager_data():
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
                print(f"Error collecting data: {e}")

        if current_row:
            yield current_row

        await asyncio.sleep(0.1)


save_router = APIRouter(prefix="/save", tags=["save"])


@save_router.post("/start")
async def start_collecting(background_tasks: BackgroundTasks):
    global collect_data_flag
    collect_data_flag = True
    data_generator = collect_manager_data()
    asyncio.create_task(save_to_csv(data_generator))
    return {"status": "Started collecting data"}


@save_router.post("/stop")
async def stop_collecting():
    global collect_data_flag
    collect_data_flag = False
    return {"status": "Stopped collecting data"}