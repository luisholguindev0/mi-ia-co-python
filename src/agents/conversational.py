"""
Agente Conversacional: Generador de respuestas.
Genera respuestas naturales y persuasivas según el estado FSM y contexto.
"""
from typing import Optional
from ..integrations.deepseek import deepseek_client
from ..models import ConversationContext
from ..config import FSMStates, settings


CONVERSATIONAL_SYSTEM_PROMPT = """Eres el **Asistente Virtual de Mi IA Colombia**, experto en automatización y ventas B2B.

IDENTIDAD Y TONO:
- **Colombiano Profesional:** Usa un tono cercano pero respetuoso. Evita jerga excesiva ("parce", "bacano") a menos que el usuario sea muy informal. Prefiere "te colaboro", "con mucho gusto", "claro que sí".
- **Empatía Comercial:** Entiende que el cliente quiere vender más o ahorrar tiempo.
- **Directo:** Valora el tiempo del cliente. Ve al grano.

RESTICCIONES ESTRICTAS (Si no cumples, el sistema fallará):
1. **Longitud:** MÁXIMO 3 párrafos cortos. Idealmente 2.
2. **Emojis:** MÁXIMO 1 emoji por mensaje. Úsalo para enfatizar (e.g., 🚀, 💡, ✅).
3. **Preguntas:** NUNCA hagas más de UNA pregunta por turno.
4. **Precios:** NUNCA des un precio fijo. Usa rangos amplios ($10M - $100M COP) y aclara "según complejidad".
5. **Call to Action:** Tu objetivo FINAL en cada turno es acercarte al agendamiento de la cita de 15 min.

SERVICIOS:
- **Agentes SDR para WhatsApp:** Cualifican leads 24/7 y agendan citas. Ideal para empresas con >10 leads diarios.
- **Apps Web Inteligentes:** Desarrollo a la medida con IA integrada.
- **Automatización:** flujos de trabajo que ahorran horas hombre.

PROHIBIDO:
- Hablar de política, religión o competidores específicos.
- Inventar características técnicas que no existen.
- Prometer resultados numéricos exactos ("venderás 50% más").

ESTADO ACTUAL DE LA VENTA: {estado} (Sigue el objetivo de este estado)
OBJETIVO INMEDIATO: {objetivo_estado}

DATOS QUE YA SABES DEL LEAD:
{lead_data}

HISTORIAL RECIENTE:
{conversacion}

Responde como el asistente ideal: útil, breve y persuasivo."""


# Objetivos por estado
STATE_OBJECTIVES = {
    FSMStates.BIENVENIDA: "Dar la bienvenida, presentar brevemente la empresa y preguntar en qué puedes ayudar.",
    FSMStates.EXTRACCION_DATOS: "Hacer preguntas naturales para obtener nombre, empresa, ciudad, o problema que tiene.",
    FSMStates.CALIFICACION: "Entender mejor su necesidad, presupuesto aproximado y urgencia.",
    FSMStates.OBJECIONES: "Manejar la objeción con empatía, dar argumentos de valor y reconducir.",
    FSMStates.CIERRE: "Proponer agendar una llamada de 15 minutos. Ofrecer 2-3 horarios específicos.",
    FSMStates.AGENDADO: "Confirmar la cita con todos los detalles y despedirse amablemente.",
    FSMStates.NUTRICION: "Mantener el engagement, ofrecer valor, y dejar la puerta abierta.",
    FSMStates.DESCARTADO: "Despedirse amablemente y dejar la puerta abierta para el futuro."
}


class ConversationalAgent:
    """Agente que genera respuestas naturales y persuasivas."""
    
    async def generate_response(
        self, 
        context: ConversationContext,
        state: str = None
    ) -> str:
        """Genera una respuesta para el estado actual."""
        
        current_state = state or context.fsm_state
        objetivo = STATE_OBJECTIVES.get(current_state, "Responder de forma útil y guiar hacia agendar.")
        
        # Construir conversación
        conversation = self._build_conversation(context)
        
        system_prompt = CONVERSATIONAL_SYSTEM_PROMPT.format(
            estado=current_state,
            lead_data=context.lead_data or {},
            objetivo_estado=objetivo,
            conversacion=conversation
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context.current_message}
        ]
        
        # Llamar a DeepSeek
        response = await deepseek_client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        return response.strip()
    
    async def generate_welcome(self) -> str:
        """Genera mensaje de bienvenida estándar."""
        return f"""¡Hola! 👋 Soy el asistente virtual de {settings.company_name}.

Ayudamos a empresas a crecer con sistemas de inteligencia artificial: apps web de alto rendimiento y agentes de ventas que trabajan 24/7.

¿En qué puedo ayudarte hoy?"""
    
    async def generate_closing_message(
        self, 
        lead_name: str,
        available_slots: list
    ) -> str:
        """Genera mensaje de cierre con horarios disponibles."""
        name_part = f", {lead_name}" if lead_name else ""
        
        slots_text = "\n".join([f"📅 {slot}" for slot in available_slots[:3]])
        
        return f"""¡Excelente{name_part}! 🎯

Me encantaría que hables directamente con nuestro equipo de soluciones.

Tenemos disponibilidad para una llamada de 15 minutos:
{slots_text}

¿Cuál te funciona mejor?"""
    
    async def generate_confirmation(
        self,
        lead_name: str,
        meeting_date: str,
        meeting_time: str,
        meeting_link: str = None
    ) -> str:
        """Genera mensaje de confirmación de cita."""
        link_part = f"\n📍 Link: {meeting_link}" if meeting_link else ""
        
        return f"""✅ ¡Cita confirmada{', ' + lead_name if lead_name else ''}!

📅 Fecha: {meeting_date}
🕐 Hora: {meeting_time} (Hora Colombia){link_part}

Te enviaré un recordatorio antes de la llamada. ¡Hasta pronto! 🚀"""
    
    def _build_conversation(self, context: ConversationContext) -> str:
        """Construye el historial de conversación."""
        if not context.message_history:
            return "(Nueva conversación)"
        
        lines = []
        for msg in context.message_history[-5:]:  # Últimos 5 mensajes
            role = "Usuario" if msg.direction == "inbound" else "Agente"
            lines.append(f"{role}: {msg.content}")
        
        return "\n".join(lines)


# Instancia global
conversational_agent = ConversationalAgent()
