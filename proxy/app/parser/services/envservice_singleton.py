
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
from proxy.app.parser.dataclasses.envservice_dataclass import newTempEvent_1Msg
from proxy.app.parser.dataclasses.envservice_dataclass import newTempEvent_2Msg
from proxy.app.parser.dataclasses.envservice_dataclass import newTempEvent_3Msg
from proxy.app.parser.dataclasses.envservice_dataclass import newPressEventMsg
from proxy.app.parser.dataclasses.envservice_dataclass import newDPressEventMsg

class ServiceManagerSingleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(ServiceManagerSingleton, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.service_discovery = None
        self.methods = []
        self.events = []
        self.newtempevent_1_instance = None
        self.newtempevent_2_instance = None
        self.newtempevent_3_instance = None
        self.newpressevent_instance = None
        self.newdpressevent_instance = None


    async def setup_service_discovery(self):
        if not self.service_discovery:
            self.service_discovery = await construct_service_discovery(MULTICAST_GROUP, SD_PORT, INTERFACE_IP)
        return self.service_discovery

    async def setup_manager(self) -> None:

        envservice = (
            ServiceBuilder()
            .with_service_id(514)
            .with_major_version(1)
            .build()
        )

        self.newtempevent_1_instance = await construct_client_service_instance(
            service=envservice,
            instance_id=32769,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10000),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.newtempevent_1_instance.register_callback(self.callback_newtempevent_1_msg)
        self.newtempevent_1_instance.subscribe_eventgroup(32769)
        self.events.append(self.newtempevent_1_instance)
        self.service_discovery.attach(self.newtempevent_1_instance)

        self.newtempevent_2_instance = await construct_client_service_instance(
            service=envservice,
            instance_id=32770,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10001),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.newtempevent_2_instance.register_callback(self.callback_newtempevent_2_msg)
        self.newtempevent_2_instance.subscribe_eventgroup(32770)
        self.events.append(self.newtempevent_2_instance)
        self.service_discovery.attach(self.newtempevent_2_instance)

        self.newtempevent_3_instance = await construct_client_service_instance(
            service=envservice,
            instance_id=32771,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10002),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.newtempevent_3_instance.register_callback(self.callback_newtempevent_3_msg)
        self.newtempevent_3_instance.subscribe_eventgroup(32771)
        self.events.append(self.newtempevent_3_instance)
        self.service_discovery.attach(self.newtempevent_3_instance)

        self.newpressevent_instance = await construct_client_service_instance(
            service=envservice,
            instance_id=32773,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10003),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.newpressevent_instance.register_callback(self.callback_newpressevent_msg)
        self.newpressevent_instance.subscribe_eventgroup(32773)
        self.events.append(self.newpressevent_instance)
        self.service_discovery.attach(self.newpressevent_instance)

        self.newdpressevent_instance = await construct_client_service_instance(
            service=envservice,
            instance_id=32771,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10004),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.newdpressevent_instance.register_callback(self.callback_newdpressevent_msg)
        self.newdpressevent_instance.subscribe_eventgroup(32771)
        self.events.append(self.newdpressevent_instance)
        self.service_discovery.attach(self.newdpressevent_instance)

    def callback_newtempevent_1_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            print(f"Received {len(someip_message.payload)} bytes for event {someip_message.header.method_id}. Attempting deserialization...")
            newTempEvent_1_msg = newTempEvent_1Msg().deserialize(someip_message.payload)
            print(newTempEvent_1_msg)
        except Exception as e:
            print(f"Error in deserialization: {e}")

    def callback_newtempevent_2_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            print(f"Received {len(someip_message.payload)} bytes for event {someip_message.header.method_id}. Attempting deserialization...")
            newTempEvent_2_msg = newTempEvent_2Msg().deserialize(someip_message.payload)
            print(newTempEvent_2_msg)
        except Exception as e:
            print(f"Error in deserialization: {e}")

    def callback_newtempevent_3_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            print(f"Received {len(someip_message.payload)} bytes for event {someip_message.header.method_id}. Attempting deserialization...")
            newTempEvent_3_msg = newTempEvent_3Msg().deserialize(someip_message.payload)
            print(newTempEvent_3_msg)
        except Exception as e:
            print(f"Error in deserialization: {e}")

    def callback_newpressevent_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            print(f"Received {len(someip_message.payload)} bytes for event {someip_message.header.method_id}. Attempting deserialization...")
            newPressEvent_msg = newPressEventMsg().deserialize(someip_message.payload)
            print(newPressEvent_msg)
        except Exception as e:
            print(f"Error in deserialization: {e}")

    def callback_newdpressevent_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            print(f"Received {len(someip_message.payload)} bytes for event {someip_message.header.method_id}. Attempting deserialization...")
            newDPressEvent_msg = newDPressEventMsg().deserialize(someip_message.payload)
            print(newDPressEvent_msg)
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
    service_manager = ServiceManagerSingleton()
    await service_manager.setup_service_discovery()
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Shutting down...")
    finally:
        await service_manager.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
