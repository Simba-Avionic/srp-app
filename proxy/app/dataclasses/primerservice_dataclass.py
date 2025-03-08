from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Bool,
    Uint8
)


@dataclass
class OnPrimeIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class OnPrimeOut(SomeIpPayload):
    data: Bool

    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
         self.data.value = bool(json_argument)



@dataclass
class OffPrimeIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class OffPrimeOut(SomeIpPayload):
    data: Bool

    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
         self.data.value = bool(json_argument)



@dataclass
class StartPrimeIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class StartPrimeOut(SomeIpPayload):
    data: Bool

    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
         self.data.value = bool(json_argument)



@dataclass
class primeStatusEventIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class primeStatusEventOut(SomeIpPayload):
    data: Uint8

    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
         self.data.value = int(json_argument)
