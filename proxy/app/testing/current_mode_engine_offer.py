import asyncio
import ipaddress
import logging
import random

from someipy import ServiceBuilder, EventGroup, construct_server_service_instance, TransportLayerProtocol
from someipy.logging import set_someipy_log_level
from someipy.service_discovery import construct_service_discovery

from proxy.app.parser.custom_dataclasses.engineservice_dataclass import CurrentModeOut

sd_multicast_group = "224.224.224.245"
sd_port = 30490
interface_ip = "127.0.0.4"

sample_service_id = 518
sample_eventgroup_id = 32769
sample_event_id = 32769
sample_instance_id = 32769


def create_engine_message(msg: CurrentModeOut):
    msg.data.value = random.randint(1, 20)
    return msg

async def setup_service_discovery():
    return await construct_service_discovery(sd_multicast_group, sd_port, interface_ip)


async def setup_server_service(service_discovery):
    engine_eventgroup = EventGroup(
        id=sample_eventgroup_id, event_ids=[sample_event_id]
    )
    engineservice = (
        ServiceBuilder()
        .with_service_id(sample_service_id)
        .with_major_version(1)
        .with_eventgroup(engine_eventgroup)
        .build()
    )

    service_instance = await construct_server_service_instance(
        engineservice,
        instance_id=sample_instance_id,
        endpoint=(ipaddress.IPv4Address(interface_ip), 3001),
        ttl=5,
        sd_sender=service_discovery,
        cyclic_offer_delay_ms=2000,
        protocol=TransportLayerProtocol.UDP,
    )

    service_instance.start_offer()
    service_discovery.attach(service_instance)
    return service_instance


async def main_send():
    set_someipy_log_level(logging.DEBUG)
    service_discovery = await setup_service_discovery()
    service_instance = await setup_server_service(service_discovery)
    msg = CurrentModeOut()
    try:
        while True:
            await asyncio.sleep(0.00001)
            engine_msg = create_engine_message(msg)
            payload = engine_msg.serialize()
            service_instance.send_event(
                sample_eventgroup_id, sample_event_id, payload
            )
    except asyncio.CancelledError:
        print("Stopping service offer...")
        await service_instance.stop_offer()
    finally:
        service_discovery.close()


if __name__ == "__main__":
    asyncio.run(main_send())
