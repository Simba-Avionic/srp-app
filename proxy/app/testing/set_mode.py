import asyncio
import ipaddress
import logging
from typing import Tuple

from someipy import TransportLayerProtocol, construct_server_service_instance, MethodResult, ReturnCode, MessageType
from someipy.logging import set_someipy_log_level
from someipy.service import Method, ServiceBuilder
from someipy.service_discovery import construct_service_discovery

from proxy.app.parser.custom_dataclasses.engineservice_dataclass import SetModeOut, SetModeIn

SD_MULTICAST_GROUP = "224.224.224.245"
SD_PORT = 30490
interface_ip = "127.0.0.2"
SAMPLE_SERVICE_ID = 518
SAMPLE_INSTANCE_ID = 2
SAMPLE_METHOD_ID = 2



async def method_handler(input_data: bytes, addr: Tuple[str, int]) -> MethodResult:
    print(
        f"Received data: {' '.join(f'0x{b:02x}' for b in input_data)} from IP: {addr[0]} Port: {addr[1]}"
    )

    result = MethodResult()
    try:
        in_data = SetModeIn()
        in_data.deserialize(input_data)
        print(in_data.data)
    except Exception as e:
        print(f"Error during deserialization: {e}")
        result.message_type = MessageType.RESPONSE
        result.return_code = ReturnCode.E_MALFORMED_MESSAGE
        return result

    out = SetModeOut()
    out.data.value = True

    print(f"Send back: {' '.join(f'0x{b:02x}' for b in out.serialize())}")

    result.message_type = MessageType.RESPONSE
    result.return_code = ReturnCode.E_OK
    result.payload = out.serialize()
    return result

async def main():
    set_someipy_log_level(logging.DEBUG)
    service_discovery = await construct_service_discovery(
        SD_MULTICAST_GROUP, SD_PORT, interface_ip
    )

    setmode_method = Method(id=SAMPLE_METHOD_ID, method_handler=method_handler)
    service = (
        ServiceBuilder()
        .with_service_id(SAMPLE_SERVICE_ID)
        .with_major_version(1)
        .with_method(setmode_method)
        .build()
    )
    service_instance_addition = await construct_server_service_instance(
        service,
        instance_id=SAMPLE_INSTANCE_ID,
        endpoint=(
            ipaddress.IPv4Address(interface_ip),
            3000,
        ),
        ttl=5,
        sd_sender=service_discovery,
        cyclic_offer_delay_ms=2000,
        protocol=TransportLayerProtocol.UDP,
    )
    service_discovery.attach(service_instance_addition)

    print("Start offering service..")
    service_instance_addition.start_offer()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Stop offering service..")
        await service_instance_addition.stop_offer()
    finally:
        print("Service Discovery close..")
        service_discovery.close()
    print("End main task..")


if __name__ == "__main__":
    asyncio.run(main())
