
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
from proxy.app.pressure import pressure_from_raw
from proxy.app.temperature import temperature_from_raw
from proxy.app.dataclasses.secenvapp_dataclass import NewEthanolPressEventOut
from proxy.app.dataclasses.secenvapp_dataclass import NewChamberPressEvent2Out
from proxy.app.dataclasses.secenvapp_dataclass import NewChamberPressEvent3Out
from proxy.app.dataclasses.secenvapp_dataclass import NewBoardTempEvent1Out
from proxy.app.dataclasses.secenvapp_dataclass import NewBoardTempEvent2Out
from proxy.app.dataclasses.secenvapp_dataclass import NewBoardTempEvent3Out

class SecEnvAppManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(SecEnvAppManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None
            self.newethanolpressevent = None
            self.newchamberpressevent2 = None
            self.newchamberpressevent3 = None
            self.newboardtempevent1 = None
            self.newboardtempevent2 = None
            self.newboardtempevent3 = None

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
            id=32772, event_ids=[32772, 32773, 32774, 32775, 32776, 32777]
        )

        secenvapp = (
            ServiceBuilder()
            .with_service_id(526)
            .with_major_version(1).with_eventgroup(event_group)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=secenvapp,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10326),
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
            case 32772:
                try:
                    newEthanolPressEvent_msg = NewEthanolPressEventOut().deserialize(someip_message.payload)
                    self.newethanolpressevent = pressure_from_raw(newEthanolPressEvent_msg.data.value)
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32773:
                try:
                    newChamberPressEvent2_msg = NewChamberPressEvent2Out().deserialize(someip_message.payload)
                    self.newchamberpressevent2 = pressure_from_raw(newChamberPressEvent2_msg.data.value)
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32774:
                try:
                    newChamberPressEvent3_msg = NewChamberPressEvent3Out().deserialize(someip_message.payload)
                    self.newchamberpressevent3 = pressure_from_raw(newChamberPressEvent3_msg.data.value)
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32775:
                try:
                    newBoardTempEvent1_msg = NewBoardTempEvent1Out().deserialize(someip_message.payload)
                    self.newboardtempevent1 = temperature_from_raw(newBoardTempEvent1_msg.data.value)
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32776:
                try:
                    newBoardTempEvent2_msg = NewBoardTempEvent2Out().deserialize(someip_message.payload)
                    self.newboardtempevent2 = temperature_from_raw(newBoardTempEvent2_msg.data.value)
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
            case 32777:
                try:
                    newBoardTempEvent3_msg = NewBoardTempEvent3Out().deserialize(someip_message.payload)
                    self.newboardtempevent3 = temperature_from_raw(newBoardTempEvent3_msg.data.value)
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
    async def shutdown(self):
        if self.instance:
            await self.instance.close()

    def get_newethanolpressevent(self):
        return self.newethanolpressevent
    
    def get_newchamberpressevent2(self):
        return self.newchamberpressevent2
    
    def get_newchamberpressevent3(self):
        return self.newchamberpressevent3
    
    def get_newboardtempevent1(self):
        return self.newboardtempevent1
    
    def get_newboardtempevent2(self):
        return self.newboardtempevent2
    
    def get_newboardtempevent3(self):
        return self.newboardtempevent3
    
async def initialize_secenvapp(sd):
    service_manager = SecEnvAppManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await service_manager.shutdown()
