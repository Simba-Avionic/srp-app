from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Bool,
    Uint8
)


@dataclass
class StartMsg(SomeIpPayload):
    in_data: None
    out: Bool

    def __init__(self):
        self.out = Bool()


@dataclass
class SetModeMsg(SomeIpPayload):
    in_data: Uint8
    out: Bool

    def __init__(self):
        self.in_data = Uint8()
        self.out = Bool()


@dataclass
class CurrentModeMsg(SomeIpPayload):
    out: Uint8

    def __init__(self):
        self.out = Uint8()