from dataclasses import dataclass
from someipy.serialization import (
    SomeIpPayload,
    Sint16,
)

@dataclass
class NewTempEvent_1Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewTempEvent_2Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewTempEvent_3Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewOxidizerPressEventOut(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewPressureFeedPressEventOut(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewChamberPressEvent1Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewBoardTempEvent1Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewBoardTempEvent2Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)


@dataclass
class NewBoardTempEvent3Out(SomeIpPayload):
    data: Sint16
    def __init__(self):
        self.data = Sint16()

    def from_json(self, json_argument):
        self.data.value = int(json_argument)
