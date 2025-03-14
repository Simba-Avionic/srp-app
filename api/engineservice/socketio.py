
from socketio import AsyncServer
from proxy.app.services.engineservice import EngineServiceManager

namespace = '/engineservice'

def register_engineservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to engineservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        print(f"Client {sid} disconnected from engineservice namespace")

    
    @sio.on('currentmode', namespace=namespace)
    async def get_currentmode(sid, data):
        try:
            manager = EngineServiceManager()
            response = manager.get_currentmode()
            await sio.emit('currentmode', 
                          {'event_name': 'currentmode', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
