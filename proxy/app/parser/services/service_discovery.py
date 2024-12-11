from someipy.service_discovery import construct_service_discovery
from proxy.app.settings import MULTICAST_GROUP, SD_PORT, INTERFACE_IP


async def initialize_service_discovery():
    service_discovery = await construct_service_discovery(MULTICAST_GROUP, SD_PORT, INTERFACE_IP)
    return service_discovery
