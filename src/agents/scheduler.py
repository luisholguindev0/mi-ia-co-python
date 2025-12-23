"""
Agente Scheduler: Manejo de agendamiento.
Gestiona la lógica de agendamiento de citas, soportando Mock y Google Calendar.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Protocol, Dict
import pytz
import json

from ..config import settings

# =====================
# INTERFACE
# =====================

class CalendarService(Protocol):
    def get_available_slots(self, days_ahead: int = 7) -> List[str]:
        ...
    
    def create_event(self, date_str: str, lead_email: str, description: str) -> Dict:
        ...

# =====================
# MOCK IMPLEMENTATION
# =====================

class MockCalendarService:
    """Servicio simulado de calendario para desarrollo/testing."""
    
    def __init__(self):
        self.timezone = pytz.timezone(settings.company_timezone)
        self.duration = settings.consultation_duration_minutes
        
    def get_available_slots(self, days_ahead: int = 7) -> List[str]:
        """Genera slots estáticos pero realistas."""
        slots = []
        now = datetime.now(self.timezone)
        
        # Horarios probables de disponibilidad
        work_hours = [9, 10, 11, 14, 15, 16]
        
        for day_offset in range(1, days_ahead + 1):
            date = now + timedelta(days=day_offset)
            
            # Saltar fines de semana
            if date.weekday() >= 5:
                continue
            
            for hour in work_hours:
                # Simular ocupación aleatoria (simple: horas pares disponibles)
                if hour % 2 == 0: 
                    slot_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
                    day_name = self._get_day_name(slot_time)
                    formatted = f"{day_name} {slot_time.day} - {hour}:00 {'AM' if hour < 12 else 'PM'}"
                    slots.append(formatted)
                
            if len(slots) >= 5:
                break
                
        return slots[:3]
    
    def create_event(self, date_str: str, lead_email: str, description: str) -> Dict:
        """Simula la creación de un evento."""
        return {
            "id": f"mock-event-{int(datetime.now().timestamp())}",
            "link": "https://meet.google.com/mock-link-123",
            "status": "confirmed",
            "provider": "mock"
        }

    def _get_day_name(self, date: datetime) -> str:
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        return days[date.weekday()]

# =====================
# GOOGLE CALENDAR (TODO: Implementar)
# =====================

class GoogleCalendarService:
    """Conexión real con Google Calendar API."""
    
    def __init__(self):
        # Aquí iría la carga de credenciales
        self.creds = None
        if settings.google_calendar_credentials:
            pass # Cargar credenciales
            
    def get_available_slots(self, days_ahead: int = 7) -> List[str]:
        # Implementar lógica real "FreeBusy"
        return []

    def create_event(self, date_str: str, lead_email: str, description: str) -> Dict:
        # Implementar insert event
        return {}

# =====================
# FACTORY & AGENT
# =====================

def get_calendar_service() -> CalendarService:
    """Factory que devuelve el servicio adecuado según config."""
    if settings.use_mock_calendar:
        return MockCalendarService()
    return GoogleCalendarService()


class SchedulerAgent:
    """Agente principal que usa el servicio de calendario."""
    
    def __init__(self):
        self.service = get_calendar_service()
        self.duration = settings.consultation_duration_minutes
        self.timezone = pytz.timezone(settings.company_timezone)
    
    def get_available_slots(self, days_ahead: int = 7) -> List[str]:
        return self.service.get_available_slots(days_ahead)
    
    def format_confirmation(self, slot: str) -> dict:
        """Formatea los datos para confirmar la cita."""
        # Recuperar fecha "Lunes 24 - 10:00 AM"
        try:
            parts = slot.split(" - ")
            date_part = parts[0]
            time_part = parts[1]
            return {
                "date": date_part,
                "time": time_part,
                "duration": self.duration,
                "timezone": settings.company_timezone
            }
        except:
            return {"date": slot, "time": "", "duration": 15}

    def parse_user_selection(self, message: str, available_slots: List[str]) -> Optional[str]:
        """Lógica heurística para entender qué slot eligió el usuario."""
        msg = message.lower()
        
        # 1. Búsqueda directa
        for slot in available_slots:
            # Slot: "Lunes 24 - 10:00 AM"
            # Buscar "lunes" y "10"
            parts = slot.lower().split(" - ")
            day_num = parts[0].split(" ")[1] # "24"
            hour = parts[1].split(":")[0] # "10"
            
            if day_num in msg and hour in msg:
                return slot
            
        # 2. Ordinales ("la primera", "la 1")
        if "primera" in msg or "uno" in msg or "1" in msg:
            return available_slots[0] if len(available_slots) > 0 else None
        if "segunda" in msg or "dos" in msg or "2" in msg:
            return available_slots[1] if len(available_slots) > 1 else None
        if "tercera" in msg or "tres" in msg or "3" in msg:
            return available_slots[2] if len(available_slots) > 2 else None
            
        return None

# Instancia global
scheduler_agent = SchedulerAgent()
