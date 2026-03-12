
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
from proxy.app.dataclasses.fileloggerapp_dataclass import LoggingStateOut
from proxy.app.dataclasses.fileloggerapp_dataclass import StartIn
from proxy.app.dataclasses.fileloggerapp_dataclass import StopIn

class FileLoggerAppManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(FileLoggerAppManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None
            self.loggingstate = None

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
            id=32769, event_ids=[32769]
        )

        fileloggerapp = (
            ServiceBuilder()
            .with_service_id(517)
            .with_major_version(1).with_eventgroup(event_group)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=fileloggerapp,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10286),
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
                    LoggingState_msg = LoggingStateOut().deserialize(someip_message.payload)
                    self.loggingstate = LoggingState_msg.data.value
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
    async def shutdown(self):
        if self.instance:
            await self.instance.close()

    def get_loggingstate(self):
        return self.loggingstate
    
    async def Start(self):
        await self.find_service()
        method_result = await self.instance.call_method(
            1, b''
        )
    
        return method_result
    
    async def Stop(self):
        await self.find_service()
        method_result = await self.instance.call_method(
            2, b''
        )
    
        return method_result
    
async def initialize_fileloggerapp(sd):
    service_manager = FileLoggerAppManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await service_manager.shutdown()
