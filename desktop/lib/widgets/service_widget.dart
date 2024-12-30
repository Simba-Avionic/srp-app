import 'package:flutter/material.dart';
import 'method_widget.dart';
import 'event_widget.dart';

class ServiceWidget extends StatelessWidget {
  final String serviceName;
  final int serviceId;
  final List<Map<String, dynamic>>? methods;
  final List<Map<String, dynamic>>? events;

  const ServiceWidget({
    super.key,
    required this.serviceName,
    required this.serviceId,
    this.methods,
    this.events,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: MediaQuery.of(context).size.width / 2 - 200,
      decoration: BoxDecoration(
        color: Theme.of(context).secondaryHeaderColor,
        borderRadius: BorderRadius.circular(16.0),
      ),
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.settings, color: Colors.white),
              const SizedBox(width: 8),
              Text(
                "$serviceName\nService ID: $serviceId",
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          if (methods != null && methods!.isNotEmpty)...[
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: methods!.map<Widget>(
                    (method) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8.0),
                    child: MethodWidget(
                      methodName: method['name'],
                      methodId: method['id'],
                      inType: method['in_type'],
                      namespace: 'engine',
                    ),
                  );
                },
              ).toList(),
            ),
            const SizedBox(height: 16),
          ],

          if (events != null && events!.isNotEmpty)
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: events!.map<Widget>(
                    (event) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8.0),
                    child: EventWidget(
                      eventName: event['name'],
                      eventId: event['id'],
                      namespace: 'engine',
                    ),
                  );
                },
              ).toList(),
            ),
        ],
      ),
    );
  }
}
