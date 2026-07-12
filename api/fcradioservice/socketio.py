
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.fcradioservice import FcRadioServiceManager

namespace = '/fcradioservice'

def register_fcradioservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to fcradioservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from fcradioservice namespace", sid)

    
    @sio.on('radiostatusevent', namespace=namespace)
    async def get_radiostatusevent(sid, data):
        try:
            manager = FcRadioServiceManager()
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
    
