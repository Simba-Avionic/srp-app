import 'package:flutter/material.dart';
import '../widgets/service_widget.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> EngineService = {
      "serviceName": "EngineService",
      "serviceId": 518,
      "methods": [
        { "name": "Start", "id": 1, "in_type": "void"},
        { "name": "SetMode", "id": 2, "in_type": "uint8"}],
      "events": [
        {"name": "CurrentMode", "id": 32769}]
    };

    final Map<String, dynamic> EnvApp = {
      "serviceName": "EnvApp",
      "serviceId": 514,
      "events": [
        { "name": "newTempEvent_1",  "id": 32769 },
        { "name": "newTempEvent_2", "id": 32770},
        { "name": "newTempEvent_3", "id": 32771},
        { "name": "newPressEvent", "id": 32772},
        { "name": "newDPressEvent", "id": 32773}
      ]
    };

    final Map<String, dynamic> ServoService = {
      "serviceName": "ServoService",
      "serviceId": 515,
      "methods": [
        {"name": "SetMainServoValue",  "id": 1,  "in_type": "uint8"},
        {"name": "ReadMainServoValue", "id": 2, "in_type": "void"},
        {"name": "SetVentServoValue", "id": 3, "in_type": "uint8"},
        {"name": "ReadVentServoValue", "id": 4, "in_type": "void"}
      ],
      "events": [
        { "name": "ServoStatusEvent", "id": 32769},
        { "name": "ServoVentStatusEvent", "id": 32770}
      ]
    };

    final Map<String, dynamic> FileLoggerApp = {
      "serviceName": "FileLoggerApp",
      "serviceId": 517,
      "methods": [
        { "name": "Start", "id": 1, "in_type": "void"},
        {"name": "Stop", "id": 2, "in_type": "void"}
      ]
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
                  serviceName: EngineService['serviceName'],
                  serviceId: EngineService['serviceId'],
                  methods: EngineService['methods'],
                  events: EngineService['events'],
                ),

                ServiceWidget(
                  serviceName: EnvApp['serviceName'],
                  serviceId: EnvApp['serviceId'],
                  events: EnvApp['events'],
                  methods: EnvApp['methods'],
                ),
                ]
              ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ServiceWidget(
                  serviceName: ServoService['serviceName'],
                  serviceId: ServoService['serviceId'],
                  events: ServoService['events'],
                  methods: ServoService['methods'],
                ),

                ServiceWidget(
                  serviceName: FileLoggerApp['serviceName'],
                  serviceId: FileLoggerApp['serviceId'],
                  events: FileLoggerApp['events'],
                  methods: FileLoggerApp['methods'],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
