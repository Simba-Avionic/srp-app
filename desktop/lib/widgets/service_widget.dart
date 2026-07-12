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
    String namespace = serviceName.toLowerCase().trim();
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).secondaryHeaderColor,
        borderRadius: BorderRadius.circular(12.0),
      ),
      padding: const EdgeInsets.all(12.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.settings, color: Colors.white, size: 20),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  serviceName,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          Text(
            "ID: $serviceId",
            style: const TextStyle(color: Colors.white70, fontSize: 11),
          ),
          if (methods != null && methods!.isNotEmpty) ...[
            const SizedBox(height: 10),
            ...methods!.map(
              (method) => MethodWidget(
                methodName: method['name'],
                methodId: method['id'],
                inType: method['in_type'],
                namespace: namespace,
              ),
            ),
          ],
          if (events != null && events!.isNotEmpty) ...[
            const SizedBox(height: 8),
            Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(8.0),
              ),
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Column(
                children: events!.asMap().entries.map((entry) {
                  final isLast = entry.key == events!.length - 1;
                  return Column(
                    children: [
                      EventWidget(
                        eventName: entry.value['name'],
                        eventId: entry.value['id'],
                        namespace: namespace,
                      ),
                      if (!isLast)
                        const Divider(height: 1, thickness: 0.5, indent: 8, endIndent: 8),
                    ],
                  );
                }).toList(),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
