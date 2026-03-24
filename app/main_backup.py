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
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from app.database import get_or_create_client, get_menu, get_barrios
from app.utils import format_menu_for_ai, format_barrios_for_ai
from app.ai_service import build_system_prompt, call_openai
from app.tools import get_active_order
from app.memory import add_message, get_conversation_history, clear_old_conversations, update_conversation_history

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
        
        # Limpiar conversaciones viejas (>2 horas)
        clear_old_conversations(max_age_minutes=120)

        # Obtener cliente, menú y barrios
        cliente = get_or_create_client(request.telefono, request.nombre_cliente)
        menu_items = get_menu()
        barrios = get_barrios()

        # Obtener pedido activo si existe
        pedido_activo = get_active_order(cliente["id"])

        # Formatear menú y barrios para IA
        menu_formateado = format_menu_for_ai(menu_items)
        barrios_formateados = format_barrios_for_ai(barrios)

        # Obtener historial de conversación
        conversation_history = get_conversation_history(request.telefono)

        # Construir descripción del pedido activo
        pedido_info = ""
        if pedido_activo and pedido_activo.get("items"):
            items_desc = []
            total = pedido_activo.get("total_order", 0)
            precio_dom = pedido_activo.get("precio_domicilio", 0)
            for item in pedido_activo["items"]:
                nombre = item.get('product_name')
                sabores_extra = item.get('sabores_extra')
                if sabores_extra:
                    nombre += "/" + "/".join(sabores_extra)
                items_desc.append(f"{item.get('quantity')}x {nombre} {item.get('variant_name')}")
            pedido_info = f"Items: {', '.join(items_desc)} | Subtotal: ${total:,.0f} | Domicilio: ${precio_dom:,.0f} | Total: ${total + precio_dom:,.0f} | Dirección: {pedido_activo.get('address_delivery', 'sin definir')}"

        # Construir prompt y llamar a OpenAI
        system_prompt = build_system_prompt(
            nombre_cliente=cliente.get("name", "Cliente"),
            direccion_guardada=cliente.get("address"),
            order_id=pedido_activo.get("id", "N/A") if pedido_activo else "N/A",
            estado_pedido=pedido_activo.get("state", "N/A") if pedido_activo else "N/A",
            menu_formateado=menu_formateado,
            pedido_info=pedido_info,
            barrios_formateados=barrios_formateados
        )
        respuesta, new_history = call_openai(
            request.mensaje,
            system_prompt,
            client_id=cliente["id"],
            conversation_history=conversation_history
        )

        # Actualizar el historial completo
        update_conversation_history(request.telefono, new_history)
        
        logger.info(f"Respuesta enviada a {request.telefono}")

        return {"respuesta": respuesta}
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error procesando mensaje: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")