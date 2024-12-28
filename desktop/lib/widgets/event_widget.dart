import 'package:flutter/material.dart';

class EventWidget extends StatelessWidget {
  final String eventName;
  final int eventId;

  const EventWidget({
    super.key,
    required this.eventName,
    required this.eventId,
  });

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
                      text: "$eventName\n",
                      style: const TextStyle(
                        color: Colors.black87,
                        fontSize: 20,
                      ),
                    ),
                    TextSpan(
                      text: "Event ID: $eventId",
                      style: const TextStyle(
                        color: Colors.black87,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
              )

            ],
          ),
          const SizedBox(height: 24),
          const Text(
            "Result: ",
            style: TextStyle(
              color: Colors.black87,
              fontSize: 20,
            ),
          ),
        ],
      ),
    );
  }
}
