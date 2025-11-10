

import ipaddress
import asyncio

from someipy import (
    construct_client_service_instance,
    TransportLayerProtocol,
    ServiceBuilder,
    SomeIpMessage,
    EventGroup
)
from proxy.app.settings import INTERFACE_IP
from proxy.app.dataclasses.primerservice_dataclass import primeStatusEventOut
from proxy.app.dataclasses.primerservice_dataclass import OnPrimeIn
from proxy.app.dataclasses.primerservice_dataclass import OffPrimeIn
from proxy.app.dataclasses.primerservice_dataclass import StartPrimeIn

class PrimerServiceManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(PrimerServiceManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None
            self.primestatusevent = None

    async def find_service(self):
        while not self.instance.service_found():
            print("Waiting for service")
            await asyncio.sleep(0.5)

    def assign_service_discovery(self, new_sd):
        self.service_discovery = new_sd

    async def setup_manager(self) -> None:
        event_group = EventGroup(
            id=32769, event_ids=[32769]
        )

        primerservice = (
            ServiceBuilder()
            .with_service_id(516)
            .with_major_version(1).with_eventgroup(event_group)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=primerservice,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10259),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.service_discovery.attach(self.instance)
        self.instance.register_callback(self.event_callback)
        self.instance.subscribe_eventgroup(event_group.id)
        self.service_discovery.attach(self.instance)

    def event_callback(self, someip_message: SomeIpMessage) -> None:
        match someip_message.header.method_id:
            case 32769:
                try:
                    primeStatusEvent_msg = primeStatusEventOut().deserialize(someip_message.payload)
                    self.primestatusevent = primeStatusEvent_msg.data.value
                except Exception as e:
                    print(f"Error in deserialization: {e}")

    async def shutdown(self):
        if self.instance:
            self.instance.close()

    def get_primestatusevent(self):
        return self.primestatusevent

    async def OnPrime(self):
        await self.find_service()
        method_result = await self.instance.call_method(
            1, b''
        )

        return method_result

    async def OffPrime(self):
        await self.find_service()
        method_result = await self.instance.call_method(
            2, b''
        )

        return method_result

    async def StartPrime(self):
        await self.find_service()
        method_result = await self.instance.call_method(
            3, b''
        )

        return method_result

async def initialize_primerservice(sd):
    service_manager = PrimerServiceManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Shutting down...")
    finally:
        await service_manager.shutdown()

