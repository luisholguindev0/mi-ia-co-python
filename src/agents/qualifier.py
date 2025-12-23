"""
Agente Calificador: Evaluación BANT del lead.
Calcula el score de calificación para determinar si el lead está listo para cierre.
"""
from ..integrations.deepseek import deepseek_client
from ..models import BANTScore, ConversationContext
from ..config import BANT_MIN_SCORE_FOR_CLOSE, BANT_MIN_SCORE_FOR_NURTURE


QUALIFIER_SYSTEM_PROMPT = """Eres el **Agente Calificador BANT de Mi IA Colombia**. Evalúas la calidad del lead para priorizar esfuerzos.

CONTEXTO:
- Producto: Agentes de IA ($10M-$50M COP).
- Meta: Identificar leads con DOLOR real y CAPACIDAD potencial.

CRITERIOS DE PUNTUACIÓN (Total 100 pts):

1. **BUDGET (0-25 pts):**
   - 25: Presupuesto confirmado >$10M.
   - 20: "Tengo recursos" o "Inversión necesaria".
   - 15: Pide cotización formal (señal de compra).
   - 10: No sabe precios pero el tamaño de empresa sugiere capacidad.
   - 0: Dice explícitamente "no tengo plata" o "busco gratis".

2. **AUTHORITY (0-25 pts):**
   - 25: Dueño, Gerente, Fundador.
   - 20: Director, Jefe de Área.
   - 10: Empleado buscando para su jefe.
   - 0: Estudiante, Curioso sin rol.

3. **NEED (0-25 pts):** (EL MÁS IMPORTANTE PARA NOSOTROS)
   - 25: Tiene un problema urgente ("pierdo clientes", "no doy abasto").
   - 20: Quiere modernizar/automatizar.
   - 10: Curiosidad general sobre IA.
   - 0: No sabe qué quiere.

4. **TIMING (0-25 pts):**
   - 25: "Para ya", "Urgente", "Este mes".
   - 20: "Próximo mes", "Q1".
   - 10: "Este año", "Solo mirando".
   - 0: "Futuro lejano".

DATOS DEL LEAD:
{lead_data}

HISTORIAL:
{conversacion}

Evalúa y responde JSON:
{{
  "budget_score": 0-25,
  "budget_justification": "...",
  "authority_score": 0-25,
  "authority_justification": "...",
  "need_score": 0-25,
  "need_justification": "...",
  "timing_score": 0-25,
  "timing_justification": "..."
}}"""


class QualifierAgent:
    """Agente que califica leads usando framework BANT."""
    
    async def qualify(self, context: ConversationContext) -> BANTScore:
        """Evalúa el lead según criterios BANT."""
        
        # Construir conversación
        conversation = self._build_conversation(context)
        
        system_prompt = QUALIFIER_SYSTEM_PROMPT.format(
            lead_data=context.lead_data or {},
            conversacion=conversation
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Evalúa este lead según el framework BANT."}
        ]
        
        # Llamar a DeepSeek
        result = await deepseek_client.chat_json(messages, temperature=0.2)
        
        # Parsear resultado
        try:
            return BANTScore(
                budget_score=min(25, max(0, int(result.get("budget_score", 0)))),
                budget_justification=result.get("budget_justification", ""),
                authority_score=min(25, max(0, int(result.get("authority_score", 0)))),
                authority_justification=result.get("authority_justification", ""),
                need_score=min(25, max(0, int(result.get("need_score", 0)))),
                need_justification=result.get("need_justification", ""),
                timing_score=min(25, max(0, int(result.get("timing_score", 0)))),
                timing_justification=result.get("timing_justification", "")
            )
        except Exception as e:
            print(f"Error parsing qualifier result: {e}")
            return BANTScore()
    
    def should_close(self, score: BANTScore) -> bool:
        """Determina si el lead está listo para cierre."""
        return score.total_score >= BANT_MIN_SCORE_FOR_CLOSE
    
    def should_nurture(self, score: BANTScore) -> bool:
        """Determina si el lead necesita nurturing."""
        total = score.total_score
        return BANT_MIN_SCORE_FOR_NURTURE <= total < BANT_MIN_SCORE_FOR_CLOSE
    
    def should_discard(self, score: BANTScore) -> bool:
        """Determina si el lead debe descartarse."""
        return score.total_score < BANT_MIN_SCORE_FOR_NURTURE
    
    def _build_conversation(self, context: ConversationContext) -> str:
        """Construye el historial de conversación."""
        lines = []
        for msg in context.message_history:
            role = "Usuario" if msg.direction == "inbound" else "Agente"
            lines.append(f"{role}: {msg.content}")
        lines.append(f"Usuario: {context.current_message}")
        return "\n".join(lines)


# Instancia global
qualifier_agent = QualifierAgent()
