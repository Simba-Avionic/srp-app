
import ipaddress
import logging
import asyncio

from someipy import (
    construct_client_service_instance,
    TransportLayerProtocol,
    ServiceBuilder, SomeIpMessage
)
from someipy.logging import set_someipy_log_level
from someipy.service_discovery import construct_service_discovery
from proxy.app.settings import INTERFACE_IP, MULTICAST_GROUP, SD_PORT
from proxy.app.parser.custom_dataclasses.engineservice_dataclass import CurrentModeMsg
from proxy.app.parser.custom_dataclasses.engineservice_dataclass import StartMsg
from proxy.app.parser.custom_dataclasses.engineservice_dataclass import SetModeMsg

class EngineServiceManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(EngineServiceManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.service_discovery = None
        self.methods = []
        self.events = []
        self.start_instance = None
        self.setmode_instance = None
        self.currentmode_instance = None

    async def Start(self, start):
        while not self.start_instance.service_found():
            print("Waiting for service")
            await asyncio.sleep(0.5)

        start_msg = StartMsg()
        start_msg.out.val = start
        method_result = await self.start_instance.call_method(
            1, start_msg.serialize()
        )
        return method_result
    
    async def SetMode(self, setmode):
        while not self.setmode_instance.service_found():
            print("Waiting for service")
            await asyncio.sleep(0.5)

        setmode_msg = SetModeMsg()
        setmode_msg.out.val = setmode
        method_result = await self.setmode_instance.call_method(
            2, setmode_msg.serialize()
        )
        return method_result
    

    async def setup_service_discovery(self):
        if not self.service_discovery:
            self.service_discovery = await construct_service_discovery(MULTICAST_GROUP, SD_PORT, INTERFACE_IP)
        return self.service_discovery

    async def setup_manager(self) -> None:

        engineservice = (
            ServiceBuilder()
            .with_service_id(518)
            .with_major_version(1)
            .build()
        )

        self.start_instance = await construct_client_service_instance(
            service=engineservice,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10038),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.methods.append(self.Start) 
        self.service_discovery.attach(self.start_instance)

        self.setmode_instance = await construct_client_service_instance(
            service=engineservice,
            instance_id=2,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10039),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.methods.append(self.SetMode) 
        self.service_discovery.attach(self.setmode_instance)

        self.currentmode_instance = await construct_client_service_instance(
            service=engineservice,
            instance_id=32769,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10040),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.currentmode_instance.register_callback(self.callback_currentmode_msg)
        self.currentmode_instance.subscribe_eventgroup(32769)
        self.events.append(self.currentmode_instance)
        self.service_discovery.attach(self.currentmode_instance)

    def callback_currentmode_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            print(f"Received {len(someip_message.payload)} bytes for event {someip_message.header.method_id}. Attempting deserialization...")
            CurrentMode_msg = CurrentModeMsg().deserialize(someip_message.payload)
            print(CurrentMode_msg)
        except Exception as e:
            print(f"Error in deserialization: {e}")

    async def shutdown(self):
        if self.service_discovery:
            self.service_discovery.close()
        for event in self.events:
            if event:
                await event.close()
        for method in self.methods:
            if method:
                await method.close()

async def main():
    set_someipy_log_level(logging.DEBUG)
    service_manager = EngineServiceManager()
    await service_manager.setup_service_discovery()
    await service_manager.setup_manager()
    await service_manager.Start(False)
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Shutting down...")
    finally:
        await service_manager.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
