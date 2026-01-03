from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
)
from .structs import (
    GPSDataStructure,
)

@dataclass
class GPSStatusEventOut(SomeIpPayload):
    data: GPSDataStructure
    def __init__(self):
        self.data = GPSDataStructure()

    def from_json(self, json_argument):
        self.data.from_json(json_argument)