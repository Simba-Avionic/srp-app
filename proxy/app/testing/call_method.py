import asyncio
import ipaddress
import logging
from typing import Tuple

from someipy import ( TransportLayerProtocol, MethodResult, ReturnCode, MessageType, SomeIpMessage, EventGroup)
from someipy.service import ServiceBuilder, Method
from someipy.service_discovery import construct_service_discovery
from someipy.client_service_instance import (
    MethodResult,
    construct_client_service_instance,
)
from someipy.logging import set_someipy_log_level

from proxy.app.parser.custom_dataclasses.engineservice_dataclass import StartOut, CurrentModeOut

SD_MULTICAST_GROUP = "224.224.224.245"
SD_PORT = 30490
interface_ip = "127.0.0.1"
SAMPLE_SERVICE_ID = 518
SAMPLE_INSTANCE_ID = 1
SAMPLE_METHOD_ID = 1





async def main():
    engine_eventgroup = EventGroup(
        id=32769, event_ids=[32769]
    )
    set_someipy_log_level(logging.DEBUG)
    service_discovery = await construct_service_discovery(
        SD_MULTICAST_GROUP, SD_PORT, interface_ip
    )


    service = (
        ServiceBuilder()
        .with_service_id(SAMPLE_SERVICE_ID)
        .with_major_version(1)
        .with_eventgroup(engine_eventgroup)
        .build()
    )

    client_instance_addition = await construct_client_service_instance(
            service=service,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(interface_ip), 10142),
            sd_sender=service_discovery,
            ttl=500,
            protocol=TransportLayerProtocol.UDP,
    )

    def callback_currentmode_msg(someip_message: SomeIpMessage) -> None:
        try:
            print("event received")
            CurrentMode_msg = CurrentModeOut().deserialize(someip_message.payload)
            currentmode = CurrentMode_msg.data.value
        except Exception as e:
            print(f"Error in deserialization: {e}")

    event_instance = await construct_client_service_instance(
        service,
        instance_id=32769,
        endpoint=(ipaddress.IPv4Address(interface_ip), 3001),
        sd_sender=service_discovery,
        ttl=255,
        protocol=TransportLayerProtocol.UDP,
    )

    event_instance.register_callback(callback_currentmode_msg)
    event_instance.subscribe_eventgroup(32769)
    service_discovery.attach(event_instance)
    service_discovery.attach(client_instance_addition)

    try:
        while True:
            print(f"Service found: {client_instance_addition.service_found()}")

            while not client_instance_addition.service_found():
                print("Waiting for service..")
                await asyncio.sleep(0.5)

            method_result = await client_instance_addition.call_method(
                SAMPLE_METHOD_ID, b''
            )

            if method_result.message_type == MessageType.RESPONSE:
                print(
                    f"Received result for method: {' '.join(f'0x{b:02x}' for b in method_result.payload)}"
                )
                if method_result.return_code == ReturnCode.E_OK:
                    sum = StartOut().deserialize(method_result.payload).data.value
                    print(f"result: {sum}")
                else:
                    print(
                        f"Method call returned an error: {method_result.return_code}"
                    )
            elif method_result.message_type == MessageType.ERROR:
                print("Server returned an error..")
            await  asyncio.sleep(1)

    finally:
        print("Service Discovery close..")
        service_discovery.close()

        print("Shutdown service instance..")
        await client_instance_addition.close()
    print("End main task..")


if __name__ == "__main__":
    asyncio.run(main())