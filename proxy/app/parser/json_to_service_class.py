import json
from typing import Dict, Any

from proxy.app import settings
from proxy.app.utils import increment_port

def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file:
        return json.load(file)

def save_code(file_path: str, code: str):
    with open(file_path, "w") as file:
        file.write(code)




def generate_service_code(parsed_config, ttl=5):
    services = parsed_config['someip']
    service_code = f"""
import ipaddress
import logging
import asyncio

from someipy import (
    construct_client_service_instance,
    TransportLayerProtocol,
    ServiceBuilder, SomeIpMessage
)
from proxy.app.settings import INTERFACE_IP
"""

    for service_name, service_config in services.items():
        for event_name in service_config.get('events', {}).keys():
            service_code += f"from proxy.app.parser.custom_dataclasses.{service_name.lower()}_dataclass import {event_name}Out\n"

        for method_name in service_config.get('methods', {}).keys():
            service_code += f"from proxy.app.parser.custom_dataclasses.{service_name.lower()}_dataclass import {method_name}In\n"

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
            self.methods = []
            self.events = []
            self.initialized = False
"""

    for service_name, service_config in services.items():
        for method_name in service_config.get('methods', {}).keys():
            service_code += f"            self.{method_name.lower()}_instance = None\n"
        for event_name in service_config.get('events', {}).keys():
            service_code += f"            self.{event_name.lower()}_instance = None\n"
            service_code += f"            self.{event_name.lower()} = None\n"
    service_code += f"""
    async def ensure_initialized(self):
        if not self.initialized:
            await self.setup_manager()
            self.initialized = True
    """
    for service_name, service_config in services.items():
        for event_name in service_config.get('events', {}).keys():
            service_code += f"""
    def get_{event_name.lower()}(self):
        return self.{event_name.lower()}
    """

    for method_name, method_config in service_config.get('methods', {}).items():
        in_type = method_config['data_structure']['in']['type']
        service_code += f"""
    async def {method_name}(self{', ' + method_name.lower() if in_type != 'void' else ''}):
        await self.ensure_initialized()
        while not self.{method_name.lower()}_instance.service_found():
            print("Waiting for service")
            await asyncio.sleep(0.5)
    """

        if in_type == 'void':
            service_code += f"""
        method_result = await self.{method_name.lower()}_instance.call_method(
            {method_config['id']}, b''
        )
    """
        else:
            service_code += f"""
        {method_name.lower()}_msg = {method_name}In()
        {method_name.lower()}_msg.from_json({method_name.lower()})
        method_result = await self.{method_name.lower()}_instance.call_method(
            {method_config['id']}, {method_name.lower()}_msg.serialize()
        )
    """
        service_code += """
        return method_result
    """

    service_code += f"""
    
    def assign_service_discovery(self, new_sd):
        self.service_discovery = new_sd

    async def setup_manager(self) -> None:"""

    for service_name, service_config in services.items():
        service_code += f"""
        {service_name.lower()} = (
            ServiceBuilder()
            .with_service_id({service_config['service_id']})
            .with_major_version({service_config['major_version']})
            .build()
        )
"""

        for method_name, method_config in service_config.get('methods', {}).items():
            service_code += f"""
        self.{method_name.lower()}_instance = await construct_client_service_instance(
            service={service_name.lower()},
            instance_id={method_config['id']},
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), {settings.NEXT_PORT}),
            ttl={ttl},
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.methods.append(self.{method_name}) 
        self.service_discovery.attach(self.{method_name.lower()}_instance)
"""
            increment_port()

        for event_name, event_config in service_config.get('events', {}).items():
            service_code += f"""
        self.{event_name.lower()}_instance = await construct_client_service_instance(
            service={service_name.lower()},
            instance_id={event_config['id']},
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), {settings.NEXT_PORT}),
            ttl={ttl},
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.{event_name.lower()}_instance.register_callback(self.callback_{event_name.lower()}_msg)
        self.{event_name.lower()}_instance.subscribe_eventgroup({event_config['id']})
        self.events.append(self.{event_name.lower()}_instance)
        self.service_discovery.attach(self.{event_name.lower()}_instance)
"""
            increment_port()

    for service_name, service_config in services.items():
        for event_name in service_config.get('events', {}).keys():
            service_code += f"""
    def callback_{event_name.lower()}_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            {event_name}_msg = {event_name}Out().deserialize(someip_message.payload)
            self.{event_name.lower()} = {event_name}_msg.data.value
        except Exception as e:
            print(f"Error in deserialization: {{e}}")
"""

    service_code += """
    async def shutdown(self):
        if self.service_discovery:
            self.service_discovery.close()
        for event in self.events:
            if event:
                await event.close()
        for method in self.methods:
            if method:
                await method.close()
"""

    service_code += f"""
async def initialize_{service_name.lower()}(sd):
    service_manager = {service_name}Manager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Shutting down...")
    finally:
        await service_manager.shutdown()

"""

    save_code(f'services/{service_name.lower()}.py', service_code)
    return service_code


def process_service_json(input_json_path: str):
    parsed_config = load_json(input_json_path)
    generate_service_code(parsed_config)


input_json_path = 'sample_input/engine_service.json'
process_service_json(input_json_path)
