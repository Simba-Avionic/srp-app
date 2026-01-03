from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Bool,
    Uint8,
)

@dataclass
class OpenReefedParachuteIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class OpenReefedParachuteOut(SomeIpPayload):
    data: Bool
    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
        self.data.value = bool(json_argument)

@dataclass
class UnreefeParachuteIn(SomeIpPayload):
    data: bytes = b''


@dataclass
class UnreefeParachuteOut(SomeIpPayload):
    data: Bool
    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
        self.data.value = bool(json_argument)

@dataclass
class NewParachuteStatusEventOut(SomeIpPayload):
    data: Uint8
    def __init__(self):
        self.data = Uint8()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)