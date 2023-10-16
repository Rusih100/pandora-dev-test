import json
from collections.abc import Mapping
from datetime import datetime
from logging import getLogger
from typing import Any

from aiohttp import ClientConnectorError
from aiohttp.client import ClientSession

from pandora.models import Device, DeviceRecord, DeviceRecordValue
from pandora.utils import datetime_to_string, parse_datetime_string

logger = getLogger("PandoraService")


class PandoraService:
    @classmethod
    async def get_decoded_payloads(
        cls, *, list_id: list[int], start_time: datetime, end_time: datetime
    ) -> list[Device]:
        url = r"https://pandora.dvfu.ru/records/decoded_payloads"
        payload = {
            "conditions": {
                "list_id": list_id,
                "start_time": datetime_to_string(start_time),
                "end_time": datetime_to_string(end_time),
            }
        }
        try:
            async with ClientSession() as session:
                response = await session.get(url=url, json=payload)
                response_json = await response.json()
                return cls._parse_decoded_payloads(
                    list_id=list_id, response_json=response_json
                )
        except (ClientConnectorError, Exception) as exc:
            logger.exception(exc)
            return []

    @classmethod
    def _parse_decoded_payloads(
        cls, *, list_id: list[int], response_json: Mapping[str, Any]
    ) -> list[Device]:
        devices: list[Device] = []
        raw_data = response_json["data"]

        for device_id in list_id:
            devices.append(
                cls._parse_device(device_id=device_id, raw_data=raw_data)
            )
        devices.sort(key=lambda x: -x.records_count)
        return devices

    @classmethod
    def _parse_device(
        cls, *, device_id: int, raw_data: Mapping[str, Any]
    ) -> Device:
        raw_device = raw_data[str(device_id)]
        records: list[DeviceRecord] = []

        for raw_record in raw_device["records"]:
            records.append(cls._parse_record(raw_record=raw_record))
        return Device(
            id=device_id, records_count=raw_device["count"], records=records
        )

    @staticmethod
    def _parse_record(*, raw_record: Mapping[str, Any]) -> DeviceRecord:
        raw_value_string: str = raw_record["value"]
        raw_value_string = raw_value_string.replace(r"'", r'"')
        raw_record_value = json.loads(raw_value_string)

        return DeviceRecord(
            id=raw_record["id"],
            created=parse_datetime_string(raw_record["created"]),
            value=DeviceRecordValue(
                battery=raw_record_value["battery"],
                co2=raw_record_value["co2"],
                hum=raw_record_value["hum"],
                lux=raw_record_value["lux"],
                noise=raw_record_value["noise"],
                powertype=raw_record_value["powertype"],
                temp=raw_record_value["temp"],
                tilt=raw_record_value["tilt"],
                time=raw_record_value["time"],
                type=raw_record_value["type"],
            ),
        )
