from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv
import logging
import httpx
import os

load_dotenv()

from app.database import get_or_create_client, get_menu, get_barrios, update_client_barrio
from app.utils import format_menu_for_ai, format_barrios_for_ai
from app.ai_service import build_system_prompt, build_menu_context, call_openai
from app.tools import get_active_order
from app.memory import add_message, get_conversation_history, clear_old_conversations, update_conversation_history

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Pizzeria WhatsApp Bot")

# ── Configuración WhatsApp ─────────────────────────────────────────────────────
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID")   # ej: 989708707553821
WA_ACCESS_TOKEN    = os.getenv("WA_ACCESS_TOKEN")       # Bearer token de Meta


class MessageRequest(BaseModel):
    telefono: str
    nombre_cliente: str
    mensaje: str


# ── Helper: enviar mensaje a WhatsApp directamente desde Python ────────────────
async def send_whatsapp_message(telefono: str, texto: str):
    """Llama a la Graph API de Meta para enviar el mensaje al cliente."""
    url = f"https://graph.facebook.com/v24.0/{WA_PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": telefono,
        "type": "text",
        "text": {"body": texto}
    }
    headers = {
        "Authorization": f"Bearer {WA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            logger.error(f"Error enviando WA a {telefono}: {resp.status_code} {resp.text}")
        else:
            logger.info(f"Mensaje enviado a {telefono}")


# ── Lógica principal (ahora en background) ────────────────────────────────────
async def process_and_reply(telefono: str, nombre_cliente: str, mensaje: str):
    """
    Toda la lógica pesada ocurre aquí, en background.
    FastAPI ya respondió 200 OK a N8n antes de entrar aquí.
    """
    try:
        clear_old_conversations(max_age_minutes=120)

        cliente           = get_or_create_client(telefono, nombre_cliente)
        menu_items        = get_menu()
        barrios           = get_barrios()
        pedido_activo     = get_active_order(cliente["id"])
        menu_formateado   = format_menu_for_ai(menu_items)
        barrios_formateados = format_barrios_for_ai(barrios)

        conversation_history = get_conversation_history(telefono)

        pedido_info = ""
        if pedido_activo and pedido_activo.get("items"):
            items_desc = []
            total      = pedido_activo.get("total_order", 0)
            precio_dom = pedido_activo.get("precio_domicilio", 0)
            for item in pedido_activo["items"]:
                nombre = item.get('product_name')
                sabores_extra = item.get('sabores_extra')
                if sabores_extra:
                    nombre += "/" + "/".join(sabores_extra)
                items_desc.append(
                    f"{item.get('quantity')}x {nombre} {item.get('variant_name')}"
                )
            pedido_info = (
                f"Items: {', '.join(items_desc)} | "
                f"Subtotal: ${total:,.0f} | "
                f"Domicilio: ${precio_dom:,.0f} | "
                f"Total: ${total + precio_dom:,.0f} | "
                f"Dirección: {pedido_activo.get('address_delivery', 'sin definir')}"
            )

        system_prompt = build_system_prompt(
            nombre_cliente=cliente.get("name", "Cliente"),
            direccion_guardada=cliente.get("address"),
            order_id=pedido_activo.get("id", "N/A") if pedido_activo else "N/A",
            estado_pedido=pedido_activo.get("state", "N/A") if pedido_activo else "N/A",
            pedido_info=pedido_info,
            barrio_session=cliente.get("barrio") or "",
        )

        menu_ctx = build_menu_context(menu_formateado, barrios_formateados)

        respuesta, new_history, session_data = call_openai(
            mensaje,
            system_prompt,
            client_id=cliente["id"],
            conversation_history=conversation_history,
            menu_context=menu_ctx,
            telefono=telefono,
        )

        if session_data.get("barrio"):
            update_client_barrio(telefono, session_data["barrio"])

        update_conversation_history(telefono, new_history)

        # ── Enviar respuesta directo a WhatsApp ──
        await send_whatsapp_message(telefono, respuesta)

    except Exception as e:
        logger.error(f"Error en process_and_reply para {telefono}: {e}", exc_info=True)
        # Notificar al cliente que algo salió mal
        await send_whatsapp_message(
            telefono,
            "Lo siento, tuve un problema procesando tu mensaje. Por favor intenta de nuevo 🙏"
        )


# ── Endpoints ──────────────────────────────────────────────────────────────────
@app.get("/")
async def health_check():
    return {"status": "ok", "service": "Pizzeria WhatsApp Bot", "version": "2.0.0"}


@app.post("/process-message")
async def process_message(request: MessageRequest, background_tasks: BackgroundTasks):
    """
    Responde 200 OK a N8n INMEDIATAMENTE.
    El procesamiento real ocurre en background sin bloquear.
    """
    if not request.telefono or not request.nombre_cliente or not request.mensaje:
        # Incluso los errores de validación los manejamos rápido
        logger.warning("Request con campos vacíos ignorado")
        return {"status": "ignored"}

    background_tasks.add_task(
        process_and_reply,
        request.telefono,
        request.nombre_cliente,
        request.mensaje
    )

    # N8n recibe esto en <50ms y queda libre para el siguiente mensaje
    return {"status": "queued"}