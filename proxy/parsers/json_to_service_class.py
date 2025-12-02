import json
import os
from typing import Dict, Any, Set

from proxy.app import settings
from proxy.app.utils import increment_port


def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file:
        return json.load(file)


def save_code(file_path: str, code: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    print(file_path)
    with open(file_path, "w") as file:
        file.write(code)


NUMERIC_ENDIAN_TYPES = {
    "uint8":  (1, False),
    "int8":   (1, True),
    "uint16": (2, False),
    "int16":  (2, True),
    "uint32": (4, False),
    "int32":  (4, True),
    "uint64": (8, False),
    "int64":  (8, True),
}


def _collect_event_out_types(services: Dict[str, Any]) -> Set[str]:
    """Zbiera typy danych z pola 'out' eventów, aby wygenerować pomocnicze funkcje endianness."""
    types: Set[str] = set()
    for _service_name, service_config in services.items():
        for _event_name, event_config in service_config.get("events", {}).items():
            out_cfg = event_config.get("data_structure", {}).get("out")
            if not out_cfg:
                continue
            t = out_cfg.get("type")
            if t in NUMERIC_ENDIAN_TYPES:
                types.add(t)
    return types


def generate_service_code(parsed_config, ttl=5):
    services = parsed_config['someip']
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

    # Dodaj pomocnicze funkcje do konwersji big endian -> little endian
    used_types = _collect_event_out_types(services)
    if used_types:
        service_code += "\n"
        for t in sorted(used_types):
            size, signed = NUMERIC_ENDIAN_TYPES[t]
            # dla 1‑bajtowych typów endianness nie ma znaczenia – zwracamy wartość bez zmian
            if size == 1:
                service_code += f"""
def _to_little_endian_{t}(value: int) -> int:
    \"\"\"Konwersja typu {t}; dla 1 bajtu endianness jest bez znaczenia.\"\"\"
    return value
"""
            else:
                service_code += f"""
def _to_little_endian_{t}(value: int) -> int:
    \"\"\"Konwersja wartosci {t} sparsowanej jako BIG ENDIAN na LITTLE ENDIAN.\"\"\"
    if value is None:
        return None
    return int.from_bytes(
        value.to_bytes({size}, byteorder="big", signed={str(signed)}),
        byteorder="little",
        signed={str(signed)},
    )
"""

    for service_name, service_config in services.items():
        for event_name in service_config.get('events', {}).keys():
            service_code += f"from proxy.app.dataclasses.{service_name.lower()}_dataclass import {event_name}Out\n"

        for method_name in service_config.get('methods', {}).keys():
            service_code += f"from proxy.app.dataclasses.{service_name.lower()}_dataclass import {method_name}In\n"

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
    for service_name, service_config in services.items():
        for event_name in service_config.get('events', {}).keys():
            service_code += f"""
            self.{event_name.lower()} = None"""
    # service and instance definition
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

    for service_name, service_config in services.items():
        event_ids = [event_config['id'] for event_config in service_config.get('events', {}).values()]

        if event_ids:
            service_code += f"""            
        event_group = EventGroup(
            id={event_ids[0]}, event_ids={event_ids}
        )"""

    for service_name, service_config in services.items():
        service_code += f"""

        {service_name.lower()} = (
            ServiceBuilder()
            .with_service_id({service_config['service_id']})
            .with_major_version({service_config['major_version']})"""

        if any(event_config.get('id') for event_config in service_config.get('events', {}).values()):
            service_code += f".with_eventgroup(event_group)"

        service_code += f"""
            .build()
        )

        self.instance = await construct_client_service_instance(
            service={service_name.lower()},
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
    if any(event_config.get('id') for event_config in service_config.get('events', {}).values()):
        service_code += f"""
    def event_callback(self, someip_message: SomeIpMessage) -> None:
        match someip_message.header.method_id:"""

    for service_name, service_config in services.items():
        for event_name, event_config in service_config.get('events', {}).items():
            # Ustalenie typu 'out' eventu w celu dobrania odpowiedniej funkcji endianness
            out_cfg = event_config.get('data_structure', {}).get('out', {})
            out_type = out_cfg.get('type')
            endian_helper = None
            if out_type in NUMERIC_ENDIAN_TYPES:
                endian_helper = f"_to_little_endian_{out_type}"

            if endian_helper:
                assign_expr = f"{endian_helper}({event_name}_msg.data.value)"
            else:
                assign_expr = f"{event_name}_msg.data.value"

            service_code += f"""
            case {event_config['id']}:
                try:
                    {event_name}_msg = {event_name}Out().deserialize(someip_message.payload)
                    self.{event_name.lower()} = {assign_expr}
                except Exception as e:
                    logger.exception("Error in deserialization: {{}}, e)
    """

    service_code += """
    async def shutdown(self):
        if self.instance:
            await self.instance.close()
"""
    # getter for event state
    for service_name, service_config in services.items():
        for event_name in service_config.get('events', {}).keys():
            service_code += f"""
    def get_{event_name.lower()}(self):
        return self.{event_name.lower()}
    """
    # methods
    for method_name, method_config in service_config.get('methods', {}).items():
        in_type = method_config['data_structure']['in']['type']
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
        {method_name.lower()}_msg = {method_name}In()
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

    save_code(f'../app/services/{service_name.lower()}.py', service_code)
    print(service_code)
    return service_code


def process_service_json(input_json_path: str):
    parsed_config = load_json(input_json_path)
    generate_service_code(parsed_config)

# for single files
input_json_path = '/home/krzysztof/srp-app/system_definition/someip/prim_service/service.json'
process_service_json(input_json_path)

def process_multiple_services_json(input_json_path: str, output_dir: str):
    for root, dirs, files in os.walk(input_json_path):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(root, file)
                print(f"Processing {json_file_path}...")

                parsed_config = load_json(json_file_path)

                generate_service_code(parsed_config)



# input_json_path = '../../system_definition/someip'
# process_multiple_services_json(input_json_path, '../app/services/')