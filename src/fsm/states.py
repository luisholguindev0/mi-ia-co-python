"""
Definición de estados de la FSM y sus transiciones.
"""
from enum import Enum
from typing import Dict, List, Optional
from ..config import FSMStates


class TransitionTrigger(Enum):
    """Triggers que causan transiciones de estado."""
    # Desde cualquier estado
    USER_NOT_INTERESTED = "user_not_interested"
    USER_SPAM = "user_spam"
    
    # Desde INICIO
    NEW_MESSAGE = "new_message"
    
    # Desde BIENVENIDA
    USER_SHOWS_INTEREST = "user_shows_interest"
    USER_MENTIONS_NEED = "user_mentions_need"
    
    # Desde EXTRACCION_DATOS
    DATA_COMPLETE = "data_complete"
    NEED_MORE_DATA = "need_more_data"
    
    # Desde CALIFICACION
    LEAD_HOT = "lead_hot"
    LEAD_WARM = "lead_warm"
    LEAD_COLD = "lead_cold"
    USER_OBJECTS = "user_objects"
    
    # Desde OBJECIONES
    OBJECTION_RESOLVED = "objection_resolved"
    OBJECTION_UNRESOLVED = "objection_unresolved"
    
    # Desde CIERRE
    USER_CONFIRMS = "user_confirms"
    USER_ASKS_MORE = "user_asks_more"
    NO_SLOT_WORKS = "no_slot_works"
    
    # Desde AGENDADO
    APPOINTMENT_CONFIRMED = "appointment_confirmed"
    
    # Desde NUTRICION
    USER_REENGAGES = "user_reengages"


# Matriz de transiciones: (estado_actual, trigger) -> estado_siguiente
TRANSITIONS: Dict[tuple, str] = {
    # Desde INICIO
    (FSMStates.INICIO, TransitionTrigger.NEW_MESSAGE): FSMStates.BIENVENIDA,
    
    # Desde BIENVENIDA
    (FSMStates.BIENVENIDA, TransitionTrigger.USER_SHOWS_INTEREST): FSMStates.CALIFICACION,
    (FSMStates.BIENVENIDA, TransitionTrigger.USER_MENTIONS_NEED): FSMStates.EXTRACCION_DATOS,
    (FSMStates.BIENVENIDA, TransitionTrigger.USER_NOT_INTERESTED): FSMStates.DESCARTADO,
    
    # Desde EXTRACCION_DATOS
    (FSMStates.EXTRACCION_DATOS, TransitionTrigger.DATA_COMPLETE): FSMStates.CALIFICACION,
    (FSMStates.EXTRACCION_DATOS, TransitionTrigger.NEED_MORE_DATA): FSMStates.EXTRACCION_DATOS,
    (FSMStates.EXTRACCION_DATOS, TransitionTrigger.USER_NOT_INTERESTED): FSMStates.DESCARTADO,
    
    # Desde CALIFICACION
    (FSMStates.CALIFICACION, TransitionTrigger.LEAD_HOT): FSMStates.CIERRE,
    (FSMStates.CALIFICACION, TransitionTrigger.LEAD_WARM): FSMStates.NUTRICION,
    (FSMStates.CALIFICACION, TransitionTrigger.LEAD_COLD): FSMStates.DESCARTADO,
    (FSMStates.CALIFICACION, TransitionTrigger.USER_OBJECTS): FSMStates.OBJECIONES,
    (FSMStates.CALIFICACION, TransitionTrigger.NEED_MORE_DATA): FSMStates.EXTRACCION_DATOS,
    
    # Desde OBJECIONES
    (FSMStates.OBJECIONES, TransitionTrigger.OBJECTION_RESOLVED): FSMStates.CALIFICACION,
    (FSMStates.OBJECIONES, TransitionTrigger.OBJECTION_UNRESOLVED): FSMStates.NUTRICION,
    (FSMStates.OBJECIONES, TransitionTrigger.USER_NOT_INTERESTED): FSMStates.DESCARTADO,
    
    # Desde CIERRE
    (FSMStates.CIERRE, TransitionTrigger.USER_CONFIRMS): FSMStates.AGENDADO,
    (FSMStates.CIERRE, TransitionTrigger.USER_ASKS_MORE): FSMStates.NUTRICION,
    (FSMStates.CIERRE, TransitionTrigger.NO_SLOT_WORKS): FSMStates.CIERRE,
    (FSMStates.CIERRE, TransitionTrigger.USER_OBJECTS): FSMStates.OBJECIONES,
    
    # Desde AGENDADO
    (FSMStates.AGENDADO, TransitionTrigger.APPOINTMENT_CONFIRMED): FSMStates.COMPLETADO,
    
    # Desde NUTRICION
    (FSMStates.NUTRICION, TransitionTrigger.USER_REENGAGES): FSMStates.CALIFICACION,
    (FSMStates.NUTRICION, TransitionTrigger.USER_NOT_INTERESTED): FSMStates.DESCARTADO,
}


def get_next_state(current_state: str, trigger: TransitionTrigger) -> Optional[str]:
    """
    Obtiene el siguiente estado basado en el estado actual y el trigger.
    Retorna None si no hay transición válida.
    """
    return TRANSITIONS.get((current_state, trigger))


def get_valid_triggers(current_state: str) -> List[TransitionTrigger]:
    """
    Obtiene los triggers válidos para un estado dado.
    """
    valid = []
    for (state, trigger), _ in TRANSITIONS.items():
        if state == current_state:
            valid.append(trigger)
    return valid


def is_terminal_state(state: str) -> bool:
    """
    Verifica si un estado es terminal (no hay más transiciones).
    """
    return state in [FSMStates.COMPLETADO, FSMStates.DESCARTADO]
