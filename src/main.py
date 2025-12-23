"""
Entry point de la aplicación FastAPI.
Expone webhook de WhatsApp y endpoints de salud.
"""
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse
import json
import structlog

try:
    from src.config import settings
    from src.fsm import process_message
    from src.integrations import whatsapp_client
    from src.guardrails import guardrails, pii_detector
except ImportError:
    # Fallback for local dev/relative context
    from .config import settings
    from .fsm import process_message
    from .integrations import whatsapp_client
    from .guardrails import guardrails, pii_detector

# Configurar logging estructurado
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Crear app FastAPI
app = FastAPI(
    title="Mi IA Colombia - SDR WhatsApp",
    description="Sistema de IA SDR autónomo para WhatsApp",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Mi IA Colombia - SDR WhatsApp",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check detallado."""
    return {
        "status": "healthy",
        "deepseek_configured": bool(settings.deepseek_api_key),
        "supabase_configured": bool(settings.supabase_url),
        "whatsapp_configured": bool(settings.whatsapp_token),
    }


# =====================
# WEBHOOK WHATSAPP
# =====================

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """
    Verificación del webhook de WhatsApp.
    Meta envía un GET para verificar que el webhook es válido.
    """
    logger.info("webhook_verification_attempt", mode=hub_mode, token=hub_verify_token)
    
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        logger.info("webhook_verified")
        return PlainTextResponse(content=hub_challenge)
    
    logger.warning("webhook_verification_failed", expected=settings.whatsapp_verify_token)
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Recibe mensajes de WhatsApp.
    Procesa el mensaje y responde automáticamente.
    """
    try:
        body = await request.json()
        
        logger.info("webhook_received", body_keys=list(body.keys()))
        
        # Extraer mensaje
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        
        # Verificar que es un mensaje de texto
        messages = value.get("messages", [])
        if not messages:
            return {"status": "no_messages"}
        
        message = messages[0]
        
        # Solo procesar mensajes de texto
        if message.get("type") != "text":
            logger.info("non_text_message", type=message.get("type"))
            return {"status": "non_text_ignored"}
        
        phone_number = message.get("from")
        text = message.get("text", {}).get("body", "")
        message_id = message.get("id")
        
        if not phone_number or not text:
            return {"status": "invalid_message"}
        
        logger.info(
            "message_received",
            phone=phone_number[-4:],  # Solo últimos 4 dígitos por privacidad
            text_length=len(text),
            message_id=message_id
        )
        
        # Verificar guardrails de input
        is_valid, reason = guardrails.check_input(text)
        if not is_valid:
            logger.warning("input_blocked", reason=reason, phone=phone_number[-4:])
            response = guardrails.get_deflection(reason.split(":")[1] if ":" in reason else "default")
        else:
            # Procesar mensaje con el grafo de agentes
            response = await process_message(phone_number, text)
            
            # Verificar y sanitizar output
            response = guardrails.sanitize_output(response)
        
        # Marcar mensaje como leído
        await whatsapp_client.mark_as_read(message_id)
        
        # Enviar respuesta
        send_result = await whatsapp_client.send_text_message(phone_number, response)
        
        logger.info(
            "response_sent",
            phone=phone_number[-4:],
            response_length=len(response),
            send_result=send_result.get("messages", [{}])[0].get("id") if "messages" in send_result else None
        )
        
        return {"status": "processed"}
        
    except Exception as e:
        logger.error("webhook_error", error=str(e))
        # No lanzar excepción para que WhatsApp no reintente
        return {"status": "error", "message": str(e)}


# =====================
# ENDPOINTS DE DEBUG (solo desarrollo)
# =====================

@app.post("/test/message")
async def test_message(phone_number: str, message: str):
    """
    Endpoint de prueba para simular mensajes.
    Solo para desarrollo/testing.
    """
    logger.info("test_message", phone=phone_number, message=message)
    
    response = await process_message(phone_number, message)
    
    return {
        "input": message,
        "response": response
    }


# =====================
# INIT
# =====================

@app.on_event("startup")
async def startup():
    """Inicialización al arrancar."""
    logger.info(
        "app_startup",
        deepseek_configured=bool(settings.deepseek_api_key),
        supabase_configured=bool(settings.supabase_url),
        whatsapp_configured=bool(settings.whatsapp_token)
    )


@app.on_event("shutdown")
async def shutdown():
    """Limpieza al cerrar."""
    logger.info("app_shutdown")
