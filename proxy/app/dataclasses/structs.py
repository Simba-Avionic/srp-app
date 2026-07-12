from dataclasses import dataclass
from someipy.serialization import (
    Float32,
    Uint16,
    Uint8,
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
class RadioDataType:
    rxerrors: Uint16
    fixed: Uint16
    rssi: Uint8
    remrssi: Uint8
    txbuf: Uint8
    noise: Uint8
    remnoise: Uint8

    def __init__(self):
        self.rxerrors = Uint16()
        self.fixed = Uint16()
        self.rssi = Uint8()
        self.remrssi = Uint8()
        self.txbuf = Uint8()
        self.noise = Uint8()
        self.remnoise = Uint8()

    def from_json(self, json_obj):
        self.rxerrors.value = int(json_obj['rxerrors'])
        self.fixed.value = int(json_obj['fixed'])
        self.rssi.value = int(json_obj['rssi'])
        self.remrssi.value = int(json_obj['remrssi'])
        self.txbuf.value = int(json_obj['txbuf'])
        self.noise.value = int(json_obj['noise'])
        self.remnoise.value = int(json_obj['remnoise'])

    def deserialize(self, payload: bytes):
        self.rxerrors.deserialize(payload[0:2])
        self.fixed.deserialize(payload[2:4])
        self.rssi.deserialize(payload[4:5])
        self.remrssi.deserialize(payload[5:6])
        self.txbuf.deserialize(payload[6:7])
        self.noise.deserialize(payload[7:8])
        self.remnoise.deserialize(payload[8:9])

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
class IMUDataStructure:
    gyroscope_x: Float32
    gyroscope_y: Float32
    gyroscope_z: Float32
    accel_x: Float32
    accel_y: Float32
    accel_z: Float32

    def __init__(self):
        self.gyroscope_x = Float32()
        self.gyroscope_y = Float32()
        self.gyroscope_z = Float32()
        self.accel_x = Float32()
        self.accel_y = Float32()
        self.accel_z = Float32()

    def from_json(self, json_obj):
        self.gyroscope_x.value = float(json_obj['gyroscope_x'])
        self.gyroscope_y.value = float(json_obj['gyroscope_y'])
        self.gyroscope_z.value = float(json_obj['gyroscope_z'])
        self.accel_x.value = float(json_obj['accel_x'])
        self.accel_y.value = float(json_obj['accel_y'])
        self.accel_z.value = float(json_obj['accel_z'])

    def deserialize(self, payload: bytes):
        self.gyroscope_x.deserialize(payload[0:4])
        self.gyroscope_y.deserialize(payload[4:8])
        self.gyroscope_z.deserialize(payload[8:12])
        self.accel_x.deserialize(payload[12:16])
        self.accel_y.deserialize(payload[16:20])
        self.accel_z.deserialize(payload[20:24])

@dataclass
class FcSysStatType:
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

@dataclass
class GPSRMCDataStructure:
    latitude: Float32
    longitude: Float32
    speed: Float32
    angle: Float32

    def __init__(self):
        self.latitude = Float32()
        self.longitude = Float32()
        self.speed = Float32()
        self.angle = Float32()

    def from_json(self, json_obj):
        self.latitude.value = float(json_obj['latitude'])
        self.longitude.value = float(json_obj['longitude'])
        self.speed.value = float(json_obj['speed'])
        self.angle.value = float(json_obj['angle'])

    def deserialize(self, payload: bytes):
        self.latitude.deserialize(payload[0:4])
        self.longitude.deserialize(payload[4:8])
        self.speed.deserialize(payload[8:12])
        self.angle.deserialize(payload[12:16])

@dataclass
class GPSVTGDataStructure:
    trueCourse: Float32
    relativeSpeed: Float32

    def __init__(self):
        self.trueCourse = Float32()
        self.relativeSpeed = Float32()

    def from_json(self, json_obj):
        self.trueCourse.value = float(json_obj['trueCourse'])
        self.relativeSpeed.value = float(json_obj['relativeSpeed'])

    def deserialize(self, payload: bytes):
        self.trueCourse.deserialize(payload[0:4])
        self.relativeSpeed.deserialize(payload[4:8])