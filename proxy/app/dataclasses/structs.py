from dataclasses import dataclass
from someipy.serialization import (
    Float32,
)

@dataclass
class PressCalibrationRes:
    a: Float32
    b: Float32

    def from_json(self, json_obj):
        self.a.value = float(json_obj['a'])
        self.b.value = float(json_obj['b'])

@dataclass
class GPSDataStructure:
    latitude: Float32
    longitude: Float32
    altitude: Float32

    def from_json(self, json_obj):
        self.latitude.value = float(json_obj['latitude'])
        self.longitude.value = float(json_obj['longitude'])
        self.altitude.value = float(json_obj['altitude'])