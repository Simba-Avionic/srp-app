from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Bool,
    Uint8
)


@dataclass
class StartIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class StartOut(SomeIpPayload):
    data: Bool

    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
         self.data.value = bool(json_argument)



@dataclass
class SetModeIn(SomeIpPayload):
    data: Uint8

    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class SetModeOut(SomeIpPayload):
    data: Bool

    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
         self.data.value = bool(json_argument)



@dataclass
class CurrentModeIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class CurrentModeOut(SomeIpPayload):
    data: Uint8

    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
         self.data.value = int(json_argument)
