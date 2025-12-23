"""
Grafo LangGraph para orquestación del sistema multi-agente.
Define el flujo de procesamiento de mensajes.
"""
from typing import TypedDict, Annotated, Literal, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from ..config import FSMStates, IntentTypes, BANT_MIN_SCORE_FOR_CLOSE
from ..models import Message, ConversationContext
from ..agents import (
    router_agent, 
    extractor_agent, 
    qualifier_agent, 
    conversational_agent,
    scheduler_agent
)
from ..integrations import supabase_client
from .states import TransitionTrigger, get_next_state


class AgentState(TypedDict):
    """Estado del grafo LangGraph."""
    phone_number: str
    current_message: str
    fsm_state: str
    lead_data: dict
    message_history: list
    bant_score: int
    intent: Optional[str]
    extracted_data: Optional[dict]
    response: Optional[str]
    next_state: Optional[str]
    available_slots: Optional[list]
    error: Optional[str]


async def route_message(state: AgentState) -> AgentState:
    """Nodo: Clasifica la intención del mensaje."""
    context = ConversationContext(
        phone_number=state["phone_number"],
        current_message=state["current_message"],
        message_history=[Message(**m) for m in state.get("message_history", [])],
        lead_data=state.get("lead_data"),
        fsm_state=state["fsm_state"],
        bant_score=state.get("bant_score", 0)
    )
    
    result = await router_agent.classify(context)
    
    state["intent"] = result.intencion_primaria
    state["extracted_data"] = result.datos_detectados if result.contiene_dato_extraible else None
    
    return state


async def extract_data(state: AgentState) -> AgentState:
    """Nodo: Extrae datos del lead."""
    context = ConversationContext(
        phone_number=state["phone_number"],
        current_message=state["current_message"],
        message_history=[Message(**m) for m in state.get("message_history", [])],
        lead_data=state.get("lead_data"),
        fsm_state=state["fsm_state"]
    )
    
    lead_data = await extractor_agent.extract(context)
    
    # Merge con datos existentes
    existing = state.get("lead_data") or {}
    new_data = lead_data.model_dump(exclude_none=True)
    merged = {**existing, **new_data}
    
    # Actualizar en base de datos
    if new_data:
        await supabase_client.update_extracted_facts(state["phone_number"], new_data)
    
    state["lead_data"] = merged
    
    return state


async def qualify_lead(state: AgentState) -> AgentState:
    """Nodo: Califica el lead según BANT."""
    context = ConversationContext(
        phone_number=state["phone_number"],
        current_message=state["current_message"],
        message_history=[Message(**m) for m in state.get("message_history", [])],
        lead_data=state.get("lead_data"),
        fsm_state=state["fsm_state"]
    )
    
    score = await qualifier_agent.qualify(context)
    
    state["bant_score"] = score.total_score
    
    # Actualizar en base de datos
    await supabase_client.update_bant_score(state["phone_number"], score.total_score)
    
    return state


async def determine_transition(state: AgentState) -> AgentState:
    """Nodo: Determina la transición de estado basada en intención y score."""
    current = state["fsm_state"]
    intent = state.get("intent", IntentTypes.OFF_TOPIC)
    bant = state.get("bant_score", 0)
    
    # Determinar trigger basado en intención y contexto
    trigger = None
    
    # Verificar si no está interesado
    if intent == IntentTypes.NOT_INTERESTED:
        trigger = TransitionTrigger.USER_NOT_INTERESTED
    
    # Lógica por estado
    elif current == FSMStates.INICIO:
        trigger = TransitionTrigger.NEW_MESSAGE
    
    elif current == FSMStates.BIENVENIDA:
        if intent in [IntentTypes.INTEREST, IntentTypes.QUESTION_SERVICE]:
            trigger = TransitionTrigger.USER_SHOWS_INTEREST
        elif intent == IntentTypes.PAIN_POINT:
            trigger = TransitionTrigger.USER_MENTIONS_NEED
    
    elif current == FSMStates.EXTRACCION_DATOS:
        lead = state.get("lead_data", {})
        # Verificar si tenemos datos mínimos: nombre + empresa + 1 dolor
        has_min_data = (
            lead.get("nombre") and 
            lead.get("empresa") and 
            (lead.get("puntos_dolor") or lead.get("presupuesto_min"))
        )
        if has_min_data:
            trigger = TransitionTrigger.DATA_COMPLETE
        else:
            trigger = TransitionTrigger.NEED_MORE_DATA
    
    elif current == FSMStates.CALIFICACION:
        if intent == IntentTypes.OBJECTION:
            trigger = TransitionTrigger.USER_OBJECTS
        elif bant >= BANT_MIN_SCORE_FOR_CLOSE:
            trigger = TransitionTrigger.LEAD_HOT
        elif bant >= 30:
            trigger = TransitionTrigger.LEAD_WARM
        else:
            trigger = TransitionTrigger.LEAD_COLD
    
    elif current == FSMStates.OBJECIONES:
        # Si después de manejar la objeción el usuario sigue interesado
        if intent in [IntentTypes.INTEREST, IntentTypes.CONFIRMATION]:
            trigger = TransitionTrigger.OBJECTION_RESOLVED
        else:
            trigger = TransitionTrigger.OBJECTION_UNRESOLVED
    
    elif current == FSMStates.CIERRE:
        if intent == IntentTypes.CONFIRMATION:
            trigger = TransitionTrigger.USER_CONFIRMS
        elif intent == IntentTypes.OBJECTION:
            trigger = TransitionTrigger.USER_OBJECTS
    
    elif current == FSMStates.AGENDADO:
        trigger = TransitionTrigger.APPOINTMENT_CONFIRMED
    
    # Obtener siguiente estado
    if trigger:
        next_state = get_next_state(current, trigger)
        if next_state:
            state["next_state"] = next_state
            # Actualizar en base de datos
            await supabase_client.update_fsm_state(state["phone_number"], next_state)
            state["fsm_state"] = next_state
    
    return state


async def generate_response(state: AgentState) -> AgentState:
    """Nodo: Genera la respuesta usando el agente conversacional."""
    context = ConversationContext(
        phone_number=state["phone_number"],
        current_message=state["current_message"],
        message_history=[Message(**m) for m in state.get("message_history", [])],
        lead_data=state.get("lead_data"),
        fsm_state=state["fsm_state"],
        bant_score=state.get("bant_score", 0)
    )
    
    # Caso especial: estado CIERRE - generar con slots
    if state["fsm_state"] == FSMStates.CIERRE:
        slots = scheduler_agent.get_available_slots()
        state["available_slots"] = slots
        
        lead_name = state.get("lead_data", {}).get("nombre", "")
        response = await conversational_agent.generate_closing_message(lead_name, slots)
    
    # Caso especial: estado AGENDADO - confirmar cita
    elif state["fsm_state"] == FSMStates.AGENDADO:
        slots = state.get("available_slots", [])
        selected = scheduler_agent.parse_user_selection(state["current_message"], slots)
        
        if selected:
            confirmation = scheduler_agent.format_confirmation(selected)
            lead_name = state.get("lead_data", {}).get("nombre", "")
            response = await conversational_agent.generate_confirmation(
                lead_name,
                confirmation["date"],
                confirmation["time"]
            )
        else:
            response = await conversational_agent.generate_response(context)
    
    # Caso normal: generar respuesta según estado
    else:
        response = await conversational_agent.generate_response(context)
    
    state["response"] = response
    return state


def should_extract_data(state: AgentState) -> Literal["extract", "skip"]:
    """Router: Decide si extraer datos."""
    # Extraer si el router detectó datos o si estamos en extracción
    if state.get("extracted_data") or state["fsm_state"] == FSMStates.EXTRACCION_DATOS:
        return "extract"
    return "skip"


def should_qualify(state: AgentState) -> Literal["qualify", "skip"]:
    """Router: Decide si calificar el lead."""
    # Calificar si estamos en calificación o tenemos suficientes datos
    if state["fsm_state"] in [FSMStates.CALIFICACION, FSMStates.CIERRE]:
        return "qualify"
    lead = state.get("lead_data", {})
    if lead.get("nombre") and lead.get("empresa"):
        return "qualify"
    return "skip"


def build_conversation_graph():
    """Construye el grafo de conversación."""
    
    # Crear grafo
    workflow = StateGraph(AgentState)
    
    # Añadir nodos
    workflow.add_node("route", route_message)
    workflow.add_node("extract", extract_data)
    workflow.add_node("qualify", qualify_lead)
    workflow.add_node("transition", determine_transition)
    workflow.add_node("respond", generate_response)
    
    # Definir flujo
    workflow.set_entry_point("route")
    
    # Route -> Extract (conditional)
    workflow.add_conditional_edges(
        "route",
        should_extract_data,
        {
            "extract": "extract",
            "skip": "qualify"
        }
    )
    
    # Extract -> Qualify
    workflow.add_edge("extract", "qualify")
    
    # Qualify -> Transition (conditional, pero siempre pasa)
    workflow.add_conditional_edges(
        "qualify",
        should_qualify,
        {
            "qualify": "transition",
            "skip": "transition"
        }
    )
    
    # Transition -> Respond
    workflow.add_edge("transition", "respond")
    
    # Respond -> END
    workflow.add_edge("respond", END)
    
    # Compilar con checkpointing
    checkpointer = MemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)
    
    return graph


# Instancia global del grafo
conversation_graph = build_conversation_graph()


async def process_message(phone_number: str, message: str) -> str:
    """
    Procesa un mensaje entrante y retorna la respuesta.
    Entry point principal del sistema.
    """
    # Obtener contexto de la conversación
    context = await supabase_client.get_conversation_context(phone_number)
    
    # Estado inicial
    lead = context.get("lead") or {}
    initial_state: AgentState = {
        "phone_number": phone_number,
        "current_message": message,
        "fsm_state": lead.get("fsm_state", FSMStates.INICIO),
        "lead_data": lead.get("extracted_facts", {}),
        "message_history": context.get("messages", []),
        "bant_score": lead.get("bant_score", 0),
        "intent": None,
        "extracted_data": None,
        "response": None,
        "next_state": None,
        "available_slots": None,
        "error": None
    }
    
    # Si es un nuevo lead, asegurarse de que existe
    if not context.get("lead"):
        await supabase_client.get_or_create_lead(phone_number)
    
    # Ejecutar grafo
    config = {"configurable": {"thread_id": phone_number}}
    result = await conversation_graph.ainvoke(initial_state, config)
    
    # Guardar mensaje entrante
    await supabase_client.save_message(Message(
        phone_number=phone_number,
        direction="inbound",
        content=message
    ))
    
    # Guardar respuesta
    response = result.get("response", "Lo siento, hubo un error. ¿Puedes intentar de nuevo?")
    await supabase_client.save_message(Message(
        phone_number=phone_number,
        direction="outbound",
        content=response
    ))
    
    return response
