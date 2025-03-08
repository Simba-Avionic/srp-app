

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

    async def find_service(self):
        while not self.instance.service_found():
            print("Waiting for service")
            await asyncio.sleep(0.5)

    def assign_service_discovery(self, new_sd):
        self.service_discovery = new_sd

    async def setup_manager(self) -> None:

        fileloggerapp = (
            ServiceBuilder()
            .with_service_id(517)
            .with_major_version(1)
            .build()
        )

        self.instance = await construct_client_service_instance(
            service=fileloggerapp,
            instance_id=1,
            endpoint=(ipaddress.IPv4Address(INTERFACE_IP), 10254),
            ttl=5,
            sd_sender=self.service_discovery,
            protocol=TransportLayerProtocol.UDP,
        )
        self.service_discovery.attach(self.instance)
        self.service_discovery.attach(self.instance)
        
    async def shutdown(self):
        if self.instance:
            self.instance.close()

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
        print("Shutting down...")
    finally:
        await service_manager.shutdown()

