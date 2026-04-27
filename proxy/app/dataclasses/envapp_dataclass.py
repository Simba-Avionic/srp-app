from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Float32,
    Sint16,
    Uint16,
)

@dataclass
class GetTankPressureIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class GetTankPressureOut(SomeIpPayload):
    data: Uint16
    def __init__(self):
        self.data = Uint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class GetUpperTankTempIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class GetUpperTankTempOut(SomeIpPayload):
    data: Uint16
    def __init__(self):
        self.data = Uint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class GetLowerTankTempIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class GetLowerTankTempOut(SomeIpPayload):
    data: Uint16
    def __init__(self):
        self.data = Uint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewTempEvent_1Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewTempEvent_2Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewTempEvent_3Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewPressEventOut(SomeIpPayload):
    data: Uint16
    def __init__(self):
        self.data = Uint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewDPressEventOut(SomeIpPayload):
    data: Uint16
    def __init__(self):
        self.data = Uint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


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


@dataclass
class NewTensoEventOut(SomeIpPayload):
    data: Float32
    def __init__(self):
        self.data = Float32()

    def from_json(self, json_argument):
        self.data.value = float(json_argument)
