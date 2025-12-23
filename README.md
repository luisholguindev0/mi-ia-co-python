# Sistema IA SDR WhatsApp - Mi IA Colombia

Sistema de Inteligencia Artificial autónomo para WhatsApp que actúa como Sales Development Representative (SDR), con capacidad de conversación multi-lead, extracción de datos, FSM de ventas y agendamiento automatizado.

## Stack Tecnológico

- **Runtime:** Python 3.12
- **Framework:** FastAPI
- **Orquestación:** LangGraph
- **LLM:** DeepSeek-V3
- **Base de Datos:** Supabase (PostgreSQL)
- **Cache:** Upstash Redis
- **Hosting:** Vercel
- **WhatsApp:** Meta Cloud API
- **Calendario:** Google Calendar API

## Estructura del Proyecto

```
src/
├── main.py              # Entry point FastAPI
├── config.py            # Configuración y variables de entorno
├── agents/              # Agentes especializados
│   ├── __init__.py
│   ├── router.py        # Clasificador de intención
│   ├── extractor.py     # Extractor de datos NER
│   ├── qualifier.py     # Calificador BANT
│   ├── conversational.py # Generador de respuestas
│   └── scheduler.py     # Agendamiento
├── fsm/                 # Máquina de Estados Finitos
│   ├── __init__.py
│   ├── states.py        # Definición de estados
│   └── graph.py         # LangGraph orchestration
├── integrations/        # Integraciones externas
│   ├── __init__.py
│   ├── whatsapp.py      # WhatsApp Business API
│   ├── calendar.py      # Google Calendar
│   └── supabase_client.py
├── models/              # Pydantic models
│   ├── __init__.py
│   ├── lead.py
│   └── message.py
├── guardrails/          # Seguridad
│   ├── __init__.py
│   └── simple.py
└── utils/
    ├── __init__.py
    └── logging.py
```

## Instalación

```bash
pip install -r requirements.txt
```

## Variables de Entorno

```env
# DeepSeek
DEEPSEEK_API_KEY=

# Supabase
SUPABASE_URL=
SUPABASE_KEY=

# WhatsApp Business API
WHATSAPP_TOKEN=
WHATSAPP_PHONE_ID=
WHATSAPP_VERIFY_TOKEN=

# Google Calendar
GOOGLE_CALENDAR_CREDENTIALS=

# Upstash Redis
UPSTASH_REDIS_URL=
UPSTASH_REDIS_TOKEN=
```

## Desarrollo Local

```bash
uvicorn src.main:app --reload
```
