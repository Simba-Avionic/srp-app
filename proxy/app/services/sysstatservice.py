
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
from proxy.app.dataclasses.sysstatservice_dataclass import NewSystemUsageOut

class SysStatServiceManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(SysStatServiceManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None
            self.newsystemusage = None

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

        sysstatservice = (
            ServiceBuilder()
            .with_service_id(522)
            .with_major_version(1).with_eventgroup(event_group)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=sysstatservice,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10273),
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
                    NewSystemUsage_msg = NewSystemUsageOut().deserialize(someip_message.payload)
                    self.newsystemusage = [NewSystemUsage_msg.data.mem_usage.value, NewSystemUsage_msg.data.cpu_usage.value, NewSystemUsage_msg.data.disk_utilization.value]
                except Exception as e:
                    logger.exception(f"Error in deserialization: {e}")
    
    async def shutdown(self):
        if self.instance:
            await self.instance.close()

    def get_newsystemusage(self):
        return self.newsystemusage
    
async def initialize_sysstatservice(sd):
    service_manager = SysStatServiceManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await service_manager.shutdown()
