
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

    
    @socketio.on('currentmode', namespace=namespace)
    def callback_currentmode_msg(message):
        try:
            print("w")
            manager = EngineServiceManager()
            response = manager.get_currentmode()
            emit('currentmode', {'event_name': 'callback_currentmode_msg', 'response': response+1})
        except Exception as e:
            emit('event_error', {'error': str(e)})

