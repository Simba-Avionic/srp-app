
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.secservoservice import SecServoServiceManager

namespace = '/secservoservice'

def register_secservoservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to secservoservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from secservoservice namespace", sid)

    
    @sio.on('newethanolmainvalveevent', namespace=namespace)
    async def get_newethanolmainvalveevent(sid, data):
        try:
            manager = SecServoServiceManager()
            response = manager.get_newethanolmainvalveevent()
            await sio.emit('newethanolmainvalveevent', 
                          {'event_name': 'newethanolmainvalveevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newethanolmainvalveevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newethanolventvalveevent', namespace=namespace)
    async def get_newethanolventvalveevent(sid, data):
        try:
            manager = SecServoServiceManager()
            response = manager.get_newethanolventvalveevent()
            await sio.emit('newethanolventvalveevent', 
                          {'event_name': 'newethanolventvalveevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newethanolventvalveevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
