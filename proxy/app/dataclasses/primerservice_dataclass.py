from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Bool,
    Uint8,
)

@dataclass
class OnPrimeIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class OnPrimeOut(SomeIpPayload):
    data: Bool
    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
        self.data.value = bool(json_argument)


@dataclass
class OffPrimeIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class OffPrimeOut(SomeIpPayload):
    data: Bool
    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
        self.data.value = bool(json_argument)


@dataclass
class StartPrimeIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class StartPrimeOut(SomeIpPayload):
    data: Bool
    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
        self.data.value = bool(json_argument)


@dataclass
class GetPrimerStateIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class GetPrimerStateOut(SomeIpPayload):
    data: Uint8
    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class PrimeStatusEventOut(SomeIpPayload):
    data: Uint8
    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)
