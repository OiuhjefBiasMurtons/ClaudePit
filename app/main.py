from fastapi import FastAPI
from pydantic import BaseModel

from app.database import get_or_create_client, get_menu
from app.utils import format_menu_for_ai
from app.ai_service import build_system_prompt, call_openai
from app.tools import get_active_order
from app.memory import add_message, get_conversation_history, clear_old_conversations

app = FastAPI(title="Pizzeria WhatsApp Bot")


class MessageRequest(BaseModel):
    telefono: str
    nombre_cliente: str
    mensaje: str


@app.post("/process-message")
async def process_message(request: MessageRequest):
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

    return {"respuesta": respuesta}
