

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
from proxy.app.dataclasses.envservice_dataclass import newTempEvent_1Out
from proxy.app.dataclasses.envservice_dataclass import newTempEvent_2Out
from proxy.app.dataclasses.envservice_dataclass import newTempEvent_3Out
from proxy.app.dataclasses.envservice_dataclass import newPressEventOut
from proxy.app.dataclasses.envservice_dataclass import newDPressEventOut

class EnvServiceManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(EnvServiceManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None
            self.newtempevent_1 = None
            self.newtempevent_2 = None
            self.newtempevent_3 = None
            self.newpressevent = None
            self.newdpressevent = None

    async def find_service(self):
        while not self.instance.service_found():
            print("Waiting for service")
            await asyncio.sleep(0.5)

    def assign_service_discovery(self, new_sd):
        self.service_discovery = new_sd

    async def setup_manager(self) -> None:            
        event_group = EventGroup(
            id=32769, event_ids=[32769, 32770, 32771, 32772, 32773]
        )

        envservice = (
            ServiceBuilder()
            .with_service_id(514)
            .with_major_version(1)
            .with_eventgroup(event_group)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=envservice,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10192),
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
                    newTempEvent_1_msg = newTempEvent_1Out().deserialize(someip_message.payload)
                    self.newtempevent_1 = newTempEvent_1_msg.data.value
                except Exception as e:
                    print(f"Error in deserialization: {e}")
    
            case 32770:
                try:
                    newTempEvent_2_msg = newTempEvent_2Out().deserialize(someip_message.payload)
                    self.newtempevent_2 = newTempEvent_2_msg.data.value
                except Exception as e:
                    print(f"Error in deserialization: {e}")
    
            case 32771:
                try:
                    newTempEvent_3_msg = newTempEvent_3Out().deserialize(someip_message.payload)
                    self.newtempevent_3 = newTempEvent_3_msg.data.value
                except Exception as e:
                    print(f"Error in deserialization: {e}")
    
            case 32772:
                try:
                    newPressEvent_msg = newPressEventOut().deserialize(someip_message.payload)
                    self.newpressevent = newPressEvent_msg.data.value
                except Exception as e:
                    print(f"Error in deserialization: {e}")
    
            case 32773:
                try:
                    newDPressEvent_msg = newDPressEventOut().deserialize(someip_message.payload)
                    self.newdpressevent = newDPressEvent_msg.data.value
                except Exception as e:
                    print(f"Error in deserialization: {e}")
    
    async def shutdown(self):
        if self.instance:
            self.instance.close()

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

