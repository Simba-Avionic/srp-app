
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.secenvapp import SecEnvAppManager

namespace = '/secenvapp'

def register_secenvapp_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to secenvapp namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from secenvapp namespace", sid)

    
    @sio.on('newboardtempevent1', namespace=namespace)
    async def get_newboardtempevent1(sid, data):
        try:
            manager = SecEnvAppManager()
            response = manager.get_newboardtempevent1()
            await sio.emit('newboardtempevent1', 
                          {'event_name': 'newboardtempevent1', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newboardtempevent1: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newboardtempevent2', namespace=namespace)
    async def get_newboardtempevent2(sid, data):
        try:
            manager = SecEnvAppManager()
            response = manager.get_newboardtempevent2()
            await sio.emit('newboardtempevent2', 
                          {'event_name': 'newboardtempevent2', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newboardtempevent2: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newboardtempevent3', namespace=namespace)
    async def get_newboardtempevent3(sid, data):
        try:
            manager = SecEnvAppManager()
            response = manager.get_newboardtempevent3()
            await sio.emit('newboardtempevent3', 
                          {'event_name': 'newboardtempevent3', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newboardtempevent3: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newchamberpressevent2', namespace=namespace)
    async def get_newchamberpressevent2(sid, data):
        try:
            manager = SecEnvAppManager()
            response = manager.get_newchamberpressevent2()
            await sio.emit('newchamberpressevent2', 
                          {'event_name': 'newchamberpressevent2', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newchamberpressevent2: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newchamberpressevent3', namespace=namespace)
    async def get_newchamberpressevent3(sid, data):
        try:
            manager = SecEnvAppManager()
            response = manager.get_newchamberpressevent3()
            await sio.emit('newchamberpressevent3', 
                          {'event_name': 'newchamberpressevent3', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newchamberpressevent3: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newethanolpressevent', namespace=namespace)
    async def get_newethanolpressevent(sid, data):
        try:
            manager = SecEnvAppManager()
            response = manager.get_newethanolpressevent()
            await sio.emit('newethanolpressevent', 
                          {'event_name': 'newethanolpressevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newethanolpressevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
