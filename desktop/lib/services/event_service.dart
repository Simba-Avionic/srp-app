import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'dart:async';
import 'dart:convert';

class EventService {
  late IO.Socket _socket;
  void Function(String)? _eventCallback;
  String? _event;

  void initializeSocket(String namespace, String event) {
    _event = event;

    _socket = IO.io(
      'http://127.0.0.1:5000/$namespace',
      IO.OptionBuilder()
          .setTransports(['websocket'])
          .build(),
    );

    _socket.onConnect((_) {
      print('Connected to server at $namespace');
      _requestEvent();
    });

    _socket.on(event, (msg) {
      print('Received $event response: $msg');

      try {
        var responseData = msg is String ? jsonDecode(msg) : msg;
        if (responseData is Map<String, dynamic> && responseData.containsKey('response')) {
          var responseValue = responseData['response'];

          if (_eventCallback != null) {
            _eventCallback!(responseValue.toString());
          }
        } else {
          print('Response data is not in the expected format: $responseData');
        }
      } catch (e) {
        print('Error parsing $event response: $e');
      }
    });

    _socket.onConnectError((err) {
      print('Connection error: $err');
    });

    _socket.onError((err) {
      print('Socket error: $err');
    });
  }

  void connect() {
    _socket.connect();
  }

  void disconnect() {
    _socket.disconnect();
  }

  void onEventResponse(void Function(String) callback) {
    _eventCallback = callback;
  }

  void _requestEvent() async {
    while (_socket.connected) {
      await Future.delayed(const Duration(milliseconds: 100));
      if (_event != null) {
        _socket.emit(_event!, 'Requesting event data');
      }
    }
  }
}
