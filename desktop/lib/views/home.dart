import 'package:flutter/material.dart';
import '../widgets/service_widget.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> serviceData = {
      "serviceName": "Engine Service",
      "serviceId": 518,
      "methods": [
        {"name": "Start", "id": 1, "in_type": "void"},
        {"name": "SetMode", "id": 2, "in_type": "uint8"},
      ],
      "events": [
        {"name": "CurrentMode", "id": 32769},
      ],
    };

    final Map<String, dynamic> envService = {
      "serviceName": "Env Service",
      "serviceId": 514,
      "methods": {},
      "events": [
        {"name": "newTempEvent_1", "id": 32769},
        {"name": "newTempEvent_2", "id": 32770},
        {"name": "newTempEvent_3", "id": 32771},
        {"name": "newPressEvent", "id": 32773},
        {"name": "newDPressEvent", "id": 32774},
      ],
    };



    return Container(
      color: Colors.white,
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ServiceWidget(
                  serviceName: serviceData['serviceName'],
                  serviceId: serviceData['serviceId'],
                  methods: serviceData['methods'],
                  events: serviceData['events'],
                ),

                ServiceWidget(
                  serviceName: envService['serviceName'],
                  serviceId: envService['serviceId'],
                  events: envService['events'],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
