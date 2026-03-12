
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

class RadioServiceManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(RadioServiceManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.service_discovery = None
            self.initialized = False
            self.instance = None

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

        radioservice = (
            ServiceBuilder()
            .with_service_id(530)
            .with_major_version(1)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=radioservice,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10279),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.service_discovery.attach(self.instance)
        self.service_discovery.attach(self.instance)
        
    async def shutdown(self):
        if self.instance:
            await self.instance.close()

async def initialize_radioservice(sd):
    service_manager = RadioServiceManager()
    service_manager.assign_service_discovery(sd)
    await service_manager.setup_manager()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutting down...")
    finally:
        await service_manager.shutdown()
