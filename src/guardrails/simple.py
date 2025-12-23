"""
Guardrails simples en Python.
Valida inputs y outputs sin dependencias costosas.
"""
import re
from typing import Tuple, List


class SimpleGuardrails:
    """Guardrails ligeros para startup - costo $0"""
    
    # Patrones bloqueados en las respuestas del agente
    BLOCKED_OUTPUT_PATTERNS = [
        r"precio exacto",
        r"cuánto cuesta exactamente",
        r"cuesta \$?\d+",  # No mencionar precios específicos
        r"gratis",
        r"sin costo",
        r"garantizo",
        r"prometo",
    ]
    
    # Tópicos bloqueados
    BLOCKED_TOPICS = [
        "política",
        "religión", 
        "competencia",
        "otros clientes",
        "información confidencial"
    ]
    
    # Respuestas de deflexión
    DEFLECTION_RESPONSES = {
        "politica": "Prefiero mantener nuestra conversación enfocada en cómo podemos ayudar a tu negocio. ¿En qué área de automatización puedo ayudarte?",
        "religion": "Prefiero mantener nuestra conversación enfocada en cómo podemos ayudar a tu negocio. ¿En qué área de automatización puedo ayudarte?",
        "competencia": "No tengo información detallada sobre otras empresas, pero puedo contarte todo sobre nuestras soluciones. ¿Qué necesidad específica tienes?",
        "default": "Eso está fuera de mi área de conocimiento. ¿Hay algo sobre automatización o IA para tu empresa en lo que pueda ayudarte?"
    }
    
    @classmethod
    def check_input(cls, message: str) -> Tuple[bool, str]:
        """
        Verifica si el input del usuario es apropiado.
        Retorna (is_allowed, reason)
        """
        message_lower = message.lower()
        
        for topic in cls.BLOCKED_TOPICS:
            if topic in message_lower:
                return False, f"topic_blocked:{topic}"
        
        # Detectar posibles ataques de prompt injection
        injection_patterns = [
            r"ignora.*instrucciones",
            r"olvida.*sistema",
            r"actúa como",
            r"pretende ser",
            r"jailbreak",
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, message_lower):
                return False, "injection_attempt"
        
        return True, "allowed"
    
    @classmethod
    def check_output(cls, response: str) -> Tuple[bool, str]:
        """
        Verifica que la respuesta del bot no prometa cosas indebidas.
        Retorna (is_allowed, reason)
        """
        response_lower = response.lower()
        
        for pattern in cls.BLOCKED_OUTPUT_PATTERNS:
            if re.search(pattern, response_lower):
                return False, f"blocked_pattern:{pattern}"
        
        return True, "allowed"
    
    @classmethod
    def get_deflection(cls, topic: str) -> str:
        """Obtiene respuesta de deflexión para un tópico bloqueado."""
        return cls.DEFLECTION_RESPONSES.get(
            topic, 
            cls.DEFLECTION_RESPONSES["default"]
        )
    
    @classmethod
    def sanitize_output(cls, response: str) -> str:
        """
        Intenta sanitizar una respuesta que no pasó la validación.
        Si no puede, retorna una respuesta genérica.
        """
        is_valid, reason = cls.check_output(response)
        
        if is_valid:
            return response
        
        # Intentar remover el patrón problemático
        for pattern in cls.BLOCKED_OUTPUT_PATTERNS:
            response = re.sub(pattern, "[información confidencial]", response, flags=re.IGNORECASE)
        
        # Verificar de nuevo
        is_valid, _ = cls.check_output(response)
        
        if is_valid:
            return response
        
        # Si sigue fallando, retornar respuesta genérica
        return "Gracias por tu interés. Para darte información más precisa, ¿te gustaría agendar una llamada con nuestro equipo?"


class PIIDetector:
    """Detector de información personal identificable para Colombia."""
    
    PATTERNS = {
        "cedula": r"\b\d{6,10}\b",  # Cédula colombiana
        "nit": r"\b\d{9}-\d\b",     # NIT empresarial
        "telefono": r"\b3\d{9}\b",  # Celular colombiano
        "tarjeta": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        "email": r"\b[\w.-]+@[\w.-]+\.\w+\b"
    }
    
    @classmethod
    def detect(cls, text: str) -> dict:
        """
        Detecta PII en el texto.
        Retorna dict con tipo de PII y matches encontrados.
        """
        detected = {}
        
        for pii_type, pattern in cls.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                detected[pii_type] = matches
        
        return detected
    
    @classmethod
    def mask(cls, text: str) -> str:
        """
        Enmascara PII en el texto para logging seguro.
        """
        masked = text
        
        for pii_type, pattern in cls.PATTERNS.items():
            masked = re.sub(
                pattern,
                f"[{pii_type.upper()}_REDACTED]",
                masked
            )
        
        return masked


# Instancias globales
guardrails = SimpleGuardrails()
pii_detector = PIIDetector()
