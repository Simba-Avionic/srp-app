
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.recoveryservice import RecoveryServiceManager

namespace = '/recoveryservice'

def register_recoveryservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to recoveryservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from recoveryservice namespace", sid)

    
    @sio.on('newparachutestatusevent', namespace=namespace)
    async def get_newparachutestatusevent(sid, data):
        try:
            manager = RecoveryServiceManager()
            response = manager.get_newparachutestatusevent()
            await sio.emit('newparachutestatusevent', 
                          {'event_name': 'newparachutestatusevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newparachutestatusevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
