import 'package:flutter/material.dart';
import 'package:desktop/services/event_service.dart';

class EventWidget extends StatefulWidget {
  final String eventName;
  final int eventId;
  final String namespace;

  const EventWidget({
    super.key,
    required this.eventName,
    required this.eventId,
    required this.namespace
  });

  @override
  _EventWidgetState createState() => _EventWidgetState();
}

class _EventWidgetState extends State<EventWidget> {
  final EventService eventService = EventService();
  String response = "No response yet";

  @override
  void initState() {
    super.initState();
    eventService.initializeSocket(widget.namespace, widget.eventName.toLowerCase());
    eventService.connect();

    eventService.onEventResponse((msg) {
      setState(() {
        response = msg;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8.0),
        boxShadow: const [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 4.0,
            offset: Offset(0, 2),
          ),
        ],
      ),
      padding: const EdgeInsets.all(12.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.data_object_rounded, color: Colors.black54),
              const SizedBox(width: 8),
              RichText(
                text: TextSpan(
                  children: [
                    TextSpan(
                      text: "${widget.eventName}\n",
                      style: const TextStyle(
                        color: Colors.black87,
                        fontSize: 20,
                      ),
                    ),
                    TextSpan(
                      text: "Event ID: ${widget.eventId}",
                      style: const TextStyle(
                        color: Colors.black87,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          Text(
            "Result: $response",
            style: const TextStyle(
              color: Colors.black87,
              fontSize: 20,
            ),
          ),
        ],
      ),
    );
  }
}
