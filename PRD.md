# PRD: Sistema de IA SDR Autónomo para WhatsApp
## Mi IA Colombia – AI Growth & Automation Partner

**Versión:** 1.0  
**Fecha:** 22 de Diciembre de 2025  
**Cliente:** Mi IA Colombia (https://mi-ia-co-blush.vercel.app)  
**Ubicación:** Barranquilla, Colombia

---

## 1. Resumen Ejecutivo

### 1.1 Descripción del Producto
Sistema de Inteligencia Artificial autónomo para WhatsApp que actúa como Sales Development Representative (SDR) empresarial, capaz de:

- **Conversación simultánea** con múltiples leads en paralelo
- **Extracción automática de datos** (nombre, empresa, ciudad, puntos de dolor, presupuesto, urgencia)
- **Comportamiento FSM (Finite State Machine)** para flujos de ventas deterministas
- **Agendamiento automatizado** de llamadas de consultoría de 15 minutos

### 1.2 Propuesta de Valor
Mi IA Colombia vende "sistemas con IA" a empresas colombianas. Este agente será el primer punto de contacto digital, calificando leads 24/7, extrayendo información crítica de manera conversacional y convirtiendo prospects en llamadas de consultoría agendadas.

### 1.3 Métricas de Éxito Objetivo (MVP Startup)

| Métrica | Objetivo MVP | Objetivo Escalado |
|---------|--------------|-------------------|
| Capacidad simultánea | 10-50 leads | 500+ leads |
| Tiempo de respuesta | < 60 segundos | < 30 segundos |
| Tasa de extracción de datos | > 85% campos | > 95% campos |
| Tasa de conversión a cita | > 10% | > 15% |
| Precisión de clasificación FSM | > 90% | > 98% |
| Uptime del sistema | 99% | 99.9% |

> [!NOTE]
> Métricas ajustadas para fase inicial de startup sin tráfico existente. Escalar según crecimiento orgánico.

---

## 2. Análisis de Contexto

### 2.1 Perfil del Cliente: Mi IA Colombia

**Posicionamiento:** "AI Growth & Automation Partner" – Startup colombiana que desarrolla aplicaciones web personalizadas y agentes de ventas con IA.

> [!IMPORTANT]
> **Contexto Real de la Startup:**
> - Sin base de leads existente
> - Presupuesto limitado para infraestructura
> - Sin presencia digital consolidada
> - Necesidad de validar product-market fit

**Servicios Principales:**
- Apps Web con Next.js y Server Components
- Agentes de ventas inteligentes con IA
- Automatización de procesos

**Stack Tecnológico Optimizado para Costo:**
- Next.js (Vercel Free Tier)
- **DeepSeek API** como LLM principal (costo ~95% menor que GPT-4)
- Servicios gratuitos/freemium donde sea posible

**Propuesta de Valor:**
> "Sistemas de IA que trabajan 24/7 para que tu negocio crezca."

### 2.2 Mercado Objetivo

**Clientes Potenciales de Mi IA Colombia:**
- PYMEs y empresas medianas colombianas
- Sectores: Legal, Salud, Restaurantes, Retail, Servicios B2B
- Empresas buscando automatización y digitalización
- Presupuestos: $5M - $100M COP por proyecto

**Canal Principal:** WhatsApp (dominante en comunicación empresarial en Colombia)

---

## 3. Arquitectura del Sistema

### 3.1 Visión General de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAPA DE PRESENTACIÓN                              │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
│  │   WhatsApp      │    │   Dashboard     │    │   API REST      │      │
│  │   Business API  │    │   Admin         │    │   Webhooks      │      │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘      │
└───────────┼──────────────────────┼──────────────────────┼───────────────┘
            │                      │                      │
            ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAPA DE ORQUESTACIÓN                              │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         LangGraph Engine                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │    FSM       │  │  Checkpoints  │  │  Router      │          │    │
│  │  │  Controller  │  │  Manager      │  │  Agent       │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     CAPA DE AGENTES ESPECIALIZADOS                       │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Agente    │ │  Agente    │ │  Agente    │ │  Agente    │           │
│  │  Router    │ │  Extractor │ │  Qualifier │ │  Scheduler │           │
│  │(DeepSeek)  │ │ (DeepSeek) │ │ (DeepSeek) │ │ (DeepSeek) │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
└─────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAPA DE SERVICIOS                                │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│  │   Conocimiento │  │   Memoria     │  │  Guardrails   │               │
│  │   (JSON/DB)   │  │  (Supabase)   │  │   (Python)    │               │
│  └───────────────┘  └───────────────┘  └───────────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      CAPA DE INTEGRACIONES                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                        │
│  │  WhatsApp  │  │  Google    │  │   CRM      │                        │
│  │ Cloud API  │  │ Calendar   │  │(Sheets/DB) │                        │
│  └────────────┘  └────────────┘  └────────────┘                        │
└─────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       CAPA DE PERSISTENCIA                               │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐      │
│  │      Supabase (PostgreSQL)  │  │    Upstash Redis (Cache)    │      │
│  │  - Estado FSM               │  │  - Sesiones                 │      │
│  │  - Leads, Mensajes, Citas   │  │  - Rate limiting            │      │
│  │  - Memoria conversacional   │  │                             │      │
│  └─────────────────────────────┘  └─────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Componentes Principales

#### 3.2.1 WhatsApp Business API Integration
**Propósito:** Interfaz de comunicación principal con leads

**Tecnología:** Meta WhatsApp Business Cloud API

**Funcionalidades:**
- Recepción de mensajes entrantes vía webhook
- Envío de mensajes de texto, botones interactivos y listas
- Manejo de medios (imágenes, documentos, audio)
- Templates aprobados para mensajes outbound
- Estado de lectura y entrega

**Configuración Requerida:**
```json
{
  "webhook_url": "https://api.mi-ia.co/whatsapp/webhook",
  "verify_token": "MI_IA_VERIFY_TOKEN_2025",
  "app_secret": "[ENCRYPTED]",
  "phone_number_id": "[FROM_META_PORTAL]",
  "business_account_id": "[FROM_META_PORTAL]"
}
```

#### 3.2.2 LangGraph Orchestration Engine
**Propósito:** Motor central de orquestación de agentes

**Características Críticas:**
- **Grafos Cíclicos:** Soporte para loops de conversación
- **Checkpointing:** Persistencia de estado en PostgreSQL
- **Concurrencia:** Manejo asíncrono de múltiples conversaciones
- **Thread Safety:** Bloqueo optimista para evitar race conditions

---

## 4. Máquina de Estados Finitos (FSM)

### 4.1 Diagrama de Estados

```
                           ┌─────────────────┐
                           │     INICIO      │
                           │   (New Lead)    │
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │   BIENVENIDA    │
                           │  (Greeting)     │
                           └────────┬────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
           ┌────────────┐  ┌────────────┐  ┌────────────┐
           │ EXTRACCIÓN │  │CALIFICACIÓN│  │ OBJECIÓN   │
           │   DATOS    │◄─┤   BANT     │──►│  HANDLER   │
           │            │  │            │  │            │
           └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
                 │               │               │
                 └───────────────┼───────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
           ┌────────────────┐        ┌────────────────┐
           │    CIERRE      │        │   NUTRICIÓN    │
           │  (Scheduling)  │        │  (Nurturing)   │
           └───────┬────────┘        └───────┬────────┘
                   │                         │
                   ▼                         │
           ┌────────────────┐                │
           │   AGENDADO     │◄───────────────┘
           │  (Confirmed)   │
           └───────┬────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌────────────┐         ┌────────────┐
│ COMPLETADO │         │ DESCARTADO │
│ (Success)  │         │ (Discarded)│
└────────────┘         └────────────┘
```

### 4.2 Definición de Estados

#### INICIO (S0)
**Trigger:** Mensaje entrante de nuevo número
**Acciones:**
1. Crear registro de lead en base de datos
2. Inicializar objeto de estado
3. Asignar thread_id único
4. Transición automática a BIENVENIDA

#### BIENVENIDA (S1)
**Objetivo:** Establecer rapport y detectar intención
**Mensaje Tipo:**
```
¡Hola! 👋 Soy el asistente virtual de Mi IA Colombia.

Ayudamos a empresas a crecer con sistemas de inteligencia artificial 
personalizados: apps web de alto rendimiento y agentes de ventas que 
trabajan 24/7.

¿En qué puedo ayudarte hoy?
```
**Transiciones:**
- → EXTRACCIÓN_DATOS: Usuario menciona necesidad específica
- → CALIFICACIÓN: Usuario expresa interés general
- → DESCARTADO: Usuario indica que no está interesado

#### EXTRACCIÓN_DATOS (S2)
**Objetivo:** Recopilar información del lead de forma natural
**Datos a Extraer:**

| Campo | Prioridad | Ejemplo de Detección |
|-------|-----------|----------------------|
| nombre | Alta | "Me llamo Juan" → nombre: "Juan" |
| empresa | Alta | "Soy de TechCorp" → empresa: "TechCorp" |
| ciudad | Media | "Estamos en Bogotá" → ciudad: "Bogotá" |
| puntos_dolor | Alta | "Perdemos clientes por responder tarde" |
| presupuesto | Alta | "Tenemos entre 20 y 30 millones" |
| urgencia | Alta | "Necesitamos esto para enero" |
| cargo | Media | "Soy el gerente de ventas" |
| telefono | Baja | Número de WhatsApp ya disponible |
| email | Baja | "Mi correo es juan@techcorp.co" |

**Lógica de Extracción:**
```python
class LeadDataSchema(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre del contacto")
    empresa: Optional[str] = Field(None, description="Nombre de la empresa")
    ciudad: Optional[str] = Field(None, description="Ciudad en Colombia")
    puntos_dolor: Optional[List[str]] = Field(default_factory=list)
    presupuesto_min: Optional[int] = Field(None, ge=0)
    presupuesto_max: Optional[int] = Field(None, ge=0)
    urgencia: Optional[str] = Field(None, pattern="^(baja|media|alta|urgente)$")
    cargo: Optional[str] = None
    email: Optional[str] = None
```

**Transiciones:**
- → CALIFICACIÓN: Datos críticos completados (nombre + empresa + 1 dolor)
- → Permanece: Faltan datos críticos (loop de preguntas)

#### CALIFICACIÓN (S3)
**Objetivo:** Evaluar criterios BANT adaptados
**Framework BANT para Mi IA Colombia:**

| Criterio | Pregunta Guía | Puntuación |
|----------|---------------|------------|
| **Budget** | ¿Presupuesto > $5M COP? | 0-25 pts |
| **Authority** | ¿Es decisor o influenciador? | 0-25 pts |
| **Need** | ¿Tiene dolor identificado y urgente? | 0-25 pts |
| **Timing** | ¿Quiere implementar en < 3 meses? | 0-25 pts |

**Score Mínimo para Cierre:** 60 puntos

**Transiciones:**
- → CIERRE: Score ≥ 60 puntos
- → NUTRICIÓN: Score 30-59 puntos
- → DESCARTADO: Score < 30 puntos

#### OBJECIONES (S4)
**Objetivo:** Manejar objeciones comunes
**Objeciones Frecuentes y Respuestas:**

| Objeción | Respuesta Estratégica |
|----------|----------------------|
| "Es muy caro" | Valor ROI: "El agente trabaja 24/7, reemplaza 3 SDRs a fracción del costo" |
| "No confío en IA" | Social proof + garantía: "Casos en Colombia, garantía de satisfacción" |
| "Ya tengo chatbot" | Diferenciación: "Esto no es un chatbot, es un sistema que cualifica y agenda" |
| "No es el momento" | Urgencia: "¿Cuántos leads pierde cada mes por no responder a tiempo?" |

**Transiciones:**
- → CALIFICACIÓN: Objeción resuelta
- → NUTRICIÓN: Objeción parcialmente resuelta
- → DESCARTADO: Objeción no superable

#### CIERRE (S5)
**Objetivo:** Agendar llamada de consultoría de 15 minutos
**Flujo:**
1. Consultar disponibilidad en Google Calendar
2. Ofrecer 3 opciones de horario en zona horaria colombiana (COT)
3. Confirmar selección del usuario
4. Crear evento en calendario
5. Enviar confirmación con link de Meet/Zoom

**Mensaje Tipo:**
```
¡Excelente, {nombre}! 🎯

Me encantaría que hables directamente con nuestro equipo de soluciones.

Tenemos disponibilidad para una llamada de 15 minutos esta semana:
📅 Martes 24 de diciembre - 10:00 AM
📅 Miércoles 25 de diciembre - 3:00 PM  
📅 Jueves 26 de diciembre - 11:00 AM

¿Cuál te funciona mejor?
```

**Transiciones:**
- → AGENDADO: Usuario confirma horario
- → NUTRICIÓN: Usuario pide más información
- → Permanece: Ningún horario funciona (ofrecer más opciones)

#### AGENDADO (S6)
**Objetivo:** Confirmación y seguimiento
**Acciones:**
1. Enviar resumen de la cita
2. Actualizar CRM con estado "Reunión Agendada"
3. Programar recordatorio 24h antes
4. Programar recordatorio 1h antes

**Mensaje de Confirmación:**
```
✅ ¡Cita confirmada!

📅 Fecha: {fecha}
🕐 Hora: {hora} (Hora Colombia)
📍 Link: {meeting_link}

Hablarás con {asesor_nombre}, quien te ayudará a diseñar 
la solución perfecta para {empresa}.

Te enviaré un recordatorio antes de la llamada. ¡Hasta pronto! 🚀
```

#### NUTRICIÓN (S7)
**Objetivo:** Mantener engagement con leads no listos
**Acciones:**
- Enviar contenido de valor (casos de estudio, artículos)
- Programar re-engagement en 7, 14, 30 días
- Monitorear señales de compra

#### COMPLETADO (S8)
**Estado Final:** Lead convertido exitosamente

#### DESCARTADO (S9)
**Estado Final:** Lead no cualificado
**Razones de Descarte:**
- No interesado
- Sin presupuesto
- Fuera de geografía target
- Competencia
- Spam/Bot

---

## 5. Sistema de Agentes Especializados

### 5.1 Agente Router (Clasificador de Intención)

**Modelo:** DeepSeek-V3 (ultra bajo costo, excelente rendimiento)

**Función:** Clasificar intención de cada mensaje entrante

**Intenciones Detectadas:**
```python
class IntentType(Enum):
    GREETING = "saludo"
    INTEREST_EXPRESSION = "expresion_interes"
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
```

**Prompt del Router:**
```
Eres un clasificador de intenciones para un agente de ventas de Mi IA Colombia.

CONTEXTO DE LA EMPRESA:
- Mi IA Colombia vende sistemas de IA personalizados
- Servicios: Apps web con IA, Agentes de ventas, Automatización
- Mercado: Empresas colombianas

MENSAJE DEL USUARIO: {mensaje}
HISTORIAL RECIENTE: {ultimos_3_mensajes}
ESTADO ACTUAL: {estado_fsm}
DATOS EXTRAÍDOS: {datos_lead}

Clasifica la intención y determina la siguiente acción.

Responde en JSON:
{
  "intencion_primaria": "...",
  "intencion_secundaria": "...",
  "contiene_dato_extraible": true/false,
  "datos_detectados": {...},
  "siguiente_estado_sugerido": "...",
  "confianza": 0.0-1.0
}
```

### 5.2 Agente Extractor (Data Extraction)

**Modelo:** DeepSeek-V3 (excelente para extracción estructurada, muy económico)

**Función:** Extraer entidades nombradas y datos del lead

**Técnica:** Named Entity Recognition (NER) + Inferencia contextual

**Prompt del Extractor:**
```
Eres un experto en extracción de información de conversaciones de ventas.

HISTORIAL COMPLETO DE CONVERSACIÓN:
{conversacion}

DATOS YA EXTRAÍDOS:
{datos_actuales}

INSTRUCCIONES:
1. Extrae SOLO información explícitamente mencionada
2. NO inventes datos que no estén en el texto
3. Infiere ciudad/ubicación de contexto si es claro
4. Convierte presupuestos a rango numérico COP
5. Clasifica urgencia: baja/media/alta/urgente

FORMATO DE SALIDA JSON:
{
  "nombre": "...",
  "empresa": "...",
  "cargo": "...",
  "ciudad": "...",
  "email": "...",
  "puntos_dolor": ["dolor1", "dolor2"],
  "presupuesto_min": 0,
  "presupuesto_max": 0,
  "urgencia": "media",
  "contexto_adicional": "..."
}
```

### 5.3 Agente Calificador (BANT Scorer)

**Modelo:** DeepSeek-V3 (razonamiento complejo, costo mínimo)

**Función:** Evaluar calidad del lead según framework BANT

**Output:**
```python
class BANTScore(BaseModel):
    budget_score: int = Field(ge=0, le=25)
    budget_justification: str
    authority_score: int = Field(ge=0, le=25)
    authority_justification: str
    need_score: int = Field(ge=0, le=25)
    need_justification: str
    timing_score: int = Field(ge=0, le=25)
    timing_justification: str
    total_score: int = Field(ge=0, le=100)
    qualification_status: Literal["hot", "warm", "cold", "disqualified"]
    recommended_action: str
```

### 5.4 Agente Conversacional (Response Generator)

**Modelo:** DeepSeek-V3 (modelo único para simplicidad y bajo costo)

**Función:** Generar respuestas naturales y persuasivas

**Personalidad del Agente:**
```
IDENTIDAD:
- Nombre: Asistente virtual de Mi IA Colombia
- Tono: Profesional pero cercano, colombiano, confiable
- Estilo: Directo, orientado a soluciones, empático

REGLAS DE COMUNICACIÓN:
1. Máximo 3 párrafos por mensaje
2. Usar emojis con moderación (1-2 por mensaje)
3. Hacer UNA pregunta por mensaje (excepto cierre)
4. Personalizar con nombre cuando esté disponible
5. Referenciar dolores mencionados anteriormente
6. Nunca prometer precios específicos sin validación
7. Siempre guiar hacia el agendamiento

CONOCIMIENTO DEL PRODUCTO:
- Apps web de alto rendimiento (Next.js, React)
- Agentes de ventas con IA 24/7
- Automatización de procesos
- Integraciones con CRM, WhatsApp, calendarios
- Tiempo de implementación: 4-12 semanas según complejidad

PROPUESTA DE VALOR CLAVE:
"Sistemas de IA que generan ROI medible: más ventas, menos tiempo 
perdido en tareas repetitivas, clientes atendidos las 24 horas."
```

### 5.5 Agente Scheduler (Appointment Setter)

**Modelo:** DeepSeek-V3 (lógica simple, ultra bajo costo)

**Función:** Gestionar lógica de agendamiento

**Integraciones MCP:**
- Google Calendar API
- Zoom/Google Meet API

**Flujo de Agendamiento:**
```python
async def schedule_appointment(lead_data: LeadData, preferred_slot: str):
    # 1. Verificar disponibilidad real
    available_slots = await mcp_calendar.get_availability(
        calendar_id="consultoria@mi-ia.co",
        duration_minutes=15,
        days_ahead=7,
        timezone="America/Bogota"
    )
    
    # 2. Validar slot solicitado
    if preferred_slot not in available_slots:
        return suggest_alternatives(available_slots[:3])
    
    # 3. Crear evento
    event = await mcp_calendar.create_event(
        title=f"Consultoría Mi IA - {lead_data.empresa}",
        start_time=preferred_slot,
        duration_minutes=15,
        attendees=[lead_data.email],
        description=generate_meeting_description(lead_data),
        conferencing="google_meet"
    )
    
    # 4. Actualizar CRM
    await mcp_crm.update_lead(
        lead_id=lead_data.id,
        status="meeting_scheduled",
        meeting_link=event.meeting_link,
        meeting_time=event.start_time
    )
    
    return event
```

---

## 6. Sistema de Memoria y Contexto

### 6.1 Arquitectura de Memoria

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORIA DEL SISTEMA                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              MEMORIA A CORTO PLAZO                   │    │
│  │  ┌─────────────────┐  ┌─────────────────┐          │    │
│  │  │ Contexto de     │  │ Últimos 10      │          │    │
│  │  │ Conversación    │  │ Mensajes        │          │    │
│  │  └─────────────────┘  └─────────────────┘          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               MEMORIA A LARGO PLAZO                  │    │
│  │  ┌─────────────────┐  ┌─────────────────┐          │    │
│  │  │ Hechos          │  │ Preferencias    │          │    │
│  │  │ Extraídos       │  │ del Usuario     │          │    │
│  │  └─────────────────┘  └─────────────────┘          │    │
│  │  ┌─────────────────┐  ┌─────────────────┐          │    │
│  │  │ Historial de    │  │ Interacciones   │          │    │
│  │  │ Objeciones      │  │ Previas         │          │    │
│  │  └─────────────────┘  └─────────────────┘          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            GRAFO DE CONOCIMIENTO (GraphRAG)          │    │
│  │  ┌─────────────────┐  ┌─────────────────┐          │    │
│  │  │ Productos y     │  │ Casos de        │          │    │
│  │  │ Servicios       │  │ Éxito           │          │    │
│  │  └─────────────────┘  └─────────────────┘          │    │
│  │  ┌─────────────────┐  ┌─────────────────┐          │    │
│  │  │ Objeciones y    │  │ Competencia     │          │    │
│  │  │ Respuestas      │  │ (Info Pública)  │          │    │
│  │  └─────────────────┘  └─────────────────┘          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Implementación de Memoria (Supabase - Costo $0)

> [!TIP]
> En lugar de Zep ($49/mes), usamos tablas JSON en Supabase para almacenar hechos extraídos.

**Configuración:**
```python
from supabase import create_client
import json

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def save_extracted_facts(phone_number: str, facts: dict):
    """Guarda hechos extraídos en Supabase (reemplaza Zep)"""
    
    # Obtener lead existente
    result = supabase.table("leads").select("*").eq(
        "phone_number", phone_number
    ).execute()
    
    if result.data:
        lead = result.data[0]
        # Merge con hechos existentes
        existing_facts = lead.get("extracted_facts", {})
        merged_facts = {**existing_facts, **facts}
        
        supabase.table("leads").update({
            "extracted_facts": merged_facts,
            "updated_at": "now()"
        }).eq("phone_number", phone_number).execute()
    
    return merged_facts

async def get_conversation_context(phone_number: str, last_n: int = 10):
    """Obtiene contexto de conversación para el prompt"""
    
    # Obtener últimos mensajes
    messages = supabase.table("messages").select("*").eq(
        "lead_id", 
        supabase.table("leads").select("id").eq("phone_number", phone_number)
    ).order("created_at", desc=True).limit(last_n).execute()
    
    # Obtener hechos
    lead = supabase.table("leads").select(
        "extracted_facts, fsm_state, bant_score"
    ).eq("phone_number", phone_number).execute()
    
    return {
        "messages": messages.data[::-1],  # Orden cronológico
        "facts": lead.data[0].get("extracted_facts", {}),
        "current_state": lead.data[0].get("fsm_state"),
        "bant_score": lead.data[0].get("bant_score", 0)
    }
```

### 6.3 Conocimiento del Producto (JSON Simple)

> [!NOTE]
> GraphRAG con Neo4j es una **mejora futura**. Para MVP, usamos JSON estructurado.

**Archivo: `knowledge_base.json`**
```json
{
  "servicios": [
    {
      "nombre": "Agente SDR WhatsApp",
      "descripcion": "IA que cualifica leads y agenda citas 24/7",
      "precio_rango": "$10M - $30M COP",
      "tiempo_implementacion": "4-8 semanas"
    },
    {
      "nombre": "App Web Personalizada",
      "descripcion": "Desarrollo web con Next.js y React",
      "precio_rango": "$15M - $100M COP",
      "tiempo_implementacion": "6-16 semanas"
    }
  ],
  "objeciones": {
    "precio": "El ROI se ve en los primeros 3 meses. Un agente IA trabaja 24/7 por una fracción del costo de un SDR humano.",
    "confianza": "Tenemos casos de éxito con empresas colombianas. Además, ofrecemos garantía de satisfacción.",
    "chatbot": "Esto no es un chatbot simple. Es un sistema que cualifica, extrae datos y agenda automáticamente."
  },
  "industrias_target": ["Restaurantes", "Legal", "Salud", "Retail", "B2B Services"]
}
```

**Uso en el agente:**
```python
import json

with open("knowledge_base.json") as f:
    KNOWLEDGE = json.load(f)

def get_objection_response(objection_type: str) -> str:
    return KNOWLEDGE["objeciones"].get(objection_type, KNOWLEDGE["objeciones"]["default"])
```

---

## 7. Seguridad y Guardrails

### 7.1 Guardrails Ligeros (Sin NeMo - Costo Cero)

> [!TIP]
> Para una startup, NeMo Guardrails puede ser overkill. Implementamos guardrails simples en código.

**Archivo: `guardrails.py`**
```python
# Guardrails simples sin dependencias costosas
import re
from typing import Tuple

class SimpleGuardrails:
    """Guardrails ligeros para startup - costo $0"""
    
    BLOCKED_PATTERNS = [
        r"precio exacto",
        r"cuánto cuesta exactamente",
        r"descuento",
        r"gratis",
    ]
    
    BLOCKED_TOPICS = ["política", "religión", "competencia"]
    
    @classmethod
    def check_input(cls, message: str) -> Tuple[bool, str]:
        """Verifica si el input es apropiado"""
        message_lower = message.lower()
        
        for topic in cls.BLOCKED_TOPICS:
            if topic in message_lower:
                return False, "topic_blocked"
        
        return True, "allowed"
    
    @classmethod  
    def check_output(cls, response: str) -> Tuple[bool, str]:
        """Verifica que la respuesta no prometa cosas indebidas"""
        for pattern in cls.BLOCKED_PATTERNS:
            if re.search(pattern, response.lower()):
                return False, "needs_revision"
        
        return True, "allowed"
```

### 7.2 Validación de Datos PII

**Colombia-Specific PII Detection:**
```python
import re

class ColombianPIIDetector:
    patterns = {
        "cedula": r"\b\d{6,10}\b",  # Cédula colombiana
        "nit": r"\b\d{9}-\d\b",      # NIT empresarial
        "telefono": r"\b3\d{9}\b",   # Celular colombiano
        "tarjeta": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        "email": r"\b[\w.-]+@[\w.-]+\.\w+\b"
    }
    
    def detect_and_mask(self, text: str) -> tuple[str, dict]:
        detected = {}
        masked_text = text
        
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                detected[pii_type] = matches
                for match in matches:
                    masked_text = masked_text.replace(
                        match, 
                        f"[{pii_type.upper()}_REDACTED]"
                    )
        
        return masked_text, detected
```

### 7.3 Topic Rails - Límites Conversacionales

```python
ALLOWED_TOPICS = [
    "servicios_mi_ia",
    "precios_generales",
    "proceso_trabajo",
    "agendamiento",
    "casos_exito",
    "tecnologias",
    "tiempos_entrega"
]

BLOCKED_TOPICS = [
    "politica",
    "religion",
    "competencia_directa",
    "informacion_interna",
    "datos_otros_clientes"
]

DEFLECTION_RESPONSES = {
    "politica": "Prefiero mantener nuestra conversación enfocada en cómo podemos ayudar a tu negocio. ¿En qué área de automatización puedo ayudarte?",
    "competencia_directa": "No tengo información detallada sobre otras empresas, pero puedo contarte todo sobre nuestras soluciones. ¿Qué necesidad específica tienes?",
    "default": "Eso está fuera de mi área de conocimiento. ¿Hay algo sobre automatización o IA para tu empresa en lo que pueda ayudarte?"
}
```

---

## 8. Integraciones MCP

### 8.1 MCP Server: WhatsApp

```python
# mcp_servers/whatsapp_server.py
from mcp.server import Server, Resource, Tool

whatsapp_server = Server("whatsapp")

@whatsapp_server.tool("send_message")
async def send_message(phone_number: str, message: str, buttons: list = None):
    """Envía mensaje de WhatsApp al número especificado"""
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "interactive" if buttons else "text"
    }
    
    if buttons:
        payload["interactive"] = {
            "type": "button",
            "body": {"text": message},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": b["id"], "title": b["title"]}}
                    for b in buttons[:3]  # WhatsApp limit: 3 buttons
                ]
            }
        }
    else:
        payload["text"] = {"body": message}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{WHATSAPP_API_URL}/{PHONE_NUMBER_ID}/messages",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
            json=payload
        )
    
    return response.json()

@whatsapp_server.tool("send_template")
async def send_template(phone_number: str, template_name: str, params: dict):
    """Envía mensaje de plantilla aprobada"""
    # Implementación...
    pass

@whatsapp_server.resource("contact/{phone_number}")
async def get_contact(phone_number: str):
    """Obtiene información del contacto de WhatsApp"""
    # Implementación...
    pass
```

### 8.2 MCP Server: Google Calendar

```python
# mcp_servers/calendar_server.py
from mcp.server import Server, Tool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

calendar_server = Server("google_calendar")

@calendar_server.tool("get_availability")
async def get_availability(
    calendar_id: str,
    duration_minutes: int = 15,
    days_ahead: int = 7,
    timezone: str = "America/Bogota"
):
    """Obtiene slots disponibles en el calendario"""
    service = build('calendar', 'v3', credentials=get_credentials())
    
    now = datetime.now(pytz.timezone(timezone))
    end = now + timedelta(days=days_ahead)
    
    # Obtener busy times
    freebusy = service.freebusy().query(body={
        "timeMin": now.isoformat(),
        "timeMax": end.isoformat(),
        "timeZone": timezone,
        "items": [{"id": calendar_id}]
    }).execute()
    
    # Calcular slots libres
    available_slots = calculate_free_slots(
        freebusy["calendars"][calendar_id]["busy"],
        now, end, duration_minutes, timezone
    )
    
    return available_slots

@calendar_server.tool("create_event")
async def create_event(
    title: str,
    start_time: str,
    duration_minutes: int,
    attendees: list[str],
    description: str,
    conferencing: str = "google_meet"
):
    """Crea evento con conferencia de video"""
    service = build('calendar', 'v3', credentials=get_credentials())
    
    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Bogota',
        },
        'end': {
            'dateTime': (
                datetime.fromisoformat(start_time) + 
                timedelta(minutes=duration_minutes)
            ).isoformat(),
            'timeZone': 'America/Bogota',
        },
        'attendees': [{'email': email} for email in attendees],
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }
    
    result = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,
        sendUpdates='all'
    ).execute()
    
    return {
        "event_id": result['id'],
        "meeting_link": result.get('hangoutLink'),
        "start_time": result['start']['dateTime']
    }
```

### 8.3 MCP Server: CRM (HubSpot)

```python
# mcp_servers/hubspot_server.py
from mcp.server import Server, Tool, Resource
import hubspot
from hubspot.crm.contacts import ApiException

hubspot_server = Server("hubspot")

@hubspot_server.tool("create_or_update_contact")
async def create_or_update_contact(
    phone: str,
    properties: dict
):
    """Crea o actualiza contacto en HubSpot"""
    client = hubspot.Client.create(access_token=HUBSPOT_TOKEN)
    
    # Buscar contacto existente
    search_request = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "phone",
                "operator": "EQ", 
                "value": phone
            }]
        }]
    }
    
    try:
        results = client.crm.contacts.search_api.do_search(search_request)
        
        if results.total > 0:
            # Actualizar existente
            contact_id = results.results[0].id
            return client.crm.contacts.basic_api.update(
                contact_id=contact_id,
                simple_public_object_input={"properties": properties}
            )
        else:
            # Crear nuevo
            properties["phone"] = phone
            return client.crm.contacts.basic_api.create(
                simple_public_object_input={"properties": properties}
            )
    except ApiException as e:
        return {"error": str(e)}

@hubspot_server.tool("update_deal_stage")
async def update_deal_stage(deal_id: str, stage: str):
    """Actualiza etapa del deal en pipeline"""
    # Implementación...
    pass

@hubspot_server.tool("log_activity")
async def log_activity(contact_id: str, activity_type: str, content: str):
    """Registra actividad (llamada, email, nota) en el contacto"""
    # Implementación...
    pass
```

---

## 9. Observabilidad y AgentOps

### 9.1 Stack de Monitoreo

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY STACK                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   LangSmith     │  │   Arize         │                  │
│  │   (Tracing)     │  │   Phoenix       │                  │
│  └────────┬────────┘  └────────┬────────┘                  │
│           │                    │                            │
│           ▼                    ▼                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Metrics Dashboard (Grafana)             │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │   │
│  │  │Response │ │Conversion│ │ Error   │ │ Cost    │   │   │
│  │  │  Time   │ │  Rate   │ │  Rate   │ │per Lead │   │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Alerting (PagerDuty/Slack)              │   │
│  │  • Error rate > 5%                                   │   │
│  │  • Response time > 30s                               │   │
│  │  • Conversion rate drop > 20%                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Métricas Clave (KPIs)

| Categoría | Métrica | Target | Alerta |
|-----------|---------|--------|--------|
| **Performance** | Tiempo de respuesta | < 30s | > 60s |
| **Performance** | Latencia LLM | < 2s | > 5s |
| **Conversion** | Tasa de respuesta | > 80% | < 60% |
| **Conversion** | Tasa de agendamiento | > 15% | < 8% |
| **Quality** | Extracción de datos | > 95% | < 85% |
| **Quality** | Clasificación FSM | > 98% | < 90% |
| **Cost** | Costo por lead | < $0.50 USD | > $1.00 |
| **Reliability** | Uptime | 99.9% | < 99% |
| **Reliability** | Error rate | < 1% | > 5% |

### 9.3 Estructura de Logs

```python
import structlog

logger = structlog.get_logger()

# Log de mensaje entrante
logger.info(
    "message_received",
    phone_number=phone,
    message_length=len(message),
    session_id=session_id,
    current_state=fsm_state
)

# Log de transición FSM
logger.info(
    "fsm_transition",
    session_id=session_id,
    from_state=old_state,
    to_state=new_state,
    trigger=trigger_event,
    lead_score=bant_score
)

# Log de extracción de datos
logger.info(
    "data_extracted",
    session_id=session_id,
    fields_extracted=list(extracted_data.keys()),
    extraction_confidence=confidence,
    model_used=model_name
)

# Log de agendamiento
logger.info(
    "meeting_scheduled",
    session_id=session_id,
    lead_id=lead_id,
    meeting_time=meeting_time,
    meeting_link=meeting_link,
    total_messages=message_count,
    time_to_schedule=time_delta
)
```

---

## 10. Plan de Implementación (Startup Lean)

> [!IMPORTANT]
> Timeline de **6-8 semanas** para sistema completo.
> Todos los agentes usan DeepSeek-V3 para mantener costos bajos.

### Fase 1: Infraestructura y FSM (Semanas 1-2)

| Semana | Entregables |
|--------|-------------|
| **S1** | - Setup Vercel + Supabase (free tiers) |
|        | - WhatsApp Business API configurado |
|        | - Webhook recibiendo mensajes |
|        | - Conexión DeepSeek API funcionando |
|        | - Esquema de base de datos (leads, mensajes, estados) |
| **S2** | - LangGraph configurado con checkpointing |
|        | - FSM completa (9 estados) implementada |
|        | - Lógica de transiciones deterministas |
|        | - Persistencia de estado en Supabase |

### Fase 2: Sistema Multi-Agente (Semanas 3-4)

| Semana | Entregables |
|--------|-------------|
| **S3** | - Agente Router (clasificador de intención) |
|        | - Agente Extractor (NER para datos del lead) |
|        | - Agente Conversacional (generador de respuestas) |
|        | - Orquestación entre agentes con LangGraph |
| **S4** | - Agente Calificador BANT |
|        | - Agente Scheduler (lógica de agendamiento) |
|        | - Integración Google Calendar API |
|        | - Flujo completo de agendamiento |

### Fase 3: Seguridad y Memoria (Semanas 5-6)

| Semana | Entregables |
|--------|-------------|
| **S5** | - Guardrails en código Python (sin NeMo) |
|        | - Detección PII colombiana |
|        | - Topic rails para límites conversacionales |
|        | - Sistema de memoria en Supabase (reemplaza Zep) |
| **S6** | - Manejo de objeciones con respuestas predefinidas |
|        | - Optimización de prompts por industria |
|        | - Tests end-to-end del flujo completo |
|        | - Logs estructurados para debugging |

### Fase 4: Lanzamiento y Validación (Semanas 7-8)

| Semana | Entregables |
|--------|-------------|
| **S7** | - Pruebas con 10-20 leads reales |
|        | - Ajustes basados en feedback |
|        | - Monitoreo manual de conversaciones |
|        | - Documentación de uso |
| **S8** | - Lanzamiento soft |
|        | - Iteración basada en datos reales |
|        | - Handoff y capacitación |

> [!NOTE]
> **Mejoras futuras** (cuando haya tracción): GraphRAG con Neo4j, memoria Zep, NeMo Guardrails, HubSpot CRM.

---

## 11. Stack Tecnológico Recomendado

### Backend
| Componente | Tecnología | Justificación | Costo |
|------------|------------|---------------|-------|
| Runtime | Python 3.12 | Ecosystem LangChain/LangGraph | $0 |
| Framework | FastAPI | Async, performance, typing | $0 |
| Orquestación | LangGraph | Grafos cíclicos, checkpointing | $0 |
| **LLM Único** | **DeepSeek-V3** | **95% más barato que GPT-4** | **~$0.001/1K tokens** |

### Datos (Tier Gratuito)
| Componente | Tecnología | Justificación | Costo |
|------------|------------|---------------|-------|
| DB Principal | **Supabase Free** | PostgreSQL gratis hasta 500MB | $0 |
| Cache/Estado | **Upstash Redis Free** | 10K comandos/día gratis | $0 |
| Memoria | **JSON en Supabase** | Reemplaza Zep ($49/mes) | $0 |

> [!NOTE]
> GraphRAG y Neo4j son **opcionales para MVP**. Usar búsqueda semántica simple primero.

### Infraestructura (Free Tiers)
| Componente | Tecnología | Justificación | Costo |
|------------|------------|---------------|-------|
| Hosting | **Vercel Free** | Hobby tier suficiente para MVP | $0 |
| WhatsApp | Meta Cloud API | 1,000 conversaciones/mes gratis | $0 |
| Calendar | Google Calendar API | Backend-sync (Gestión vía Dashboard propio) | $0 |
| CRM | **Admin Dashboard (Propio)** | Next.js + Tailwind (Gestión centralizada) | $0 |
| Monitoring | **Console logs + Vercel** | Suficiente para inicio | $0 |

### Seguridad (Costo Cero)
| Componente | Tecnología | Justificación | Costo |
|------------|------------|---------------|-------|
| Guardrails | Código custom (Python) | Sin NeMo, sin costo | $0 |
| Secrets | Variables de entorno Vercel | Simple y seguro | $0 |
| Auth | Variables de entorno | Sin OAuth complejo para MVP | $0 |

---

## 12. Estimación de Costos (Startup Mode)

### Comparativa: GPT-4 vs DeepSeek-V3

| Modelo | Input (1M tokens) | Output (1M tokens) | Ahorro vs GPT-4 |
|--------|-------------------|--------------------|-----------------|
| GPT-4o | $2.50 | $10.00 | - |
| GPT-4o-mini | $0.15 | $0.60 | 85% |
| **DeepSeek-V3** | **$0.27** | **$1.10** | **~90%** |
| DeepSeek-V3 (cache) | $0.07 | $1.10 | **~97%** |

> [!IMPORTANT]
> DeepSeek-V3 ofrece rendimiento comparable a GPT-4 a una fracción del costo.
> Ideal para startups con presupuesto limitado.

### Costos Mensuales MVP (50 leads/mes)

| Concepto | Costo |
|----------|-------|
| **DeepSeek API** | |
| ~5 llamadas/lead x 50 leads x ~2K tokens | ~$2-5 USD |
| **Infraestructura** | |
| Vercel Free Tier | $0 |
| Supabase Free Tier | $0 |
| Upstash Redis Free | $0 |
| **Servicios** | |
| WhatsApp Business (1K conv gratis) | $0 |
| Google Calendar API | $0 |
| Notion/Sheets como CRM | $0 |
| **Dominio** | ~$12/año = $1/mes |
| **TOTAL MVP** | **~$5-10 USD/mes** |

### Costos Escalados (500 leads/mes)

| Concepto | Costo |
|----------|-------|
| DeepSeek API (más volumen) | ~$20-40 USD |
| Vercel Pro (si necesario) | $20 USD |
| Supabase Pro (si necesario) | $25 USD |
| **TOTAL ESCALADO** | **~$65-85 USD/mes** |

### Costo por Lead Cualificado
- MVP: ~$0.10-0.20 USD por lead
- Escalado: ~$0.15-0.20 USD por lead
- **Comparado con GPT-4: ~$3-4 USD por lead (95% ahorro)**

---

## 13. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Rate limiting WhatsApp | Media | Alto | Throttling, queue management |
| Alucinaciones LLM | Media | Alto | Guardrails, validación, few-shot |
| Latencia alta | Media | Medio | Streaming, cache, modelos small |
| Costo API excesivo | Baja | Medio | Monitoreo, alertas, modelos mixtos |
| Bans WhatsApp | Baja | Crítico | Compliance estricto, templates |
| Fallas calendario | Baja | Medio | Retry logic, fallback manual |

---

## 14. Criterios de Aceptación

### MVP (Semana 6)
- [ ] Conversación fluida en WhatsApp
- [ ] Extracción de 5/6 campos de datos (nombre, empresa, ciudad, dolor, presupuesto, urgencia)
- [ ] FSM con 9 estados funcionando
- [ ] 5 agentes especializados operativos (Router, Extractor, Qualifier, Conversacional, Scheduler)
- [ ] Agendamiento de citas con Google Calendar
- [ ] Guardrails básicos en Python

### Producción (Semana 8)
- [ ] Manejo de 10-50 leads simultáneos
- [ ] Tiempo de respuesta < 60s en P95
- [ ] Tasa de agendamiento > 10%
- [ ] Extracción de datos > 85%
- [ ] Logs estructurados para debugging
- [ ] Documentación de despliegue
- [ ] Handoff al equipo de Mi IA Colombia

---

## 15. Equipo Requerido (Startup Mode)

| Rol | Dedicación | Responsabilidades |
|-----|------------|-------------------|
| **Desarrollador Full-Stack** | 100% | Todo: Backend, LangGraph, integraciones, prompts |
| Fundador/PO (interno) | 20% | Requerimientos, pruebas, feedback |

> [!TIP]
> Para una startup, un solo desarrollador con experiencia en Python/LangChain puede construir el MVP completo en 4-6 semanas.

---

## 16. Apéndices

### A. Ejemplos de Conversación

#### Flujo Exitoso
```
[LEAD]: Hola, quiero información sobre sus servicios

[AGENTE]: ¡Hola! 👋 Soy el asistente de Mi IA Colombia.

Ayudamos a empresas a crecer con sistemas de inteligencia 
artificial: apps web de alto rendimiento y agentes de ventas 
que trabajan 24/7.

¿Qué tipo de solución estás buscando para tu empresa?

[LEAD]: Necesito automatizar la atención de clientes en mi 
restaurante, perdemos muchas reservas

[AGENTE]: ¡Entendido! El problema de perder reservas por 
respuesta lenta es muy común y tiene solución. 🎯

Nuestros agentes de IA pueden atender WhatsApp 24/7, tomar 
reservas automáticamente y reducir ese goteo de clientes.

Para entender mejor tu caso: ¿cuántas mesas manejas 
aproximadamente y en qué ciudad está tu restaurante?

[LEAD]: Tengo 25 mesas y estamos en Bogotá, soy Carlos de 
Sabor Latino

[AGENTE]: Perfecto Carlos, 25 mesas es un buen volumen para 
automatizar. 📊

Para Sabor Latino en Bogotá podríamos implementar un sistema 
que maneje reservas, confirmaciones automáticas y hasta 
recomendaciones de menú.

¿Tienes un presupuesto aproximado en mente para este proyecto?
¿Es algo que necesitan implementar pronto?

[LEAD]: Tenemos unos 15 millones y lo necesitamos antes de 
las temporadas altas, digamos en 2 meses

[AGENTE]: ¡Excelente timing Carlos! 🚀 Con 15M y 8 semanas 
podemos entregarte un sistema completo funcionando.

Me encantaría que hables directamente con nuestro equipo 
para diseñar la solución perfecta para Sabor Latino.

Tenemos disponibilidad esta semana para una llamada de 15 minutos:
📅 Martes 24 - 10:00 AM
📅 Miércoles 25 - 3:00 PM
📅 Jueves 26 - 11:00 AM

¿Cuál te funciona mejor?

[LEAD]: El miércoles a las 3 me sirve

[AGENTE]: ✅ ¡Confirmado Carlos!

📅 Miércoles 25 de diciembre
🕐 3:00 PM (Hora Colombia)
📍 Te envío el link por aquí antes de la llamada

Hablarás con Juan, nuestro especialista en soluciones 
para restaurantes. ¡Hasta el miércoles! 🎯
```

### B. Schema de Base de Datos

```sql
-- Tabla principal de leads
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100),
    empresa VARCHAR(200),
    cargo VARCHAR(100),
    ciudad VARCHAR(100),
    email VARCHAR(200),
    puntos_dolor JSONB DEFAULT '[]',
    presupuesto_min BIGINT,
    presupuesto_max BIGINT,
    urgencia VARCHAR(20),
    bant_score INTEGER DEFAULT 0,
    fsm_state VARCHAR(50) DEFAULT 'INICIO',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_message_at TIMESTAMPTZ,
    message_count INTEGER DEFAULT 0,
    source VARCHAR(50) DEFAULT 'whatsapp'
);

-- Tabla de mensajes
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    direction VARCHAR(10) NOT NULL, -- 'inbound' | 'outbound'
    content TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text',
    whatsapp_id VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Tabla de citas
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    calendar_event_id VARCHAR(200),
    meeting_link VARCHAR(500),
    scheduled_at TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER DEFAULT 15,
    status VARCHAR(20) DEFAULT 'scheduled',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    reminder_sent BOOLEAN DEFAULT FALSE
);

-- Tabla de estados FSM (para auditoría)
CREATE TABLE fsm_transitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    from_state VARCHAR(50),
    to_state VARCHAR(50) NOT NULL,
    trigger_event VARCHAR(100),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_leads_phone ON leads(phone_number);
CREATE INDEX idx_leads_state ON leads(fsm_state);
CREATE INDEX idx_messages_lead ON messages(lead_id, created_at DESC);
CREATE INDEX idx_appointments_scheduled ON appointments(scheduled_at);
```

---

**Documento preparado para:** Mi IA Colombia  
**Fecha:** 22 de Diciembre de 2025  
**Versión:** 1.0 - PRD Inicial
