
from socketio import AsyncServer
from proxy.app.services.envservice import EnvServiceManager

namespace = '/env'

def register_env_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to env namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        print(f"Client {sid} disconnected from env namespace")

    
    @sio.on('newdpressevent', namespace=namespace)
    async def get_newdpressevent(sid, data):
        try:
            manager = EnvServiceManager()
            response = manager.get_newdpressevent()
            await sio.emit('newdpressevent', 
                          {'event_name': 'newdpressevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newpressevent', namespace=namespace)
    async def get_newpressevent(sid, data):
        try:
            manager = EnvServiceManager()
            response = manager.get_newpressevent()
            await sio.emit('newpressevent', 
                          {'event_name': 'newpressevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newtempevent_1', namespace=namespace)
    async def get_newtempevent_1(sid, data):
        try:
            manager = EnvServiceManager()
            response = manager.get_newtempevent_1()
            await sio.emit('newtempevent_1', 
                          {'event_name': 'newtempevent_1', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newtempevent_2', namespace=namespace)
    async def get_newtempevent_2(sid, data):
        try:
            manager = EnvServiceManager()
            response = manager.get_newtempevent_2()
            await sio.emit('newtempevent_2', 
                          {'event_name': 'newtempevent_2', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('newtempevent_3', namespace=namespace)
    async def get_newtempevent_3(sid, data):
        try:
            manager = EnvServiceManager()
            response = manager.get_newtempevent_3()
            await sio.emit('newtempevent_3', 
                          {'event_name': 'newtempevent_3', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
