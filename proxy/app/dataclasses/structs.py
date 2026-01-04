from dataclasses import dataclass
from someipy.serialization import (
    Float32,
)

@dataclass
class PressCalibrationRes:
    a: Float32
    b: Float32

    def __init__(self):
        self.a = Float32()
        self.b = Float32()

    def from_json(self, json_obj):
        self.a.value = float(json_obj['a'])
        self.b.value = float(json_obj['b'])

    def deserialize(self, payload: bytes):
        self.a.deserialize(payload[0:4])
        self.b.deserialize(payload[4:8])

@dataclass
class GPSDataStructure:
    latitude: Float32
    longitude: Float32
    altitude: Float32

    def __init__(self):
        self.latitude = Float32()
        self.longitude = Float32()
        self.altitude = Float32()

    def from_json(self, json_obj):
        self.latitude.value = float(json_obj['latitude'])
        self.longitude.value = float(json_obj['longitude'])
        self.altitude.value = float(json_obj['altitude'])

    def deserialize(self, payload: bytes):
        self.latitude.deserialize(payload[0:4])
        self.longitude.deserialize(payload[4:8])
        self.altitude.deserialize(payload[8:12])