from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime

from pandora.config import WarningValues


@dataclass(slots=True)
class DeviceRecordValue:
    battery: int
    co2: int
    hum: int
    lux: int
    noise: int
    powertype: int
    temp: float
    tilt: int
    time: int
    type: int


@dataclass(slots=True)
class DeviceRecord:
    id: int
    created: datetime
    value: DeviceRecordValue


@dataclass(slots=True)
class Device:
    id: int
    records_count: int
    records: list[DeviceRecord]
    warnings: defaultdict[str, int] = field(default_factory=defaultdict)

    def __post_init__(self) -> None:
        self.warnings = defaultdict(int)
        for record in self.records:
            if record.value.co2 >= WarningValues.co2:
                self.warnings["co2"] += 1
            if record.value.hum >= WarningValues.hum:
                self.warnings["hum"] += 1
            if record.value.lux >= WarningValues.lux:
                self.warnings["lux"] += 1
            if record.value.noise >= WarningValues.noise:
                self.warnings["noise"] += 1
            if record.value.temp >= WarningValues.temp:
                self.warnings["temp"] += 1
