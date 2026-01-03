from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Bool,
    Uint8,
)

@dataclass
class StartIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class StartOut(SomeIpPayload):
    data: Bool
    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
        self.data.value = bool(json_argument)

@dataclass
class StopIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class StopOut(SomeIpPayload):
    data: Bool
    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
        self.data.value = bool(json_argument)

@dataclass
class LoggingStateOut(SomeIpPayload):
    data: Uint8
    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)