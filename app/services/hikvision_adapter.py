from dataclasses import dataclass
from datetime import datetime


@dataclass
class NormalizedEvent:
    terminal_user_id: str | None
    event_time: datetime
    device_id: str
    event_type: str
    source_event_id: str
    raw_payload: dict


class HikvisionEventAdapter:
    """
    Adapter layer for different Hikvision payload formats.

    Map any payload to NormalizedEvent.
    """

    def normalize(self, payload: dict) -> NormalizedEvent:
        raise NotImplementedError


class GenericHikvisionAdapter(HikvisionEventAdapter):
    def normalize(self, payload: dict) -> NormalizedEvent:
        return NormalizedEvent(
            terminal_user_id=payload.get("terminalUserId")
            or payload.get("employeeNo"),
            event_time=datetime.fromisoformat(payload["timestamp"]),
            device_id=payload.get("deviceId", "unknown"),
            event_type=payload.get("eventType", "IN"),
            source_event_id=payload.get("sourceEventId", payload.get("eventId", "")),
            raw_payload=payload,
        )
