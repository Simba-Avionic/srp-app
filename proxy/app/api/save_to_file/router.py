from fastapi import BackgroundTasks, APIRouter
import csv
import asyncio
from datetime import datetime

from proxy.app.parser.services.engineservice import EngineServiceManager
from proxy.app.parser.services.envservice import EnvServiceManager

csv_filename = 'data.csv'
collected_data = []
csv_lock = asyncio.Lock()

managers = [EngineServiceManager(), EnvServiceManager()]


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


async def save_to_csv():
    global collected_data, first_write
    async with csv_lock:
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            if first_write:
                writer.writerow(header)
                first_write = False

            for row in collected_data:
                writer.writerow(row)
        collected_data = []


collect_data_flag = False


async def collect_manager_data():
    global collected_data
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
            collected_data.append(current_row)

        await asyncio.sleep(0.1)


save_router = APIRouter(prefix="/save", tags=["save"])


@save_router.post("/start")
async def start_collecting(background_tasks: BackgroundTasks):
    global collect_data_flag
    collect_data_flag = True
    background_tasks.add_task(collect_manager_data)
    return {"status": "Started collecting data"}


@save_router.post("/stop")
async def stop_collecting():
    global collect_data_flag
    collect_data_flag = False
    await save_to_csv()
    return {"status": "Stopped collecting and data saved to CSV"}
