
import ipaddress
import logging
import asyncio

from someipy import (
    construct_client_service_instance,
    TransportLayerProtocol,
    ServiceBuilder, SomeIpMessage
)
from proxy.app.settings import INTERFACE_IP
from proxy.app.parser.custom_dataclasses.envservice_dataclass import newTempEvent_1Out
from proxy.app.parser.custom_dataclasses.envservice_dataclass import newTempEvent_2Out
from proxy.app.parser.custom_dataclasses.envservice_dataclass import newTempEvent_3Out
from proxy.app.parser.custom_dataclasses.envservice_dataclass import newPressEventOut
from proxy.app.parser.custom_dataclasses.envservice_dataclass import newDPressEventOut

class EnvServiceManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(EnvServiceManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.methods = []
            self.events = []
            self.initialized = False
            self.newtempevent_1_instance = None
            self.newtempevent_1 = None
            self.newtempevent_2_instance = None
            self.newtempevent_2 = None
            self.newtempevent_3_instance = None
            self.newtempevent_3 = None
            self.newpressevent_instance = None
            self.newpressevent = None
            self.newdpressevent_instance = None
            self.newdpressevent = None

    async def ensure_initialized(self):
        if not self.initialized:
            await self.setup_manager()
            self.initialized = True
    
    def get_newtempevent_1(self):
        return self.newtempevent_1
    
    def get_newtempevent_2(self):
        return self.newtempevent_2
    
    def get_newtempevent_3(self):
        return self.newtempevent_3
    
    def get_newpressevent(self):
        return self.newpressevent
    
    def get_newdpressevent(self):
        return self.newdpressevent
    
    
    def assign_service_discovery(self, new_sd):
        self.service_discovery = new_sd

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
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10145),
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
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10146),
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
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10147),
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
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10148),
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
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10149),
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
            newTempEvent_1_msg = newTempEvent_1Out().deserialize(someip_message.payload)
            self.newtempevent_1 = newTempEvent_1_msg.data.value
        except Exception as e:
            print(f"Error in deserialization: {e}")

    def callback_newtempevent_2_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            newTempEvent_2_msg = newTempEvent_2Out().deserialize(someip_message.payload)
            self.newtempevent_2 = newTempEvent_2_msg.data.value
        except Exception as e:
            print(f"Error in deserialization: {e}")

    def callback_newtempevent_3_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            newTempEvent_3_msg = newTempEvent_3Out().deserialize(someip_message.payload)
            self.newtempevent_3 = newTempEvent_3_msg.data.value
        except Exception as e:
            print(f"Error in deserialization: {e}")

    def callback_newpressevent_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            newPressEvent_msg = newPressEventOut().deserialize(someip_message.payload)
            self.newpressevent = newPressEvent_msg.data.value
        except Exception as e:
            print(f"Error in deserialization: {e}")

    def callback_newdpressevent_msg(self, someip_message: SomeIpMessage) -> None:
        try:
            newDPressEvent_msg = newDPressEventOut().deserialize(someip_message.payload)
            self.newdpressevent = newDPressEvent_msg.data.value
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

async def initialize_envservice(sd):
    service_manager = EnvServiceManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Shutting down...")
    finally:
        await service_manager.shutdown()

