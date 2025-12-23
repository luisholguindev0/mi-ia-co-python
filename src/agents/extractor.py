"""
Agente Extractor: Extracción de datos del lead.
Extrae entidades nombradas y datos estructurados de la conversación.
"""
from typing import Optional
from ..integrations.deepseek import deepseek_client
from ..models import LeadData, ConversationContext


EXTRACTOR_SYSTEM_PROMPT = """Eres el **Agente Extractor de Mi IA Colombia**. Tu misión es convertir conversación natural en datos estructurados JSON.

TU TAREA:
Analiza la conversación y extrae SOLO la información explícita del usuario. NO inventes datos. NO asumas nada que no esté claro.

CAMPOS A EXTRAER:
- **nombre:** Nombre propio del contacto (ej: "Juan Pérez").
- **empresa:** Nombre de la empresa u organización.
- **cargo:** Rol profesional (ej: "Gerente", "Dueño", "Vendedor").
- **ciudad:** Ciudad en Colombia (ej: "Bogotá", "Medallo", "Cali").
- **email:** Correo electrónico válido.
- **puntos_dolor:** Lista de problemas (ej: ["pierdo ventas", "no contesto a tiempo"]).
- **presupuesto_min:** Valor numérico en COP (Sin puntos ni comas).
- **presupuesto_max:** Valor numérico en COP (Sin puntos ni comas).
- **urgencia:** "baja", "media", "alta", "urgente".

REGLAS DE NORMALIZACIÓN (CRÍTICO):
1. **Moneda (COP):**
   - "15 millones" -> 15000000
   - "30 palos" -> 30000000
   - "10M" -> 10000000
   - "200 mil" -> 200000
2. **Urgencia:**
   - "para ayer", "ya", "urgente" -> "urgente"
   - "este mes", "pronto" -> "alta"
   - "viendo opciones", "sin afán" -> "baja"
3. **Puntos de Dolor:** Extrae frases cortas que describan el problema.

DATOS YA CONOCIDOS (Solo actualiza si hay nueva información mejor):
{datos_actuales}

RESPONDE SOLO EL JSON (Sin markdown):
{{
  "nombre": "...",
  "empresa": "...",
  "cargo": "...",
  "ciudad": "...",
  "email": "...",
  "puntos_dolor": ["..."],
  "presupuesto_min": 10000000,
  "presupuesto_max": 20000000,
  "urgencia": "media"
}}"""


class ExtractorAgent:
    """Agente que extrae datos estructurados de la conversación."""
    
    async def extract(self, context: ConversationContext) -> LeadData:
        """Extrae datos del lead de la conversación actual."""
        
        # Construir historial de conversación
        conversation = self._build_conversation(context)
        
        # Prompt con datos actuales
        system_prompt = EXTRACTOR_SYSTEM_PROMPT.format(
            datos_actuales=context.lead_data or {}
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"CONVERSACIÓN:\n{conversation}"}
        ]
        
        # Llamar a DeepSeek
        result = await deepseek_client.chat_json(messages, temperature=0.1)
        
        # Parsear resultado
        try:
            # Filtrar valores null
            clean_data = {
                k: v for k, v in result.items() 
                if v is not None and v != "" and v != []
            }
            return LeadData(**clean_data)
        except Exception as e:
            print(f"Error parsing extractor result: {e}")
            return LeadData()
    
    def _build_conversation(self, context: ConversationContext) -> str:
        """Construye el historial de conversación."""
        lines = []
        
        for msg in context.message_history:
            role = "Usuario" if msg.direction == "inbound" else "Agente"
            lines.append(f"{role}: {msg.content}")
        
        # Añadir mensaje actual
        lines.append(f"Usuario: {context.current_message}")
        
        return "\n".join(lines)


# Instancia global
extractor_agent = ExtractorAgent()
