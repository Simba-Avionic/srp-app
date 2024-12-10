
import socketio
from flask_socketio import emit
from proxy.app.parser.services.engineservice import EngineServiceManager

namespace = '/engine'

def register_socketio_handlers(socketio):
    @socketio.on('connect', namespace=namespace)
    def connect():
        emit('connected', {"message": "Connected to engine namespace"})

    @socketio.on('disconnect', namespace=namespace)
    def disconnect():
        print("Client disconnected from engine namespace")

    
@socketio.on('callback_currentmode_msg', namespace=namespace)
def callback_currentmode_msg(message):
    try:
        response = manager.callback_currentmode_msg(message)
        emit('event_response', {"event_name": 'callback_currentmode_msg', "response": response})
    except Exception as e:
        emit('event_error', {"error": str(e)})

