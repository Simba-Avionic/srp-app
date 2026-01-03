import json
from pathlib import Path
from typing import Dict, Any

from proxy.app import settings
from proxy.app.utils import increment_port

# --- Globals ---
BASE_OUTPUT_DIR = (Path(__file__).resolve().parent / "../../proxy/app/services").resolve()

# --- Parsing Helpers ---
def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r") as f:
        return json.load(f)

# --- Code Generator ---
def generate_service_code(parsed_config: Dict[str, Any], ttl=5) -> tuple[str, str]:
    services = parsed_config['someip']
    
    # We assume the file usually contains one main service or we name the file after the last one processed
    # (This matches your previous logic where service_name variable persisted)
    service_name = "" 

    service_code = f"""
import ipaddress
import asyncio
from loguru import logger

from someipy import (
    construct_client_service_instance,
    TransportLayerProtocol,
    ServiceBuilder, 
    SomeIpMessage,
    EventGroup
)
from proxy.app.settings import INTERFACE_IP
"""

    for s_name, service_config in services.items():
        service_name = s_name # Capture name for file saving
        for event_name in service_config.get('events', {}).keys():
            service_code += f"from proxy.app.dataclasses.{s_name.lower()}_dataclass import {event_name}Out\n"

        for method_name in service_config.get('methods', {}).keys():
            service_code += f"from proxy.app.dataclasses.{s_name.lower()}_dataclass import {method_name}In\n"

    service_code += f"""
class {service_name}Manager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super({service_name}Manager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None"""
    
    for s_name, service_config in services.items():
        for event_name in service_config.get('events', {}).keys():
            service_code += f"""
            self.{event_name.lower()} = None"""

    service_code += f"""

    async def find_service(self):
        try:
            while not self.instance or not self.instance.service_found():
                logger.debug("Waiting for service")
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            return

    def assign_service_discovery(self, new_sd):
        self.service_discovery = new_sd

    async def setup_manager(self) -> None:"""

    for s_name, service_config in services.items():
        event_ids = [event_config['id'] for event_config in service_config.get('events', {}).values()]

        if event_ids:
            service_code += f"""            
        event_group = EventGroup(
            id={event_ids[0]}, event_ids={event_ids}
        )"""

    for s_name, service_config in services.items():
        service_code += f"""

        {s_name.lower()} = (
            ServiceBuilder()
            .with_service_id({service_config['service_id']})
            .with_major_version({service_config['major_version']})"""

        if any(event_config.get('id') for event_config in service_config.get('events', {}).values()):
            service_code += f".with_eventgroup(event_group)"

        service_code += f"""
            .build()
        )

        self.instance = await construct_client_service_instance(
            service={s_name.lower()},
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), {settings.NEXT_PORT}),
            ttl={ttl},
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.service_discovery.attach(self.instance)"""

        if any(event_config.get('id') for event_config in service_config.get('events', {}).values()):
            service_code += f"""
        self.instance.register_callback(self.event_callback)
        self.instance.subscribe_eventgroup(event_group.id)"""

        service_code+="""
        self.service_discovery.attach(self.instance)
        """

        increment_port()

    # event callback
    has_events = False
    for s_name, service_config in services.items():
        if any(event_config.get('id') for event_config in service_config.get('events', {}).values()):
            has_events = True
            break
            
    if has_events:
        service_code += f"""
    def event_callback(self, someip_message: SomeIpMessage) -> None:
        match someip_message.header.method_id:"""

    for s_name, service_config in services.items():
        for event_name, event_config in service_config.get('events', {}).items():
            service_code += f"""
            case {event_config['id']}:
                try:
                    {event_name}_msg = {event_name}Out().deserialize(someip_message.payload)
                    self.{event_name.lower()} = {event_name}_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {{e}}")
    """

    service_code += """
    async def shutdown(self):
        if self.instance:
            await self.instance.close()
"""
    # getter for event state
    for s_name, service_config in services.items():
        for event_name in service_config.get('events', {}).keys():
            service_code += f"""
    def get_{event_name.lower()}(self):
        return self.{event_name.lower()}
    """
    
    # methods
    # (Note: Assuming only one service config loop for methods is safe based on previous code structure)
    for s_name, service_config in services.items():
        for method_name, method_config in service_config.get('methods', {}).items():
            in_type = method_config['data_structure']['in']['type']
            orig_name = method_name
            method_name = method_name[0].upper() + method_name[1:]
            service_code += f"""
    async def {method_name}(self{', ' + method_name.lower() if in_type != 'void' else ''}):
        await self.find_service()"""

            if in_type == 'void':
                service_code += f"""
        method_result = await self.instance.call_method(
            {method_config['id']}, b''
        )
    """
            else:
                service_code += f"""
        {method_name.lower()}_msg = {orig_name}In()
        {method_name.lower()}_msg.from_json({method_name.lower()})
        method_result = await self.instance.call_method(
            {method_config['id']}, {method_name.lower()}_msg.serialize()
        )
    """
            service_code += """
        return method_result
    """

    service_code += f"""
async def initialize_{service_name.lower()}(sd):
    service_manager = {service_name}Manager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await service_manager.shutdown()
"""

    return service_code, service_name

# --- Main Execution ---

def process_directory(directory_path: Path):
    BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating service manager files...")
    
    for file in directory_path.rglob("*.json"):
        if file.name.endswith("data_type.json"):
            continue

        print(f"Processing {file}...")
        data = load_json(file)
        code, name = generate_service_code(data)

        output_path = BASE_OUTPUT_DIR / f"{name.lower()}.py"
        output_path.write_text(code)
        print(f"Generated: {output_path}")

if __name__ == "__main__":
    process_directory(Path("/home/krzysztof/srp-app/system_definition/someip/"))