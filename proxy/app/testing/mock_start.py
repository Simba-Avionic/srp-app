import asyncio
import ipaddress
import logging
from pickle import FALSE
from typing import Tuple

from someipy import TransportLayerProtocol, MethodResult, ReturnCode, MessageType
from someipy.serialization import Bool, Sint8, Sint64
from someipy.service import ServiceBuilder, Method
from someipy.service_discovery import construct_service_discovery
from someipy.server_service_instance import construct_server_service_instance
from someipy.logging import set_someipy_log_level

from proxy.app.parser.dataclass.engineservice_dataclass import StartMsg

SD_MULTICAST_GROUP = "224.224.224.245"
SD_PORT = 30490
interface_ip = "127.0.0.2"
SAMPLE_SERVICE_ID = 0x1234
SAMPLE_INSTANCE_ID = 0x5678
SAMPLE_METHOD_ID = 0x0123


async def add_method_handler(input_data: bytes, addr: Tuple[str, int]) -> MethodResult:
    print(
        f"Received data: {' '.join(f'0x{b:02x}' for b in input_data)} from IP: {addr[0]} Port: {addr[1]}"
    )

    result = MethodResult()

    try:
        # Deserialize the input data
        addends = StartMsg()
        addends.deserialize(input_data)

    except Exception as e:
        print(f"Error during deserialization: {e}")

        # Set the return code to E_MALFORMED_MESSAGE and return
        result.message_type = MessageType.RESPONSE
        result.return_code = ReturnCode.E_MALFORMED_MESSAGE
        return result

    # Perform the addition
    sum = StartMsg()
    sum.out = Bool(False)

    print(f"Send back: {' '.join(f'0x{b:02x}' for b in sum.serialize())}")

    result.message_type = MessageType.RESPONSE
    result.return_code = ReturnCode.E_OK
    result.payload = sum.serialize()
    return result


async def main():
    set_someipy_log_level(logging.DEBUG)
    service_discovery = await construct_service_discovery(
        SD_MULTICAST_GROUP, SD_PORT, interface_ip
    )



    addition_method = Method(id=SAMPLE_METHOD_ID, method_handler=add_method_handler)
    service = (
        ServiceBuilder()
        .with_service_id(SAMPLE_SERVICE_ID)
        .with_major_version(1)
        .with_method(addition_method)
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
