from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Sint16
)


@dataclass
class newTempEvent_1Msg(SomeIpPayload):
    out: Sint16

    def __init__(self):
        self.out = Sint16()


@dataclass
class newTempEvent_2Msg(SomeIpPayload):
    out: Sint16

    def __init__(self):
        self.out = Sint16()


@dataclass
class newTempEvent_3Msg(SomeIpPayload):
    out: Sint16

    def __init__(self):
        self.out = Sint16()


@dataclass
class newPressEventMsg(SomeIpPayload):
    out: Sint16

    def __init__(self):
        self.out = Sint16()


@dataclass
class newDPressEventMsg(SomeIpPayload):
    out: Sint16

    def __init__(self):
        self.out = Sint16()