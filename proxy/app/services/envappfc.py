
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
from proxy.app.dataclasses.envappfc_dataclass import NewBoardTempEvent_1Out
from proxy.app.dataclasses.envappfc_dataclass import NewBoardTempEvent_2Out
from proxy.app.dataclasses.envappfc_dataclass import NewBoardTempEvent_3Out
from proxy.app.dataclasses.envappfc_dataclass import NewBME280EventOut

class EnvAppFcManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(EnvAppFcManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None
            self.newboardtempevent_1 = None
            self.newboardtempevent_2 = None
            self.newboardtempevent_3 = None
            self.newbme280event = None

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

        envappfc = (
            ServiceBuilder()
            .with_service_id(529)
            .with_major_version(1).with_eventgroup(event_group)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=envappfc,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10277),
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
                    newBoardTempEvent_1_msg = NewBoardTempEvent_1Out().deserialize(someip_message.payload)
                    self.newboardtempevent_1 = newBoardTempEvent_1_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32770:
                try:
                    newBoardTempEvent_2_msg = NewBoardTempEvent_2Out().deserialize(someip_message.payload)
                    self.newboardtempevent_2 = newBoardTempEvent_2_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32771:
                try:
                    newBoardTempEvent_3_msg = NewBoardTempEvent_3Out().deserialize(someip_message.payload)
                    self.newboardtempevent_3 = newBoardTempEvent_3_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32772:
                try:
                    newBME280Event_msg = NewBME280EventOut().deserialize(someip_message.payload)
                    self.newbme280event = [newBME280Event_msg.data.temperature.value, newBME280Event_msg.data.humidity.value, newBME280Event_msg.data.altitude.value]
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
    async def shutdown(self):
        if self.instance:
            await self.instance.close()

    def get_newboardtempevent_1(self):
        return self.newboardtempevent_1
    
    def get_newboardtempevent_2(self):
        return self.newboardtempevent_2
    
    def get_newboardtempevent_3(self):
        return self.newboardtempevent_3
    
    def get_newbme280event(self):
        return self.newbme280event
    
async def initialize_envappfc(sd):
    service_manager = EnvAppFcManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await service_manager.shutdown()
