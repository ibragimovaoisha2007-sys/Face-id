from datetime import datetime

class GenericHikvisionAdapter:
    def normalize(self, payload: dict):
        # Hikvision kamerasi uchun (AccessControllerEvent ichida bo'ladi)
        event = payload.get("AccessControllerEvent", {})
        
        # Generatoringdan keladigan sodda format yoki kamera formati
        # Qaysi birida ma'lumot bo'lsa, o'shani oladi
        terminal_user_id = (
            payload.get("terminalUserId") or 
            event.get("employeeNoString") or 
            event.get("employeeNo") or 
            "0"
        )
        
        device_id = payload.get("deviceId") or payload.get("dateTime") or "UNKNOWN-DEV"
        
        event_type = payload.get("eventType") or event.get("eventType") or "ACCESS"
        
        event_time = (
            payload.get("timestamp") or 
            event.get("dateTime") or 
            payload.get("dateTime") or 
            datetime.now().isoformat()
        )

        return type("NormalizedEvent", (), {
            "device_id": str(device_id),
            "terminal_user_id": str(terminal_user_id),
            "event_type": str(event_type),
            "event_time": event_time,
            "source_event_id": str(payload.get("sourceEventId") or event.get("eventLogID") or "0"),
            "raw_payload": payload
        })
