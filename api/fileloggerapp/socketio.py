
from socketio import AsyncServer
from proxy.app.services.fileloggerapp import FileLoggerAppManager

namespace = '/fileloggerapp'

def register_fileloggerapp_socketio(sio: AsyncServer):
    @sio.on('connect', namespace=namespace)
    async def connect(sid, environ):
        await sio.emit('connected', 
                      {"message": "Connected to fileloggerapp namespace"},
                      room=sid,
                      namespace=namespace)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        print(f"Client {sid} disconnected from fileloggerapp namespace")

    
