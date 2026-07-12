import 'package:flutter/material.dart';
import 'package:desktop/services/event_service.dart';
import 'package:desktop/utils/format_utils.dart';
import 'package:desktop/utils/moving_average.dart';

class EventWidget extends StatefulWidget {
  final String eventName;
  final int eventId;
  final String namespace;

  const EventWidget({
    super.key,
    required this.eventName,
    required this.eventId,
    required this.namespace,
  });

  @override
  _EventWidgetState createState() => _EventWidgetState();
}

class _EventWidgetState extends State<EventWidget> {
  final EventService eventService = EventService();
  String response = "-";
  MovingAverage? _movingAverage;

  bool get _isPressureEvent =>
      widget.eventName.toLowerCase().contains('pressevent');

  @override
  void initState() {
    super.initState();
    if (_isPressureEvent) {
      _movingAverage = MovingAverage(40);
    }
    eventService.initializeSocket(
        widget.namespace, widget.eventName.toLowerCase());
    eventService.connect();

    eventService.onEventResponse((msg) {
      setState(() {
        response = _formatEventValue(msg);
      });
    });
  }

  String _formatEventValue(dynamic msg) {
    if (_isPressureEvent) {
      final parsed = parseNumericValue(msg);
      if (parsed != null) {
        if (_movingAverage != null) {
          return formatDisplayValue(_movingAverage!.add(parsed));
        }
        return formatDisplayValue(parsed);
      }
    }
    return formatDisplayValue(msg);
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 5,
            child: Text(
              widget.eventName,
              style: const TextStyle(
                color: Colors.black87,
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            flex: 4,
            child: Text(
              response,
              style: const TextStyle(
                color: Colors.black54,
                fontSize: 12,
              ),
              overflow: TextOverflow.ellipsis,
              maxLines: 2,
            ),
          ),
        ],
      ),
    );
  }
}
