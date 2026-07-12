from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
)
from .structs import (
    GPSDataStructure,
    GPSRMCDataStructure,
    GPSVTGDataStructure,
)

@dataclass
class GPSStatusEventOut(SomeIpPayload):
    data: GPSDataStructure
    def __init__(self):
        self.data = GPSDataStructure()

    def from_json(self, json_argument):
        self.data.from_json(json_argument)

    def deserialize(self, payload: bytes):
        self.data.deserialize(payload)
        return self

@dataclass
class GPSRMCStatusEventOut(SomeIpPayload):
    data: GPSRMCDataStructure
    def __init__(self):
        self.data = GPSRMCDataStructure()

    def from_json(self, json_argument):
        self.data.from_json(json_argument)

    def deserialize(self, payload: bytes):
        self.data.deserialize(payload)
        return self

@dataclass
class GPSVTGStatusEventOut(SomeIpPayload):
    data: GPSVTGDataStructure
    def __init__(self):
        self.data = GPSVTGDataStructure()

    def from_json(self, json_argument):
        self.data.from_json(json_argument)

    def deserialize(self, payload: bytes):
        self.data.deserialize(payload)
        return self