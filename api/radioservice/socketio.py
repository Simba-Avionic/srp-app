
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.radioservice import RadioServiceManager

namespace = '/radioservice'

def register_radioservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to radioservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from radioservice namespace", sid)

    
    @sio.on('radiostatusevent', namespace=namespace)
    async def get_radiostatusevent(sid, data):
        try:
            manager = RadioServiceManager()
            response = manager.get_radiostatusevent()
            await sio.emit('radiostatusevent', 
                          {'event_name': 'radiostatusevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event radiostatusevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
