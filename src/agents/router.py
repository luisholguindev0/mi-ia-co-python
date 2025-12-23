"""
Agente Router: Clasificador de intención.
Clasifica el mensaje del usuario y sugiere el siguiente estado FSM.
"""
from typing import Optional
from ..integrations.deepseek import deepseek_client
from ..models import RouterResult, ConversationContext
from ..config import FSMStates, IntentTypes


ROUTER_SYSTEM_PROMPT = """Eres un clasificador de intenciones para un agente de ventas de Mi IA Colombia.

CONTEXTO DE LA EMPRESA:
- Mi IA Colombia vende sistemas de IA personalizados
- Servicios: Apps web con IA, Agentes de ventas, Automatización
- Mercado: Empresas colombianas (PYMEs y medianas)
- Presupuestos típicos: $5M - $100M COP

TU TAREA:
Analiza el mensaje del usuario y clasifica su intención.

INTENCIONES POSIBLES:
- saludo: Saludo inicial o casual
- expresion_interes: Muestra interés en los servicios
- pregunta_servicio: Pregunta sobre qué hacen o cómo funcionan
- pregunta_precio: Pregunta sobre costos o presupuestos
- objecion: Expresa duda, resistencia o problema
- solicitud_agendar: Quiere agendar una llamada o reunión
- info_personal: Comparte información personal (nombre, empresa, etc)
- punto_dolor: Menciona un problema o necesidad de su negocio
- no_interesado: Indica que no le interesa
- fuera_tema: Habla de algo no relacionado
- confirmacion: Confirma algo (horario, datos, etc)
- rechazo: Rechaza algo propuesto

ESTADO ACTUAL FSM: {estado_actual}
DATOS YA EXTRAÍDOS: {datos_lead}

Responde SOLO en JSON con este formato exacto:
{{
  "intencion_primaria": "...",
  "intencion_secundaria": null,
  "contiene_dato_extraible": true/false,
  "datos_detectados": {{}},
  "siguiente_estado_sugerido": "...",
  "confianza": 0.0-1.0
}}"""


class RouterAgent:
    """Agente que clasifica la intención del mensaje del usuario."""
    
    async def classify(self, context: ConversationContext) -> RouterResult:
        """Clasifica la intención del mensaje actual."""
        
        # Construir historial resumido
        history_summary = self._build_history_summary(context)
        
        # Prompt con contexto
        system_prompt = ROUTER_SYSTEM_PROMPT.format(
            estado_actual=context.fsm_state,
            datos_lead=context.lead_data or {}
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"HISTORIAL RECIENTE:\n{history_summary}\n\nMENSAJE ACTUAL:\n{context.current_message}"}
        ]
        
        # Llamar a DeepSeek
        result = await deepseek_client.chat_json(messages, temperature=0.2)
        
        # Parsear resultado
        try:
            return RouterResult(
                intencion_primaria=result.get("intencion_primaria", IntentTypes.OFF_TOPIC),
                intencion_secundaria=result.get("intencion_secundaria"),
                contiene_dato_extraible=result.get("contiene_dato_extraible", False),
                datos_detectados=result.get("datos_detectados", {}),
                siguiente_estado_sugerido=result.get("siguiente_estado_sugerido"),
                confianza=float(result.get("confianza", 0.5))
            )
        except Exception as e:
            print(f"Error parsing router result: {e}")
            return RouterResult(
                intencion_primaria=IntentTypes.OFF_TOPIC,
                confianza=0.3
            )
    
    def _build_history_summary(self, context: ConversationContext) -> str:
        """Construye un resumen del historial de mensajes."""
        if not context.message_history:
            return "(Sin historial previo)"
        
        summary = []
        for msg in context.message_history[-3:]:  # Últimos 3 mensajes
            role = "Usuario" if msg.direction == "inbound" else "Agente"
            summary.append(f"{role}: {msg.content[:100]}...")
        
        return "\n".join(summary)


# Instancia global
router_agent = RouterAgent()
