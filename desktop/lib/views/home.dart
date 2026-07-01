import 'package:flutter/material.dart';
import 'package:flutter_staggered_grid_view/flutter_staggered_grid_view.dart';
import '../widgets/service_widget.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    // --- Oxidizer EC ---
    final Map<String, dynamic> EngineService = {
      "serviceName": "EngineService",
      "serviceId": 518,
      "methods": [
        {"name": "SetMode", "id": 2, "in_type": "uint8"}
      ],
      "events": [
        {"name": "CurrentMode", "id": 32769}
      ]
    };

    final Map<String, dynamic> EnvApp = {
      "serviceName": "EnvApp",
      "serviceId": 514,
      "events": [
        {"name": "newTempEvent_1", "id": 32769},
        {"name": "newTempEvent_2", "id": 32770},
        {"name": "newTempEvent_3", "id": 32771},
        {"name": "newOxidizerPressEvent", "id": 32772},
        {"name": "newPressureFeedPressEvent", "id": 32773},
        {"name": "newChamberPressEvent1", "id": 32774},
        {"name": "newBoardTempEvent1", "id": 32775},
        {"name": "newBoardTempEvent2", "id": 32776},
        {"name": "newBoardTempEvent3", "id": 32777}
      ]
    };

    final Map<String, dynamic> ServoService = {
      "serviceName": "ServoService",
      "serviceId": 515,
      "methods": [
        {"name": "SetOxidizerMainValve", "id": 1, "in_type": "uint8"},
        {"name": "SetOxidizerVentValve", "id": 3, "in_type": "uint8"},
        {"name": "SetOxidizerDumpValve", "id": 5, "in_type": "uint8"},
        {"name": "SetPressureFeedMainValve", "id": 7, "in_type": "uint8"},
        {"name": "SetPressureFeedVentValve", "id": 9, "in_type": "uint8"}
      ],
      "events": [
        {"name": "newOxidizerMainValveEvent", "id": 32769},
        {"name": "newOxidizerVentValveEvent", "id": 32770},
        {"name": "newOxidizerDumpValveEvent", "id": 32771},
        {"name": "newPressureFeedMainEvent", "id": 32772},
        {"name": "newPressureFeedVentEvent", "id": 32773}
      ]
    };

    final Map<String, dynamic> FileLoggerApp = {
      "serviceName": "FileLoggerApp",
      "serviceId": 517,
      "methods": [
        {"name": "Start", "id": 1, "in_type": "void"},
        {"name": "Stop", "id": 2, "in_type": "void"}
      ],
      "events": [
        {"name": "LoggingState", "id": 32769}
      ]
    };

    final Map<String, dynamic> PrimerService = {
      "serviceName": "PrimerService",
      "serviceId": 516,
      "methods": [
        {"name": "StartPrime", "id": 3, "in_type": "void"}
      ],
      "events": [
        {"name": "primeStatusEvent", "id": 32769}
      ]
    };

    final Map<String, dynamic> SysStatService = {
      "serviceName": "SysStatService",
      "serviceId": 522,
      "events": [
        {"name": "NewSystemUsage", "id": 32769}
      ]
    };

    // --- Sec EC ---
    final Map<String, dynamic> SecEnvApp = {
      "serviceName": "SecEnvApp",
      "serviceId": 526,
      "events": [
        {"name": "newEthanolPressEvent", "id": 32772},
        {"name": "newChamberPressEvent2", "id": 32773},
        {"name": "newChamberPressEvent3", "id": 32774},
        {"name": "newBoardTempEvent1", "id": 32775},
        {"name": "newBoardTempEvent2", "id": 32776},
        {"name": "newBoardTempEvent3", "id": 32777}
      ]
    };

    final Map<String, dynamic> SecServoService = {
      "serviceName": "SecServoService",
      "serviceId": 525,
      "methods": [
        {"name": "SetEtanolMainValve", "id": 1, "in_type": "uint8"},
        {"name": "SetEthanolVentValve", "id": 2, "in_type": "uint8"}
      ],
      "events": [
        {"name": "newEthanolMainValveEvent", "id": 32769},
        {"name": "newEthanolVentValveEvent", "id": 32770}
      ]
    };

    // --- FC ---
    final Map<String, dynamic> MainService = {
      "serviceName": "MainService",
      "serviceId": 521,
      "methods": [
        {"name": "SetMode", "id": 1, "in_type": "uint8"}
      ],
      "events": [
        {"name": "CurrentModeStatusEvent", "id": 32769}
      ]
    };

    final Map<String, dynamic> EnvAppFc = {
      "serviceName": "EnvAppFc",
      "serviceId": 529,
      "events": [
        {"name": "newBoardTempEvent_1", "id": 32769},
        {"name": "newBoardTempEvent_2", "id": 32770},
        {"name": "newBoardTempEvent_3", "id": 32771},
        {"name": "newBME280Event", "id": 32772},
        {"name": "newIMUEvent", "id": 32773}
      ]
    };

    final Map<String, dynamic> GPSService = {
      "serviceName": "GPSService",
      "serviceId": 519,
      "events": [
        {"name": "GPSStatusEvent", "id": 32769},
        {"name": "GPSRMCStatusEvent", "id": 32770},
        {"name": "GPSVTGStatusEvent", "id": 32771}
      ]
    };

    final Map<String, dynamic> RadioService = {
      "serviceName": "RadioService",
      "serviceId": 530,
      "events": [
        {"name": "RadioStatusEvent", "id": 32769}
      ]
    };

    final Map<String, dynamic> FcRadioService = {
      "serviceName": "FcRadioService",
      "serviceId": 545,
      "events": [
        {"name": "RadioStatusEvent", "id": 32769}
      ]
    };

    final Map<String, dynamic> FcFileLoggerApp = {
      "serviceName": "FcFileLoggerApp",
      "serviceId": 531,
      "methods": [
        {"name": "Start", "id": 1, "in_type": "void"},
        {"name": "Stop", "id": 2, "in_type": "void"}
      ],
      "events": [
        {"name": "LoggingState", "id": 32769}
      ]
    };

    final Map<String, dynamic> FcSysStatService = {
      "serviceName": "FcSysStatService",
      "serviceId": 523,
      "events": [
        {"name": "NewSystemUsage", "id": 32769}
      ]
    };

    final Map<String, dynamic> RecoveryService = {
      "serviceName": "RecoveryService",
      "serviceId": 520,
      "methods": [
        {"name": "OpenReefedParachute", "id": 1, "in_type": "void"},
        {"name": "UnreefeParachute", "id": 2, "in_type": "void"}
      ],
      "events": [
        {"name": "NewParachuteStatusEvent", "id": 32769}
      ]
    };

    final Map<String, dynamic> ApogeeDetectService = {
      "serviceName": "ApogeeDetectService",
      "serviceId": 555,
      "events": [
        {"name": "newApogeeDetected", "id": 32769},
        {"name": "newMainParachuteDetected", "id": 32770}
      ]
    };

    final services = [
      // Oxidizer EC
      EngineService,
      EnvApp,
      ServoService,
      FileLoggerApp,
      PrimerService,
      SysStatService,
      // Sec EC
      SecEnvApp,
      SecServoService,
      // FC
      MainService,
      EnvAppFc,
      GPSService,
      RadioService,
      FcRadioService,
      FcFileLoggerApp,
      FcSysStatService,
      RecoveryService,
      ApogeeDetectService,
    ];

    return Container(
      color: Colors.white,
      padding: const EdgeInsets.all(24),
      child: MasonryGridView.count(
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        crossAxisCount: 3,
        mainAxisSpacing: 20,
        crossAxisSpacing: 20,
        itemCount: services.length,
        itemBuilder: (context, index) {
          final service = services[index];
          return ServiceWidget(
            serviceName: service['serviceName'],
            serviceId: service['serviceId'],
            events: service['events'] != null
                ? List<Map<String, dynamic>>.from(service['events'])
                : null,
            methods: service['methods'] != null
                ? List<Map<String, dynamic>>.from(service['methods'])
                : null,
          );
        },
      ),
    );
  }
}
