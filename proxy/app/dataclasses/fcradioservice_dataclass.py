from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
)
from .structs import (
    RadioDataType,
)

@dataclass
class RadioStatusEventOut(SomeIpPayload):
    data: RadioDataType
    def __init__(self):
        self.data = RadioDataType()

    def from_json(self, json_argument):
        self.data.from_json(json_argument)

    def deserialize(self, payload: bytes):
        self.data.deserialize(payload)
        return self