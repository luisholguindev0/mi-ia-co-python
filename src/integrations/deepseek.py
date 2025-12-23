"""
Cliente para DeepSeek API.
Proporciona interfaz unificada para llamadas al LLM.
"""
import httpx
from typing import List, Optional
import json

from ..config import settings


class DeepSeekClient:
    """Cliente para DeepSeek API (compatible con OpenAI)."""
    
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.base_url = settings.deepseek_base_url
        self.model = settings.deepseek_model
    
    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def chat_completion(
        self,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 1024,
        response_format: Optional[dict] = None
    ) -> str:
        """Genera una respuesta de chat."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if response_format:
            payload["response_format"] = response_format
        
        if not self.api_key:
            print(f"⚠️ DeepSeek no configurado. Mock response.")
            return '{"mock": true}'
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60.0
            )
            
            if response.status_code != 200:
                print(f"❌ Error DeepSeek API: {response.status_code} - {response.text}")
                return f"Error: {response.text}"
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    async def chat_json(
        self,
        messages: List[dict],
        temperature: float = 0.3
    ) -> dict:
        """Genera una respuesta en formato JSON."""
        response = await self.chat_completion(
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Intentar extraer JSON del texto
            if "{" in response and "}" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                try:
                    return json.loads(response[start:end])
                except:
                    pass
            return {"error": "Failed to parse JSON", "raw": response}


# Instancia global
deepseek_client = DeepSeekClient()
