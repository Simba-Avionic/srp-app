from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Bool
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
class StopIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''



@dataclass
class StopOut(SomeIpPayload):
    data: Bool

    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
         self.data.value = bool(json_argument)
