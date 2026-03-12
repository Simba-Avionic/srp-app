from dataclasses import dataclass
from someipy.serialization import (
    Float32,
)

@dataclass
class SysStatType:
    mem_usage: Float32
    cpu_usage: Float32
    disk_utilization: Float32

    def __init__(self):
        self.mem_usage = Float32()
        self.cpu_usage = Float32()
        self.disk_utilization = Float32()

    def from_json(self, json_obj):
        self.mem_usage.value = float(json_obj['mem_usage'])
        self.cpu_usage.value = float(json_obj['cpu_usage'])
        self.disk_utilization.value = float(json_obj['disk_utilization'])

    def deserialize(self, payload: bytes):
        self.mem_usage.deserialize(payload[0:4])
        self.cpu_usage.deserialize(payload[4:8])
        self.disk_utilization.deserialize(payload[8:12])

@dataclass
class BME280DataStructure:
    temperature: Float32
    humidity: Float32
    altitude: Float32

    def __init__(self):
        self.temperature = Float32()
        self.humidity = Float32()
        self.altitude = Float32()

    def from_json(self, json_obj):
        self.temperature.value = float(json_obj['temperature'])
        self.humidity.value = float(json_obj['humidity'])
        self.altitude.value = float(json_obj['altitude'])

    def deserialize(self, payload: bytes):
        self.temperature.deserialize(payload[0:4])
        self.humidity.deserialize(payload[4:8])
        self.altitude.deserialize(payload[8:12])

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