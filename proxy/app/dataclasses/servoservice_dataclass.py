from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Bool,
    Uint8
)


@dataclass
class SetMainServoValueIn(SomeIpPayload):
    data: Uint8

    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class SetMainServoValueOut(SomeIpPayload):
    data: Bool

    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
         self.data.value = bool(json_argument)



@dataclass
class ReadMainServoValueIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class ReadMainServoValueOut(SomeIpPayload):
    data: Uint8

    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
         self.data.value = int(json_argument)



@dataclass
class SetVentServoValueIn(SomeIpPayload):
    data: Uint8

    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class SetVentServoValueOut(SomeIpPayload):
    data: Bool

    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
         self.data.value = bool(json_argument)



@dataclass
class ReadVentServoValueIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class ReadVentServoValueOut(SomeIpPayload):
    data: Uint8

    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
         self.data.value = int(json_argument)



@dataclass
class ServoStatusEventIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class ServoStatusEventOut(SomeIpPayload):
    data: Uint8

    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
         self.data.value = int(json_argument)



@dataclass
class ServoVentStatusEventIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class ServoVentStatusEventOut(SomeIpPayload):
    data: Uint8

    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
         self.data.value = int(json_argument)
