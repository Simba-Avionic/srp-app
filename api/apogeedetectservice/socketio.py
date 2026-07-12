
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.apogeedetectservice import ApogeeDetectServiceManager

namespace = '/apogeedetectservice'

def register_apogeedetectservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to apogeedetectservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from apogeedetectservice namespace", sid)

    
    @sio.on('newapogeedetected', namespace=namespace)
    async def get_newapogeedetected(sid, data):
        try:
            manager = ApogeeDetectServiceManager()
            response = manager.get_newapogeedetected()
            await sio.emit('newapogeedetected', 
                          {'event_name': 'newapogeedetected', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newapogeedetected: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newmainparachutedetected', namespace=namespace)
    async def get_newmainparachutedetected(sid, data):
        try:
            manager = ApogeeDetectServiceManager()
            response = manager.get_newmainparachutedetected()
            await sio.emit('newmainparachutedetected', 
                          {'event_name': 'newmainparachutedetected', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newmainparachutedetected: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
