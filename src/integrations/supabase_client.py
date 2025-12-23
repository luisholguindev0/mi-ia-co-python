"""
Cliente Supabase para persistencia de datos.
Maneja leads, mensajes, estados FSM y citas.
"""
from supabase import create_client, Client
from typing import Optional, List
from datetime import datetime
import json

from ..config import settings
from ..models import Lead, Message, Appointment


class SupabaseClient:
    """Cliente para operaciones con Supabase."""
    
    def __init__(self):
        if settings.supabase_url and settings.supabase_key:
            self.client: Client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        else:
            self.client = None
            print("⚠️ Supabase no configurado. Usando modo mock.")
    
    # =====================
    # LEADS
    # =====================
    
    async def get_lead_by_phone(self, phone_number: str) -> Optional[Lead]:
        """Obtiene un lead por número de teléfono."""
        if not self.client:
            return None
            
        result = self.client.table("leads").select("*").eq(
            "phone_number", phone_number
        ).execute()
        
        if result.data and len(result.data) > 0:
            return Lead(**result.data[0])
        return None
    
    async def create_lead(self, phone_number: str) -> Lead:
        """Crea un nuevo lead."""
        lead_data = {
            "phone_number": phone_number,
            "fsm_state": "INICIO",
            "bant_score": 0,
            "message_count": 0,
            "source": "whatsapp",
            "extracted_facts": {},
            "puntos_dolor": []
        }
        
        if not self.client:
            return Lead(**lead_data, id="mock-id")
        
        result = self.client.table("leads").insert(lead_data).execute()
        return Lead(**result.data[0])
    
    async def get_or_create_lead(self, phone_number: str) -> Lead:
        """Obtiene o crea un lead."""
        lead = await self.get_lead_by_phone(phone_number)
        if not lead:
            lead = await self.create_lead(phone_number)
        return lead
    
    async def update_lead(self, phone_number: str, updates: dict) -> Optional[Lead]:
        """Actualiza un lead."""
        if not self.client:
            return None
            
        updates["updated_at"] = datetime.now().isoformat()
        
        result = self.client.table("leads").update(updates).eq(
            "phone_number", phone_number
        ).execute()
        
        if result.data:
            return Lead(**result.data[0])
        return None
    
    async def update_fsm_state(self, phone_number: str, new_state: str) -> None:
        """Actualiza el estado FSM de un lead."""
        await self.update_lead(phone_number, {"fsm_state": new_state})
    
    async def update_extracted_facts(self, phone_number: str, facts: dict) -> None:
        """Actualiza los hechos extraídos de un lead (merge)."""
        lead = await self.get_lead_by_phone(phone_number)
        if lead:
            existing_facts = lead.extracted_facts or {}
            merged_facts = {**existing_facts, **facts}
            await self.update_lead(phone_number, {"extracted_facts": merged_facts})
    
    async def update_bant_score(self, phone_number: str, score: int) -> None:
        """Actualiza el BANT score de un lead."""
        await self.update_lead(phone_number, {"bant_score": score})
    
    # =====================
    # MENSAJES
    # =====================
    
    async def save_message(self, message: Message) -> Optional[Message]:
        """Guarda un mensaje."""
        if not self.client:
            return message
        
        # Obtener lead_id
        lead = await self.get_lead_by_phone(message.phone_number)
        if not lead:
            return None
        
        message_data = {
            "lead_id": lead.id,
            "direction": message.direction,
            "content": message.content,
            "message_type": message.message_type,
            "whatsapp_id": message.whatsapp_id,
            "metadata": message.metadata
        }
        
        result = self.client.table("messages").insert(message_data).execute()
        
        # Incrementar contador de mensajes
        await self.update_lead(message.phone_number, {
            "message_count": (lead.message_count or 0) + 1,
            "last_message_at": datetime.now().isoformat()
        })
        
        if result.data:
            return Message(**result.data[0], phone_number=message.phone_number)
        return message
    
    async def get_message_history(
        self, 
        phone_number: str, 
        limit: int = 10
    ) -> List[Message]:
        """Obtiene el historial de mensajes de un lead."""
        if not self.client:
            return []
        
        lead = await self.get_lead_by_phone(phone_number)
        if not lead or not lead.id:
            return []
        
        result = self.client.table("messages").select("*").eq(
            "lead_id", lead.id
        ).order("created_at", desc=True).limit(limit).execute()
        
        messages = [
            Message(**msg, phone_number=phone_number) 
            for msg in result.data
        ]
        return messages[::-1]  # Orden cronológico
    
    # =====================
    # CITAS
    # =====================
    
    async def create_appointment(self, appointment: Appointment) -> Optional[Appointment]:
        """Crea una cita."""
        if not self.client:
            return appointment
        
        appointment_data = {
            "lead_id": appointment.lead_id,
            "calendar_event_id": appointment.calendar_event_id,
            "meeting_link": appointment.meeting_link,
            "scheduled_at": appointment.scheduled_at.isoformat(),
            "duration_minutes": appointment.duration_minutes,
            "status": appointment.status,
            "reminder_sent": appointment.reminder_sent
        }
        
        result = self.client.table("appointments").insert(appointment_data).execute()
        
        if result.data:
            return Appointment(**result.data[0])
        return appointment
    
    # =====================
    # CONTEXTO CONVERSACIÓN
    # =====================
    
    async def get_conversation_context(self, phone_number: str) -> dict:
        """Obtiene el contexto completo para los agentes."""
        lead = await self.get_lead_by_phone(phone_number)
        messages = await self.get_message_history(phone_number, limit=10)
        
        return {
            "lead": lead.model_dump() if lead else None,
            "messages": [m.model_dump() for m in messages],
            "fsm_state": lead.fsm_state if lead else "INICIO",
            "bant_score": lead.bant_score if lead else 0,
            "extracted_facts": lead.extracted_facts if lead else {}
        }


# Instancia global
supabase_client = SupabaseClient()
