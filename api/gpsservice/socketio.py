
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.gpsservice import GPSServiceManager

namespace = '/gpsservice'

def register_gpsservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to gpsservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from gpsservice namespace", sid)

    
    @sio.on('gpsrmcstatusevent', namespace=namespace)
    async def get_gpsrmcstatusevent(sid, data):
        try:
            manager = GPSServiceManager()
            response = manager.get_gpsrmcstatusevent()
            await sio.emit('gpsrmcstatusevent', 
                          {'event_name': 'gpsrmcstatusevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event gpsrmcstatusevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('gpsstatusevent', namespace=namespace)
    async def get_gpsstatusevent(sid, data):
        try:
            manager = GPSServiceManager()
            response = manager.get_gpsstatusevent()
            await sio.emit('gpsstatusevent', 
                          {'event_name': 'gpsstatusevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event gpsstatusevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('gpsvtgstatusevent', namespace=namespace)
    async def get_gpsvtgstatusevent(sid, data):
        try:
            manager = GPSServiceManager()
            response = manager.get_gpsvtgstatusevent()
            await sio.emit('gpsvtgstatusevent', 
                          {'event_name': 'gpsvtgstatusevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event gpsvtgstatusevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
