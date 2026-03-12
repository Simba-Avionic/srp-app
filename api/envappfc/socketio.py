
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.envappfc import EnvAppFcManager

namespace = '/envappfc'

def register_envappfc_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to envappfc namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from envappfc namespace", sid)

    
    @sio.on('newbme280event', namespace=namespace)
    async def get_newbme280event(sid, data):
        try:
            manager = EnvAppFcManager()
            response = manager.get_newbme280event()
            await sio.emit('newbme280event', 
                          {'event_name': 'newbme280event', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newbme280event: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newboardtempevent_1', namespace=namespace)
    async def get_newboardtempevent_1(sid, data):
        try:
            manager = EnvAppFcManager()
            response = manager.get_newboardtempevent_1()
            await sio.emit('newboardtempevent_1', 
                          {'event_name': 'newboardtempevent_1', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newboardtempevent_1: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newboardtempevent_2', namespace=namespace)
    async def get_newboardtempevent_2(sid, data):
        try:
            manager = EnvAppFcManager()
            response = manager.get_newboardtempevent_2()
            await sio.emit('newboardtempevent_2', 
                          {'event_name': 'newboardtempevent_2', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newboardtempevent_2: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newboardtempevent_3', namespace=namespace)
    async def get_newboardtempevent_3(sid, data):
        try:
            manager = EnvAppFcManager()
            response = manager.get_newboardtempevent_3()
            await sio.emit('newboardtempevent_3', 
                          {'event_name': 'newboardtempevent_3', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newboardtempevent_3: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
