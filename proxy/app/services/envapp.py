
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
from proxy.app.dataclasses.envapp_dataclass import NewTempEvent_1Out
from proxy.app.dataclasses.envapp_dataclass import NewTempEvent_2Out
from proxy.app.dataclasses.envapp_dataclass import NewTempEvent_3Out
from proxy.app.dataclasses.envapp_dataclass import NewPressEventOut
from proxy.app.dataclasses.envapp_dataclass import CalPressureSensorIn

class EnvAppManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(EnvAppManager, cls).__new__(cls)
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
            id=32769, event_ids=[32769, 32770, 32771, 32772]
        )

        envapp = (
            ServiceBuilder()
            .with_service_id(514)
            .with_major_version(1).with_eventgroup(event_group)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=envapp,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10334),
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
                    newTempEvent_1_msg = NewTempEvent_1Out().deserialize(someip_message.payload)
                    self.newtempevent_1 = newTempEvent_1_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32770:
                try:
                    newTempEvent_2_msg = NewTempEvent_2Out().deserialize(someip_message.payload)
                    self.newtempevent_2 = newTempEvent_2_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32771:
                try:
                    newTempEvent_3_msg = NewTempEvent_3Out().deserialize(someip_message.payload)
                    self.newtempevent_3 = newTempEvent_3_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32772:
                try:
                    newPressEvent_msg = NewPressEventOut().deserialize(someip_message.payload)
                    self.newpressevent = newPressEvent_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
    async def shutdown(self):
        if self.instance:
            await self.instance.close()

    def get_newtempevent_1(self):
        return self.newtempevent_1
    
    def get_newtempevent_2(self):
        return self.newtempevent_2
    
    def get_newtempevent_3(self):
        return self.newtempevent_3
    
    def get_newpressevent(self):
        return self.newpressevent
    
    async def CalPressureSensor(self):
        await self.find_service()
        method_result = await self.instance.call_method(
            1, b''
        )
    
        return method_result
    
async def initialize_envapp(sd):
    service_manager = EnvAppManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await service_manager.shutdown()
