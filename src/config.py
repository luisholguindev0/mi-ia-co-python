"""
Configuración central del sistema SDR WhatsApp.
Carga variables de entorno y define constantes del sistema.
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

# Cargar .env.local primero, luego .env como fallback
load_dotenv(".env.local")
load_dotenv(".env")


class Settings(BaseSettings):
    """Configuración del sistema cargada desde variables de entorno."""
    
    # DeepSeek API
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"
    
    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    
    # WhatsApp Business API
    whatsapp_token: str = os.getenv("WHATSAPP_TOKEN", "")
    whatsapp_phone_id: str = os.getenv("WHATSAPP_PHONE_ID", "")
    whatsapp_verify_token: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "mi_ia_verify_2025")
    whatsapp_api_url: str = "https://graph.facebook.com/v18.0"
    
    # Google Calendar
    google_calendar_credentials: Optional[str] = os.getenv("GOOGLE_CALENDAR_CREDENTIALS")
    use_mock_calendar: bool = os.getenv("USE_MOCK_CALENDAR", "true").lower() == "true"
    
    # Redis (Upstash)
    upstash_redis_url: Optional[str] = os.getenv("UPSTASH_REDIS_URL")
    upstash_redis_token: Optional[str] = os.getenv("UPSTASH_REDIS_TOKEN")
    
    # Empresa
    company_name: str = "Mi IA Colombia"
    company_timezone: str = "America/Bogota"
    consultation_duration_minutes: int = 15
    
    class Config:
        env_file = ".env"
        extra = "ignore"


# Instancia global de configuración
settings = Settings()


# Estados de la FSM
class FSMStates:
    """Constantes para los estados de la máquina de estados finitos."""
    INICIO = "INICIO"
    BIENVENIDA = "BIENVENIDA"
    EXTRACCION_DATOS = "EXTRACCION_DATOS"
    CALIFICACION = "CALIFICACION"
    OBJECIONES = "OBJECIONES"
    CIERRE = "CIERRE"
    AGENDADO = "AGENDADO"
    NUTRICION = "NUTRICION"
    COMPLETADO = "COMPLETADO"
    DESCARTADO = "DESCARTADO"


# Lista de estados válidos
VALID_STATES = [
    FSMStates.INICIO,
    FSMStates.BIENVENIDA,
    FSMStates.EXTRACCION_DATOS,
    FSMStates.CALIFICACION,
    FSMStates.OBJECIONES,
    FSMStates.CIERRE,
    FSMStates.AGENDADO,
    FSMStates.NUTRICION,
    FSMStates.COMPLETADO,
    FSMStates.DESCARTADO,
]


# BANT Scoring
BANT_MIN_SCORE_FOR_CLOSE = 60
BANT_MIN_SCORE_FOR_NURTURE = 30


# Intenciones del Router
class IntentTypes:
    """Tipos de intención para clasificación de mensajes."""
    GREETING = "saludo"
    INTEREST = "expresion_interes"
    QUESTION_SERVICE = "pregunta_servicio"
    QUESTION_PRICE = "pregunta_precio"
    OBJECTION = "objecion"
    SCHEDULE_REQUEST = "solicitud_agendar"
    PERSONAL_INFO = "info_personal"
    PAIN_POINT = "punto_dolor"
    NOT_INTERESTED = "no_interesado"
    OFF_TOPIC = "fuera_tema"
    CONFIRMATION = "confirmacion"
    REJECTION = "rechazo"
