
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.fcsysstatservice import FcSysStatServiceManager

namespace = '/fcsysstatservice'

def register_fcsysstatservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to fcsysstatservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from fcsysstatservice namespace", sid)

    
    @sio.on('newsystemusage', namespace=namespace)
    async def get_newsystemusage(sid, data):
        try:
            manager = FcSysStatServiceManager()
            response = manager.get_newsystemusage()
            await sio.emit('newsystemusage', 
                          {'event_name': 'newsystemusage', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newsystemusage: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
