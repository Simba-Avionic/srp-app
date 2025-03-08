

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
from proxy.app.dataclasses.servoservice_dataclass import ServoStatusEventOut
from proxy.app.dataclasses.servoservice_dataclass import ServoVentStatusEventOut
from proxy.app.dataclasses.servoservice_dataclass import SetMainServoValueIn
from proxy.app.dataclasses.servoservice_dataclass import ReadMainServoValueIn
from proxy.app.dataclasses.servoservice_dataclass import SetVentServoValueIn
from proxy.app.dataclasses.servoservice_dataclass import ReadVentServoValueIn

class ServoServiceManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(ServoServiceManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None
            self.servostatusevent = None
            self.servoventstatusevent = None

    async def find_service(self):
        while not self.instance.service_found():
            print("Waiting for service")
            await asyncio.sleep(0.5)

    def assign_service_discovery(self, new_sd):
        self.service_discovery = new_sd

    async def setup_manager(self) -> None:            
        event_group = EventGroup(
            id=32769, event_ids=[32769, 32770]
        )

        servoservice = (
            ServiceBuilder()
            .with_service_id(515)
            .with_major_version(1).with_eventgroup(event_group)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=servoservice,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10255),
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
                    ServoStatusEvent_msg = ServoStatusEventOut().deserialize(someip_message.payload)
                    self.servostatusevent = ServoStatusEvent_msg.data.value
                except Exception as e:
                    print(f"Error in deserialization: {e}")
    
            case 32770:
                try:
                    ServoVentStatusEvent_msg = ServoVentStatusEventOut().deserialize(someip_message.payload)
                    self.servoventstatusevent = ServoVentStatusEvent_msg.data.value
                except Exception as e:
                    print(f"Error in deserialization: {e}")
    
    async def shutdown(self):
        if self.instance:
            self.instance.close()

    def get_servostatusevent(self):
        return self.servostatusevent
    
    def get_servoventstatusevent(self):
        return self.servoventstatusevent
    
    async def SetMainServoValue(self, setmainservovalue):
        await self.find_service()
        setmainservovalue_msg = SetMainServoValueIn()
        setmainservovalue_msg.from_json(setmainservovalue)
        method_result = await self.instance.call_method(
            1, setmainservovalue_msg.serialize()
        )
    
        return method_result
    
    async def ReadMainServoValue(self):
        await self.find_service()
        method_result = await self.instance.call_method(
            2, b''
        )
    
        return method_result
    
    async def SetVentServoValue(self, setventservovalue):
        await self.find_service()
        setventservovalue_msg = SetVentServoValueIn()
        setventservovalue_msg.from_json(setventservovalue)
        method_result = await self.instance.call_method(
            3, setventservovalue_msg.serialize()
        )
    
        return method_result
    
    async def ReadVentServoValue(self):
        await self.find_service()
        method_result = await self.instance.call_method(
            4, b''
        )
    
        return method_result
    
async def initialize_servoservice(sd):
    service_manager = ServoServiceManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Shutting down...")
    finally:
        await service_manager.shutdown()

