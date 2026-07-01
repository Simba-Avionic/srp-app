from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Float32,
    Sint16,
)

@dataclass
class NewEthanolPressEventOut(SomeIpPayload):
    data: Float32
    def __init__(self):
        self.data = Float32()

    def from_json(self, json_argument):
        self.data.value = float(json_argument)


@dataclass
class NewChamberPressEvent2Out(SomeIpPayload):
    data: Float32
    def __init__(self):
        self.data = Float32()

    def from_json(self, json_argument):
        self.data.value = float(json_argument)


@dataclass
class NewChamberPressEvent3Out(SomeIpPayload):
    data: Float32
    def __init__(self):
        self.data = Float32()

    def from_json(self, json_argument):
        self.data.value = float(json_argument)


@dataclass
class NewBoardTempEvent1Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewBoardTempEvent2Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewBoardTempEvent3Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)
