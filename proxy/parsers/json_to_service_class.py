import json
from pathlib import Path
from typing import Dict, Any

from proxy.app import settings
from proxy.app.utils import increment_port

# --- Globals ---
BASE_OUTPUT_DIR = (Path(__file__).resolve().parent / "../../proxy/app/services").resolve()
STRUCT_REGISTRY: Dict[str, Dict[str, str]] = {}

# --- Parsing Helpers ---
def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r") as f:
        return json.load(f)

def find_structs(file_path: Path):
    """Scans data_type files to build a registry of struct fields."""
    data = load_json(file_path)
    structures = data.get("data_structure", {})
    for struct_name, fields in structures.items():
        STRUCT_REGISTRY[struct_name] = fields

def parse_type_name(data_type: str) -> str:
    """Extracts the simple type name from a namespaced string."""
    return data_type.split(".")[-1].split("/")[-1]

# --- Code Generator ---
def generate_service_code(parsed_config: Dict[str, Any], ttl=5) -> tuple[str, str]:
    services = parsed_config['someip']
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

    # Imports
    for s_name, service_config in services.items():
        service_name = s_name 
        for event_name in service_config.get('events', {}).keys():
            event_name = event_name[0].upper() + event_name[1:]
            service_code += f"from proxy.app.dataclasses.{s_name.lower()}_dataclass import {event_name}Out\n"

        for method_name in service_config.get('methods', {}).keys():
            method_name = method_name[0].upper() + method_name[1:]
            service_code += f"from proxy.app.dataclasses.{s_name.lower()}_dataclass import {method_name}In\n"

    # Class Definition
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
    
    # Init variables
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

    # Event Groups
    for s_name, service_config in services.items():
        event_ids = [event_config['id'] for event_config in service_config.get('events', {}).values()]

        if event_ids:
            service_code += f"""            
        event_group = EventGroup(
            id={event_ids[0]}, event_ids={event_ids}
        )"""

    # Service Construction
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

    # --- Event Callback Logic ---
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
            class_name = event_name[0].upper() + event_name[1:]
            
            # Check data type for struct detection
            out_type_raw = event_config['data_structure']['out']['type']
            simple_type = parse_type_name(out_type_raw)
            
            assignment_line = ""
            if simple_type in STRUCT_REGISTRY:
                # It is a struct -> construct list of values
                fields = STRUCT_REGISTRY[simple_type].keys()
                # Creates: [msg.data.field1.value, msg.data.field2.value, ...]
                value_list = [f"{event_name}_msg.data.{field}.value" for field in fields]
                list_str = ", ".join(value_list)
                assignment_line = f"self.{event_name.lower()} = [{list_str}]"
            else:
                # Primitive -> direct value access
                assignment_line = f"self.{event_name.lower()} = {event_name}_msg.data.value"

            service_code += f"""
            case {event_config['id']}:
                try:
                    {event_name}_msg = {class_name}Out().deserialize(someip_message.payload)
                    {assignment_line}
                except Exception as e:
                    logger.exception(f"Error in deserialization: {{e}}")
    """

    service_code += """
    async def shutdown(self):
        if self.instance:
            await self.instance.close()
"""
    # Getters
    for s_name, service_config in services.items():
        for event_name in service_config.get('events', {}).keys():
            service_code += f"""
    def get_{event_name.lower()}(self):
        return self.{event_name.lower()}
    """
    
    # Methods
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

    print("Scanning for structs...")
    # Pre-scan for data types to populate registry
    for file in directory_path.rglob("*data_type.json"):
        find_structs(file)

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
    process_directory(Path("/home/krzysztof/rocket_test/app/system_definition/someip"))