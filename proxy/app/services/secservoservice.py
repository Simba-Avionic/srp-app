
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
from proxy.app.dataclasses.secservoservice_dataclass import NewEthanolMainValveEventOut
from proxy.app.dataclasses.secservoservice_dataclass import NewEthanolVentValveEventOut
from proxy.app.dataclasses.secservoservice_dataclass import SetEtanolMainValveIn
from proxy.app.dataclasses.secservoservice_dataclass import SetEthanolVentValveIn

class SecServoServiceManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(SecServoServiceManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None
            self.newethanolmainvalveevent = None
            self.newethanolventvalveevent = None

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
            id=32769, event_ids=[32769, 32770]
        )

        secservoservice = (
            ServiceBuilder()
            .with_service_id(525)
            .with_major_version(1).with_eventgroup(event_group)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=secservoservice,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10327),
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
                    newEthanolMainValveEvent_msg = NewEthanolMainValveEventOut().deserialize(someip_message.payload)
                    self.newethanolmainvalveevent = newEthanolMainValveEvent_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32770:
                try:
                    newEthanolVentValveEvent_msg = NewEthanolVentValveEventOut().deserialize(someip_message.payload)
                    self.newethanolventvalveevent = newEthanolVentValveEvent_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
    async def shutdown(self):
        if self.instance:
            await self.instance.close()

    def get_newethanolmainvalveevent(self):
        return self.newethanolmainvalveevent
    
    def get_newethanolventvalveevent(self):
        return self.newethanolventvalveevent
    
    async def SetEtanolMainValve(self, setetanolmainvalve):
        await self.find_service()
        setetanolmainvalve_msg = SetEtanolMainValveIn()
        setetanolmainvalve_msg.from_json(setetanolmainvalve)
        method_result = await self.instance.call_method(
            1, setetanolmainvalve_msg.serialize()
        )
    
        return method_result
    
    async def SetEthanolVentValve(self, setethanolventvalve):
        await self.find_service()
        setethanolventvalve_msg = SetEthanolVentValveIn()
        setethanolventvalve_msg.from_json(setethanolventvalve)
        method_result = await self.instance.call_method(
            2, setethanolventvalve_msg.serialize()
        )
    
        return method_result
    
async def initialize_secservoservice(sd):
    service_manager = SecServoServiceManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await service_manager.shutdown()
