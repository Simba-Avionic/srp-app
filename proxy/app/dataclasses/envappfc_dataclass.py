from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Sint16,
)
from .structs import (
    BME280DataStructure,
)

@dataclass
class NewBoardTempEvent_1Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewBoardTempEvent_2Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewBoardTempEvent_3Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewBME280EventOut(SomeIpPayload):
    data: BME280DataStructure
    def __init__(self):
        self.data = BME280DataStructure()

    def from_json(self, json_argument):
        self.data.from_json(json_argument)

    def deserialize(self, payload: bytes):
        self.data.deserialize(payload)
        return self