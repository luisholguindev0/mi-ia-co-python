"""
Modelos Pydantic para mensajes de WhatsApp.
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime


class Message(BaseModel):
    """Mensaje de WhatsApp."""
    id: Optional[str] = None
    lead_id: Optional[str] = None
    phone_number: str
    direction: Literal["inbound", "outbound"]
    content: str
    message_type: Literal["text", "button", "list", "template"] = "text"
    whatsapp_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: dict = Field(default_factory=dict)


class WhatsAppWebhookMessage(BaseModel):
    """Estructura del mensaje entrante de WhatsApp webhook."""
    from_number: str = Field(alias="from")
    id: str
    timestamp: str
    text: Optional[dict] = None
    type: str
    
    @property
    def body(self) -> str:
        if self.text and "body" in self.text:
            return self.text["body"]
        return ""


class WhatsAppButton(BaseModel):
    """Botón interactivo de WhatsApp."""
    id: str
    title: str


class OutboundMessage(BaseModel):
    """Mensaje de salida para enviar a WhatsApp."""
    phone_number: str
    message: str
    buttons: Optional[List[WhatsAppButton]] = None


class RouterResult(BaseModel):
    """Resultado del agente Router."""
    intencion_primaria: str
    intencion_secundaria: Optional[str] = None
    contiene_dato_extraible: bool = False
    datos_detectados: dict = Field(default_factory=dict)
    siguiente_estado_sugerido: Optional[str] = None
    confianza: float = Field(ge=0.0, le=1.0, default=0.5)


class ConversationContext(BaseModel):
    """Contexto de conversación para los agentes."""
    phone_number: str
    current_message: str
    message_history: List[Message] = Field(default_factory=list)
    lead_data: Optional[dict] = None
    fsm_state: str = "INICIO"
    bant_score: int = 0
