import json
from typing import Dict, Any
from proxy.app.settings import INTERFACE_IP


def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file:
        return json.load(file)

def save_code(file_path: str, code: str):
    with open(file_path, "w") as file:
        file.write(code)

def generate_service_code(parsed_config, port=3002, ttl=5):
    services = parsed_config['someip']
    service_code = f"""
import ipaddress
import logging
from someipy import (
    construct_client_service_instance,
    TransportLayerProtocol,
    ServiceBuilder, SomeIpMessage
)
from someipy.logging import set_someipy_log_level
from someipy.service_discovery import construct_service_discovery
from proxy.app.settings import INTERFACE_IP, MULTICAST_GROUP, SD_PORT
"""

    events_callback = ""
    method_callback = ""
    for service_name, service_config in services.items():
        events = service_config.get('events', {})
        methods = service_config.get('methods', {})
        for event_name in events:
            service_code += f"""
from proxy.app.parser.dataclass.{service_name.lower()}_dataclass import {event_name}Msg"""
        for method_name in methods:
            service_code += f"""
from proxy.app.parser.dataclass.{service_name.lower()}_dataclass import {method_name}Msg"""
        service_code += "\n"
        events_callback += f"""
                  
def callback_{event_name.lower()}_msg(someip_message: SomeIpMessage) -> None:
    try:
        print(f"Received {{len(someip_message.payload)}} bytes for event {{someip_message.header.method_id}}. Attempting deserialization...")
        {event_name}_msg = {event_name}Msg().deserialize(someip_message.payload)
        print({event_name}_msg)
    except Exception as e:
        print(f"Error in deserialization: {{e}}")
"""

    service_code += events_callback

    for method_name, method_config in methods.items():
        instance_id = method_config['id']
        method_callback += f"""
async def {method_name}({method_name.lower()}) -> None:
    method_result = await {method_name.lower()}_instance.call_method(
        {instance_id}, {method_name}Msg().serialize()
    )
    return method_result
"""
    service_code += method_callback
    service_code += f"""
async def setup_service_discovery():
    return await construct_service_discovery(MULTICAST_GROUP, SD_PORT, INTERFACE_IP)

async def construct_service_instances(service_discovery):
    interface_ip = "{INTERFACE_IP}"
"""

    for service_name, service_config in services.items():
        service_id = service_config['service_id']
        major_version = service_config['major_version']
        methods = service_config.get('methods', {})
        events = service_config.get('events', {})

        service_variable_name = f"{service_name.lower()}"
        service_code += f"""
    {service_variable_name}_instances = []

    {service_variable_name}= (
        ServiceBuilder()
        .with_service_id({service_id})
        .with_major_version({major_version})
        .build()
        )
"""

        for method_name, method_config in methods.items():
            instance_id = method_config['id']
            service_code += f"""
    {method_name.lower()}_instance = await construct_client_service_instance(
        service={service_variable_name},
        instance_id={instance_id},
        endpoint=(ipaddress.IPv4Address(interface_ip), {port}),
        ttl={ttl},
        sd_sender=service_discovery,
        protocol=TransportLayerProtocol.UDP,
    )
    {service_variable_name}_instances.append({method_name.lower()}_instance)
"""

        for event_name, event_config in events.items():
            instance_id = event_config['id']
            service_code += f"""
    {event_name.lower()}_instance = await construct_client_service_instance(
        service={service_variable_name.lower()},
        instance_id={instance_id},
        endpoint=(ipaddress.IPv4Address(interface_ip), {port}),
        ttl={ttl},
        sd_sender=service_discovery,
        protocol=TransportLayerProtocol.UDP,
    )
    {event_name.lower()}_instance.register_callback(callback_{event_name.lower()}_msg)
    {event_name.lower()}_instance.subscribe_eventgroup({instance_id})
    {service_variable_name}_instances.append({event_name.lower()}_instance)
"""

    service_code += f"""
    for instance in {service_variable_name}_instances:
        service_discovery.attach(instance)
    return {service_variable_name}_instances


async def main():
    set_someipy_log_level(logging.DEBUG)
    service_discovery = await setup_service_discovery()
    service_instances = await construct_service_instances(service_discovery)
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Shutting down...")
    finally:
        service_discovery.close()
        for instance in service_instances:
            await instance.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
"""
    save_code(f'service/{service_variable_name}.py', service_code)
    return service_code


def process_service_json(input_json_path: str):
    parsed_config = load_json(input_json_path)
    generate_service_code(parsed_config)


input_json_path = 'input/engine_service.json'
process_service_json(input_json_path)
