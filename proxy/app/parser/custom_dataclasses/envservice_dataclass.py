from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Sint16
)


@dataclass
class newTempEvent_1In(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''


@dataclass
class newTempEvent_1Out(SomeIpPayload):
    data: Sint16

    def __init__(self):
        self.data = Sint16()



@dataclass
class newTempEvent_2In(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''


@dataclass
class newTempEvent_2Out(SomeIpPayload):
    data: Sint16

    def __init__(self):
        self.data = Sint16()



@dataclass
class newTempEvent_3In(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''


@dataclass
class newTempEvent_3Out(SomeIpPayload):
    data: Sint16

    def __init__(self):
        self.data = Sint16()



@dataclass
class newPressEventIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''


@dataclass
class newPressEventOut(SomeIpPayload):
    data: Sint16

    def __init__(self):
        self.data = Sint16()



@dataclass
class newDPressEventIn(SomeIpPayload):
    data: bytes

    def __init__(self):
        self.data = b''


@dataclass
class newDPressEventOut(SomeIpPayload):
    data: Sint16

    def __init__(self):
        self.data = Sint16()
