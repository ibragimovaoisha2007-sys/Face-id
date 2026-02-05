from datetime import datetime

class GenericHikvisionAdapter:
    def normalize(self, payload: dict):
        # Hikvision kamerasi formati
        event = payload.get("AccessControllerEvent", {})
        
        # Generatoringdan keladigan kalitlarni ham, kameranikini ham tekshiramiz
        # Muhimi: Har doim biror qiymat qaytishini ta'minlaymiz
        t_id = (payload.get("terminalUserId") or 
                event.get("employeeNoString") or 
                event.get("employeeNo") or 
                "0000")
        
        d_id = (payload.get("deviceId") or 
                payload.get("dateTime") or 
                "UNKNOWN-DEVICE")
        
        # generator 'eventType' (T katta), adapter esa 'eventType' yoki 'event_type' qidiradi
        e_type = (payload.get("eventType") or 
                  event.get("eventType") or 
                  "IN")
        
        e_time = (payload.get("timestamp") or 
                  event.get("dateTime") or 
                  datetime.now().isoformat())

        s_id = (payload.get("sourceEventId") or 
                event.get("eventLogID") or 
                "0")

        return type("NormalizedEvent", (), {
            "device_id": str(d_id),
            "terminal_user_id": str(t_id),
            "event_type": str(e_type),
            "event_time": e_time,
            "source_event_id": str(s_id),
            "raw_payload": payload
        })
