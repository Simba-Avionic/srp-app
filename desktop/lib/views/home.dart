import 'package:flutter/material.dart';
import 'package:flutter_staggered_grid_view/flutter_staggered_grid_view.dart';
import '../widgets/service_widget.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> EngineService = {
      "serviceName": "EngineService",
      "serviceId": 518,
      "methods": [
        {
          "name": "Start",
          "id": 1,
          "in_type": "void"
        },
        {
          "name": "SetMode",
          "id": 2,
          "in_type": "uint8"
        }
      ],
      "events": [
        {
          "name": "CurrentMode",
          "id": 32769
        }
      ]
    };

    final Map<String, dynamic> EnvApp = {
      "serviceName": "EnvApp",
      "serviceId": 514,
      "events": [
        {
          "name": "newTempEvent_1",
          "id": 32769
        },
        {
          "name": "newTempEvent_2",
          "id": 32770
        },
        {
          "name": "newTempEvent_3",
          "id": 32771
        },
        {
          "name": "newPressEvent",
          "id": 32772
        },
        {
          "name": "newDPressEvent",
          "id": 32773
        },
        {
          "name": "newBoardTempEvent1",
          "id": 32774
        },
        {
          "name": "newBoardTempEvent2",
          "id": 32775
        },
        {
          "name": "newBoardTempEvent3",
          "id": 32776
        }
      ]
    };

    final Map<String, dynamic> EnvAppFc = {
      "serviceName": "EnvAppFc",
      "serviceId": 529,
      "events": [
        {
          "name": "newBoardTempEvent_1",
          "id": 32769
        },
        {
          "name": "newBoardTempEvent_2",
          "id": 32770
        },
        {
          "name": "newBoardTempEvent_3",
          "id": 32771
        },
        {
          "name": "newBME280Event",
          "id": 32772
        }
      ]
    };

    final Map<String, dynamic> GPSService = {
      "serviceName": "GPSService",
      "serviceId": 519,
      "events": [
        {
          "name": "GPSStatusEvent",
          "id": 32769
        }
      ]
    };

    final Map<String, dynamic> MainService = {
      "serviceName": "MainService",
      "serviceId": 521,
      "methods": [
        {
          "name": "setMode",
          "id": 1,
          "in_type": "uint8"
        }
      ],
      "events": [
        {
          "name": "CurrentModeStatusEvent",
          "id": 32769
        }
      ]
    };

    final Map<String, dynamic> RadioService = {
      "serviceName": "RadioService",
      "serviceId": 530
    };

    final Map<String, dynamic> RecoveryService = {
      "serviceName": "RecoveryService",
      "serviceId": 520,
      "methods": [
        {
          "name": "OpenReefedParachute",
          "id": 1,
          "in_type": "void"
        },
        {
          "name": "UnreefeParachute",
          "id": 2,
          "in_type": "void"
        }
      ],
      "events": [
        {
          "name": "NewParachuteStatusEvent",
          "id": 32769
        }
      ]
    };

    final Map<String, dynamic> FcSysStatService = {
      "serviceName": "FcSysStatService",
      "serviceId": 523,
      "events": [
        {
          "name": "NewSystemUsage",
          "id": 32769
        }
      ]
    };

    final Map<String, dynamic> FileLoggerApp = {
      "serviceName": "FileLoggerApp",
      "serviceId": 517,
      "methods": [
        {
          "name": "Start",
          "id": 1,
          "in_type": "void"
        },
        {
          "name": "Stop",
          "id": 2,
          "in_type": "void"
        }
      ],
      "events": [
        {
          "name": "LoggingState",
          "id": 32769
        }
      ]
    };

    final Map<String, dynamic> PrimerService = {
      "serviceName": "PrimerService",
      "serviceId": 516,
      "methods": [
        {
          "name": "OnPrime",
          "id": 1,
          "in_type": "void"
        },
        {
          "name": "OffPrime",
          "id": 2,
          "in_type": "void"
        },
        {
          "name": "StartPrime",
          "id": 3,
          "in_type": "void"
        }
      ],
      "events": [
        {
          "name": "primeStatusEvent",
          "id": 32769
        }
      ]
    };

    final Map<String, dynamic> ServoService = {
      "serviceName": "ServoService",
      "serviceId": 515,
      "methods": [
        {
          "name": "SetMainServoValue",
          "id": 1,
          "in_type": "uint8"
        },
        {
          "name": "ReadMainServoValue",
          "id": 2,
          "in_type": "void"
        },
        {
          "name": "SetVentServoValue",
          "id": 3,
          "in_type": "uint8"
        },
        {
          "name": "ReadVentServoValue",
          "id": 4,
          "in_type": "void"
        },
        {
          "name": "SetDumpValue",
          "id": 5,
          "in_type": "uint8"
        },
        {
          "name": "ReadDumpValue",
          "id": 6,
          "in_type": "void"
        }
      ],
      "events": [
        {
          "name": "ServoStatusEvent",
          "id": 32769
        },
        {
          "name": "ServoVentStatusEvent",
          "id": 32770
        },
        {
          "name": "ServoDumpStatusEvent",
          "id": 32771
        }
      ]
    };

    final Map<String, dynamic> SysStatService = {
      "serviceName": "SysStatService",
      "serviceId": 522,
      "events": [
        {
          "name": "NewSystemUsage",
          "id": 32769
        }
      ]
    };
    final services = [
      EnvApp,
      ServoService,
      FileLoggerApp,
      PrimerService,
      EngineService,
      SysStatService,
      EnvAppFc,
      RecoveryService,
      GPSService,
      FcSysStatService,
    ];

    return Container(
      color: Colors.white,
      padding: const EdgeInsets.all(24),
      child: MasonryGridView.count(
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        crossAxisCount: 2,
        mainAxisSpacing: 20,
        crossAxisSpacing: 20,
        itemCount: services.length,
        itemBuilder: (context, index) {
          final service = services[index];
          return ServiceWidget(
            serviceName: service['serviceName'],
            serviceId: service['serviceId'],
            events: service['events'],
            methods: service['methods'],
          );
        },
      ),
    );
  }
}
