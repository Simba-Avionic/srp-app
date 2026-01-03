from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Sint16,
    Uint16,
)
from .structs import (
    PressCalibrationRes,
)

@dataclass
class calPressureSensorIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class calPressureSensorOut(SomeIpPayload):
    data: PressCalibrationRes
    def __init__(self):
        self.data = PressCalibrationRes()

    def from_json(self, json_argument):
        self.data.from_json(json_argument)

@dataclass
class newTempEvent_1Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)

@dataclass
class newTempEvent_2Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)

@dataclass
class newTempEvent_3Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)

@dataclass
class newPressEventOut(SomeIpPayload):
    data: Uint16
    def __init__(self):
        self.data = Uint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)