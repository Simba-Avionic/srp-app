import asyncio
import ipaddress
import logging
import random
from typing import Tuple

from someipy import (
    TransportLayerProtocol,
    MethodResult,
    ReturnCode,
    MessageType,
    ServiceBuilder,
    EventGroup,
    construct_server_service_instance,
)
from someipy.serialization import Bool
from someipy.service import Method
from someipy.service_discovery import construct_service_discovery
from someipy.logging import set_someipy_log_level

from proxy.app.parser.custom_dataclasses.engineservice_dataclass import StartMsg, CurrentModeMsg

SD_MULTICAST_GROUP = "224.224.224.245"
SD_PORT = 30490
INTERFACE_IP = "127.0.0.2"

SERVICE_ID = 518
METHOD_ID = 1
EVENTGROUP_ID = 32769
EVENT_ID = 32769
INSTANCE_ID_METHOD = 1
INSTANCE_ID_EVENT = 32769


async def method_handler(input_data: bytes, addr: Tuple[str, int]) -> MethodResult:
    print(f"Received data: {' '.join(f'0x{b:02x}' for b in input_data)} from IP: {addr[0]} Port: {addr[1]}")
    result = MethodResult()
    try:
        addends = StartMsg()
        addends.deserialize(input_data)
    except Exception as e:
        print(f"Error during deserialization: {e}")
        result.message_type = MessageType.RESPONSE
        result.return_code = ReturnCode.E_MALFORMED_MESSAGE
        return result

    sum = StartMsg()
    sum.out = Bool(False)
    print(f"Send back: {' '.join(f'0x{b:02x}' for b in sum.serialize())}")
    result.message_type = MessageType.RESPONSE
    result.return_code = ReturnCode.E_OK
    result.payload = sum.serialize()
    return result


def create_engine_message(msg: CurrentModeMsg):
    msg.out.value = random.randint(1, 20)
    return msg


async def setup_service_discovery():
    return await construct_service_discovery(SD_MULTICAST_GROUP, SD_PORT, INTERFACE_IP)


async def setup_method_service(service_discovery):
    addition_method = Method(id=METHOD_ID, method_handler=method_handler)
    service = (
        ServiceBuilder()
        .with_service_id(SERVICE_ID)
        .with_major_version(1)
        .with_method(addition_method)
        .build()
    )
    service_instance = await construct_server_service_instance(
        service,
        instance_id=INSTANCE_ID_METHOD,
        endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 3000),
        ttl=5,
        sd_sender=service_discovery,
        cyclic_offer_delay_ms=2000,
        protocol=TransportLayerProtocol.UDP,
    )
    service_discovery.attach(service_instance)
    service_instance.start_offer()
    return service_instance


async def setup_event_service(service_discovery):
    engine_eventgroup = EventGroup(id=EVENTGROUP_ID, event_ids=[EVENT_ID])
    engineservice = (
        ServiceBuilder()
        .with_service_id(SERVICE_ID)
        .with_major_version(1)
        .with_eventgroup(engine_eventgroup)
        .build()
    )
    service_instance = await construct_server_service_instance(
        engineservice,
        instance_id=INSTANCE_ID_EVENT,
        endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 3001),
        ttl=5,
        sd_sender=service_discovery,
        cyclic_offer_delay_ms=2000,
        protocol=TransportLayerProtocol.UDP,
    )
    service_discovery.attach(service_instance)
    service_instance.start_offer()
    return service_instance


async def main():
    set_someipy_log_level(logging.DEBUG)
    service_discovery = await setup_service_discovery()
    method_service_instance = await setup_method_service(service_discovery)
    event_service_instance = await setup_event_service(service_discovery)
    msg = CurrentModeMsg()
    try:
        while True:
            await asyncio.sleep(1)
            engine_msg = create_engine_message(msg)
            payload = engine_msg.serialize()
            event_service_instance.send_event(EVENTGROUP_ID, EVENT_ID, payload)
    except asyncio.CancelledError:
        await method_service_instance.stop_offer()
        await event_service_instance.stop_offer()
    finally:
        service_discovery.close()


if __name__ == "__main__":
    asyncio.run(main())
