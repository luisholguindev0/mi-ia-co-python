"""
Modelos Pydantic para leads y datos extraídos.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class LeadData(BaseModel):
    """Datos extraídos del lead durante la conversación."""
    nombre: Optional[str] = Field(None, description="Nombre del contacto")
    empresa: Optional[str] = Field(None, description="Nombre de la empresa")
    cargo: Optional[str] = Field(None, description="Cargo del contacto")
    ciudad: Optional[str] = Field(None, description="Ciudad en Colombia")
    email: Optional[str] = Field(None, description="Correo electrónico")
    puntos_dolor: List[str] = Field(default_factory=list, description="Problemas mencionados")
    presupuesto_min: Optional[int] = Field(None, ge=0, description="Presupuesto mínimo COP")
    presupuesto_max: Optional[int] = Field(None, ge=0, description="Presupuesto máximo COP")
    urgencia: Optional[Literal["baja", "media", "alta", "urgente"]] = None
    contexto_adicional: Optional[str] = None


class BANTScore(BaseModel):
    """Puntuación BANT del lead."""
    budget_score: int = Field(default=0, ge=0, le=25)
    budget_justification: str = ""
    authority_score: int = Field(default=0, ge=0, le=25)
    authority_justification: str = ""
    need_score: int = Field(default=0, ge=0, le=25)
    need_justification: str = ""
    timing_score: int = Field(default=0, ge=0, le=25)
    timing_justification: str = ""
    
    @property
    def total_score(self) -> int:
        return self.budget_score + self.authority_score + self.need_score + self.timing_score
    
    @property
    def qualification_status(self) -> Literal["hot", "warm", "cold", "disqualified"]:
        total = self.total_score
        if total >= 60:
            return "hot"
        elif total >= 40:
            return "warm"
        elif total >= 20:
            return "cold"
        return "disqualified"


class Lead(BaseModel):
    """Modelo completo de un lead en el sistema."""
    id: Optional[str] = None
    phone_number: str
    nombre: Optional[str] = None
    empresa: Optional[str] = None
    cargo: Optional[str] = None
    ciudad: Optional[str] = None
    email: Optional[str] = None
    puntos_dolor: List[str] = Field(default_factory=list)
    presupuesto_min: Optional[int] = None
    presupuesto_max: Optional[int] = None
    urgencia: Optional[str] = None
    bant_score: int = 0
    fsm_state: str = "INICIO"
    extracted_facts: dict = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_message_at: Optional[datetime] = None
    message_count: int = 0
    source: str = "whatsapp"


class Appointment(BaseModel):
    """Modelo de cita agendada."""
    id: Optional[str] = None
    lead_id: str
    calendar_event_id: Optional[str] = None
    meeting_link: Optional[str] = None
    scheduled_at: datetime
    duration_minutes: int = 15
    status: Literal["scheduled", "completed", "cancelled", "no_show"] = "scheduled"
    reminder_sent: bool = False
