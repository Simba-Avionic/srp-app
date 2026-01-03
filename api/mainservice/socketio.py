
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.mainservice import MainServiceManager

namespace = '/mainservice'

def register_mainservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to mainservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from mainservice namespace", sid)

    
    @sio.on('currentmodestatusevent', namespace=namespace)
    async def get_currentmodestatusevent(sid, data):
        try:
            manager = MainServiceManager()
            response = manager.get_currentmodestatusevent()
            await sio.emit('currentmodestatusevent', 
                          {'event_name': 'currentmodestatusevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event currentmodestatusevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
