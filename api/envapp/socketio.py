
from socketio import AsyncServer
from loguru import logger
from proxy.app.services.envapp import EnvAppManager

namespace = '/envapp'

def register_envapp_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to envapp namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        logger.info("Client %s disconnected from envapp namespace", sid)

    
    @sio.on('newboardtempevent1', namespace=namespace)
    async def get_newboardtempevent1(sid, data):
        try:
            manager = EnvAppManager()
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
            manager = EnvAppManager()
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
            manager = EnvAppManager()
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
    
    @sio.on('newdpressevent', namespace=namespace)
    async def get_newdpressevent(sid, data):
        try:
            manager = EnvAppManager()
            response = manager.get_newdpressevent()
            await sio.emit('newdpressevent', 
                          {'event_name': 'newdpressevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newdpressevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newpressevent', namespace=namespace)
    async def get_newpressevent(sid, data):
        try:
            manager = EnvAppManager()
            response = manager.get_newpressevent()
            await sio.emit('newpressevent', 
                          {'event_name': 'newpressevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newpressevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newtempevent_1', namespace=namespace)
    async def get_newtempevent_1(sid, data):
        try:
            manager = EnvAppManager()
            response = manager.get_newtempevent_1()
            await sio.emit('newtempevent_1', 
                          {'event_name': 'newtempevent_1', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newtempevent_1: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newtempevent_2', namespace=namespace)
    async def get_newtempevent_2(sid, data):
        try:
            manager = EnvAppManager()
            response = manager.get_newtempevent_2()
            await sio.emit('newtempevent_2', 
                          {'event_name': 'newtempevent_2', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newtempevent_2: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newtempevent_3', namespace=namespace)
    async def get_newtempevent_3(sid, data):
        try:
            manager = EnvAppManager()
            response = manager.get_newtempevent_3()
            await sio.emit('newtempevent_3', 
                          {'event_name': 'newtempevent_3', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newtempevent_3: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newtensoevent', namespace=namespace)
    async def get_newtensoevent(sid, data):
        try:
            manager = EnvAppManager()
            response = manager.get_newtensoevent()
            await sio.emit('newtensoevent', 
                          {'event_name': 'newtensoevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            logger.exception("Error handling event newtensoevent: %s", e)
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
