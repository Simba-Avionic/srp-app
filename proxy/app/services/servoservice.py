
import ipaddress
import asyncio
from loguru import logger

from someipy import (
    construct_client_service_instance,
    TransportLayerProtocol,
    ServiceBuilder, 
    SomeIpMessage,
    EventGroup
)
from proxy.app.settings import INTERFACE_IP
from proxy.app.dataclasses.servoservice_dataclass import NewOxidizerMainValveEventOut
from proxy.app.dataclasses.servoservice_dataclass import NewOxidizerVentValveEventOut
from proxy.app.dataclasses.servoservice_dataclass import NewOxidizerDumpValveEventOut
from proxy.app.dataclasses.servoservice_dataclass import NewPressureFeedMainEventOut
from proxy.app.dataclasses.servoservice_dataclass import NewPressureFeedVentEventOut
from proxy.app.dataclasses.servoservice_dataclass import SetOxidizerMainValveIn
from proxy.app.dataclasses.servoservice_dataclass import SetOxidizerVentValveIn
from proxy.app.dataclasses.servoservice_dataclass import SetOxidizerDumpValveIn
from proxy.app.dataclasses.servoservice_dataclass import SetPressureFeedMainValveIn
from proxy.app.dataclasses.servoservice_dataclass import SetPressureFeedVentValveIn

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
            self.newoxidizermainvalveevent = None
            self.newoxidizerventvalveevent = None
            self.newoxidizerdumpvalveevent = None
            self.newpressurefeedmainevent = None
            self.newpressurefeedventevent = None

    async def find_service(self):
        try:
            while not self.instance or not self.instance.service_found():
                logger.debug("Waiting for service")
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            return

    def assign_service_discovery(self, new_sd):
        self.service_discovery = new_sd

    async def setup_manager(self) -> None:            
        event_group = EventGroup(
            id=32769, event_ids=[32769, 32770, 32771, 32772, 32773]
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
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10325),
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
                    newOxidizerMainValveEvent_msg = NewOxidizerMainValveEventOut().deserialize(someip_message.payload)
                    self.newoxidizermainvalveevent = newOxidizerMainValveEvent_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32770:
                try:
                    newOxidizerVentValveEvent_msg = NewOxidizerVentValveEventOut().deserialize(someip_message.payload)
                    self.newoxidizerventvalveevent = newOxidizerVentValveEvent_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32771:
                try:
                    newOxidizerDumpValveEvent_msg = NewOxidizerDumpValveEventOut().deserialize(someip_message.payload)
                    self.newoxidizerdumpvalveevent = newOxidizerDumpValveEvent_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32772:
                try:
                    newPressureFeedMainEvent_msg = NewPressureFeedMainEventOut().deserialize(someip_message.payload)
                    self.newpressurefeedmainevent = newPressureFeedMainEvent_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32773:
                try:
                    newPressureFeedVentEvent_msg = NewPressureFeedVentEventOut().deserialize(someip_message.payload)
                    self.newpressurefeedventevent = newPressureFeedVentEvent_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
    async def shutdown(self):
        if self.instance:
            await self.instance.close()

    def get_newoxidizermainvalveevent(self):
        return self.newoxidizermainvalveevent
    
    def get_newoxidizerventvalveevent(self):
        return self.newoxidizerventvalveevent
    
    def get_newoxidizerdumpvalveevent(self):
        return self.newoxidizerdumpvalveevent
    
    def get_newpressurefeedmainevent(self):
        return self.newpressurefeedmainevent
    
    def get_newpressurefeedventevent(self):
        return self.newpressurefeedventevent
    
    async def SetOxidizerMainValve(self, setoxidizermainvalve):
        await self.find_service()
        setoxidizermainvalve_msg = SetOxidizerMainValveIn()
        setoxidizermainvalve_msg.from_json(setoxidizermainvalve)
        method_result = await self.instance.call_method(
            1, setoxidizermainvalve_msg.serialize()
        )
    
        return method_result
    
    async def SetOxidizerVentValve(self, setoxidizerventvalve):
        await self.find_service()
        setoxidizerventvalve_msg = SetOxidizerVentValveIn()
        setoxidizerventvalve_msg.from_json(setoxidizerventvalve)
        method_result = await self.instance.call_method(
            3, setoxidizerventvalve_msg.serialize()
        )
    
        return method_result
    
    async def SetOxidizerDumpValve(self, setoxidizerdumpvalve):
        await self.find_service()
        setoxidizerdumpvalve_msg = SetOxidizerDumpValveIn()
        setoxidizerdumpvalve_msg.from_json(setoxidizerdumpvalve)
        method_result = await self.instance.call_method(
            5, setoxidizerdumpvalve_msg.serialize()
        )
    
        return method_result
    
    async def SetPressureFeedMainValve(self, setpressurefeedmainvalve):
        await self.find_service()
        setpressurefeedmainvalve_msg = SetPressureFeedMainValveIn()
        setpressurefeedmainvalve_msg.from_json(setpressurefeedmainvalve)
        method_result = await self.instance.call_method(
            7, setpressurefeedmainvalve_msg.serialize()
        )
    
        return method_result
    
    async def SetPressureFeedVentValve(self, setpressurefeedventvalve):
        await self.find_service()
        setpressurefeedventvalve_msg = SetPressureFeedVentValveIn()
        setpressurefeedventvalve_msg.from_json(setpressurefeedventvalve)
        method_result = await self.instance.call_method(
            9, setpressurefeedventvalve_msg.serialize()
        )
    
        return method_result
    
async def initialize_servoservice(sd):
    service_manager = ServoServiceManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await service_manager.shutdown()
