from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Bool,
)

@dataclass
class NewApogeeDetectedOut(SomeIpPayload):
    data: Bool
    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
        self.data.value = bool(json_argument)


@dataclass
class NewMainParachuteDetectedOut(SomeIpPayload):
    data: Bool
    def __init__(self):
        self.data = Bool()

    def from_json(self, json_argument):
        self.data.value = bool(json_argument)
