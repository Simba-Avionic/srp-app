
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.servoservice import ServoServiceManager

namespace = '/servoservice'

def register_servoservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to servoservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from servoservice namespace", sid)

    
    @sio.on('newoxidizerdumpvalveevent', namespace=namespace)
    async def get_newoxidizerdumpvalveevent(sid, data):
        try:
            manager = ServoServiceManager()
            response = manager.get_newoxidizerdumpvalveevent()
            await sio.emit('newoxidizerdumpvalveevent', 
                          {'event_name': 'newoxidizerdumpvalveevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newoxidizerdumpvalveevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newoxidizermainvalveevent', namespace=namespace)
    async def get_newoxidizermainvalveevent(sid, data):
        try:
            manager = ServoServiceManager()
            response = manager.get_newoxidizermainvalveevent()
            await sio.emit('newoxidizermainvalveevent', 
                          {'event_name': 'newoxidizermainvalveevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newoxidizermainvalveevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newoxidizerventvalveevent', namespace=namespace)
    async def get_newoxidizerventvalveevent(sid, data):
        try:
            manager = ServoServiceManager()
            response = manager.get_newoxidizerventvalveevent()
            await sio.emit('newoxidizerventvalveevent', 
                          {'event_name': 'newoxidizerventvalveevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newoxidizerventvalveevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newpressurefeedmainevent', namespace=namespace)
    async def get_newpressurefeedmainevent(sid, data):
        try:
            manager = ServoServiceManager()
            response = manager.get_newpressurefeedmainevent()
            await sio.emit('newpressurefeedmainevent', 
                          {'event_name': 'newpressurefeedmainevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newpressurefeedmainevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newpressurefeedventevent', namespace=namespace)
    async def get_newpressurefeedventevent(sid, data):
        try:
            manager = ServoServiceManager()
            response = manager.get_newpressurefeedventevent()
            await sio.emit('newpressurefeedventevent', 
                          {'event_name': 'newpressurefeedventevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newpressurefeedventevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
