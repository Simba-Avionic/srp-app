
from socketio import AsyncServer
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
        print(f"Client {sid} disconnected from servoservice namespace")

    
    @sio.on('servostatusevent', namespace=namespace)
    async def get_servostatusevent(sid, data):
        try:
            manager = ServoServiceManager()
            response = manager.get_servostatusevent()
            await sio.emit('servostatusevent', 
                          {'event_name': 'servostatusevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
    @sio.on('servoventstatusevent', namespace=namespace)
    async def get_servoventstatusevent(sid, data):
        try:
            manager = ServoServiceManager()
            response = manager.get_servoventstatusevent()
            await sio.emit('servoventstatusevent', 
                          {'event_name': 'servoventstatusevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
