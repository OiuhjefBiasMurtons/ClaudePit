from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from app.database import get_or_create_client, get_menu
from app.utils import format_menu_for_ai
from app.ai_service import build_system_prompt, call_openai
from app.tools import get_active_order
from app.memory import add_message, get_conversation_history, clear_old_conversations

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Pizzeria WhatsApp Bot")


class MessageRequest(BaseModel):
    telefono: str
    nombre_cliente: str
    mensaje: str
    
    class Config:
        # Validar que los strings no estén vacíos
        str_min_length = 1
        
    def __init__(self, **data):
        super().__init__(**data)
        # Validación adicional
        if not self.telefono or not self.telefono.strip():
            raise ValueError("El campo 'telefono' es requerido y no puede estar vacío")
        if not self.nombre_cliente or not self.nombre_cliente.strip():
            raise ValueError("El campo 'nombre_cliente' es requerido y no puede estar vacío")
        if not self.mensaje or not self.mensaje.strip():
            raise ValueError("El campo 'mensaje' es requerido y no puede estar vacío")


@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Pizzeria WhatsApp Bot",
        "version": "1.0.0"
    }


@app.post("/process-message")
async def process_message(request: MessageRequest):
    try:
        logger.info(f"Procesando mensaje de {request.telefono}: {request.mensaje[:50]}...")
        
        # Limpiar conversaciones viejas (>30 min)
        clear_old_conversations()

        # Obtener cliente y menú
        cliente = get_or_create_client(request.telefono, request.nombre_cliente)
        menu_items = get_menu()

        # Obtener pedido activo si existe
        pedido_activo = get_active_order(cliente["id"])

        # Formatear menú para IA
        menu_formateado = format_menu_for_ai(menu_items)

        # Obtener historial de conversación
        conversation_history = get_conversation_history(request.telefono)

        # Guardar mensaje del usuario
        add_message(request.telefono, "user", request.mensaje)

        # Construir prompt y llamar a OpenAI
        system_prompt = build_system_prompt(cliente, menu_formateado, pedido_activo)
        respuesta = call_openai(
            request.mensaje,
            system_prompt,
            client_id=cliente["id"],
            conversation_history=conversation_history
        )

        # Guardar respuesta del asistente
        add_message(request.telefono, "assistant", respuesta)
        
        logger.info(f"Respuesta enviada a {request.telefono}")

        return {"respuesta": respuesta}
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error procesando mensaje: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
