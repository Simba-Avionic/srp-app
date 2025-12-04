
from socketio import AsyncServer
from proxy.app.services.primerservice import PrimerServiceManager

namespace = '/primerservice'

def register_primerservice_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to primerservice namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        print(f"Client {sid} disconnected from primerservice namespace")

    
    @sio.on('primestatusevent', namespace=namespace)
    async def get_primestatusevent(sid, data):
        try:
            manager = PrimerServiceManager()
            response = manager.get_primestatusevent()
            await sio.emit('primestatusevent', 
                          {'event_name': 'primestatusevent', 'response': response},
                          room=sid,
                          namespace=namespace)
        except Exception as e:
            await sio.emit('event_error',
                          {'error': str(e)},
                          room=sid,
                          namespace=namespace)
    
