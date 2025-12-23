"""
Integración con WhatsApp Business Cloud API.
Maneja envío y recepción de mensajes.
"""
import httpx
from typing import Optional, List

from ..config import settings
from ..models import OutboundMessage, WhatsAppButton


class WhatsAppClient:
    """Cliente para WhatsApp Business Cloud API."""
    
    def __init__(self):
        self.api_url = settings.whatsapp_api_url
        self.phone_id = settings.whatsapp_phone_id
        self.token = settings.whatsapp_token
    
    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def send_text_message(
        self, 
        phone_number: str, 
        message: str
    ) -> dict:
        """Envía un mensaje de texto simple."""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {"body": message}
        }
        
        return await self._send_request(payload)
    
    async def send_button_message(
        self, 
        phone_number: str, 
        message: str, 
        buttons: List[WhatsAppButton]
    ) -> dict:
        """Envía un mensaje con botones interactivos (máximo 3)."""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": message},
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": btn.id,
                                "title": btn.title[:20]  # Límite WhatsApp
                            }
                        }
                        for btn in buttons[:3]  # Máximo 3 botones
                    ]
                }
            }
        }
        
        return await self._send_request(payload)
    
    async def send_message(self, outbound: OutboundMessage) -> dict:
        """Envía un mensaje (texto o con botones)."""
        if outbound.buttons:
            return await self.send_button_message(
                outbound.phone_number,
                outbound.message,
                outbound.buttons
            )
        return await self.send_text_message(
            outbound.phone_number,
            outbound.message
        )
    
    async def mark_as_read(self, message_id: str) -> dict:
        """Marca un mensaje como leído."""
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        return await self._send_request(payload)
    
    async def _send_request(self, payload: dict) -> dict:
        """Envía una solicitud a la API de WhatsApp."""
        url = f"{self.api_url}/{self.phone_id}/messages"
        
        if not self.token:
            print(f"⚠️ WhatsApp no configurado. Mensaje mock: {payload}")
            return {"mock": True, "payload": payload}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                print(f"❌ Error WhatsApp API: {response.status_code} - {response.text}")
                return {"error": response.text}
            
            return response.json()


# Instancia global
whatsapp_client = WhatsAppClient()
