const List<Map<String, dynamic>> serviceDefinitions = [
  {
    "serviceName": "EngineService",
    "serviceId": 518,
    "methods": [
      {"name": "SetMode", "id": 2, "in_type": "uint8"}
    ],
    "events": [
      {"name": "CurrentMode", "id": 32769}
    ]
  },
  {
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
  },
  {
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
  },
  {
    "serviceName": "FileLoggerApp",
    "serviceId": 517,
    "methods": [
      {"name": "Start", "id": 1, "in_type": "void"},
      {"name": "Stop", "id": 2, "in_type": "void"}
    ],
    "events": [
      {"name": "LoggingState", "id": 32769}
    ]
  },
  {
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
  },
  {
    "serviceName": "SysStatService",
    "serviceId": 522,
    "events": [
      {"name": "NewSystemUsage", "id": 32769}
    ]
  },
  {
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
  },
  {
    "serviceName": "PrimerService",
    "serviceId": 516,
    "methods": [
      {"name": "StartPrime", "id": 3, "in_type": "void"}
    ],
    "events": [
      {"name": "primeStatusEvent", "id": 32769}
    ]
  },
];
