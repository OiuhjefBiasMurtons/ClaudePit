import asyncio
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
from app.tools import get_active_orders
from app.memory import add_message, get_conversation_history, clear_old_conversations, update_conversation_history

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Pizzeria WhatsApp Bot")

# ── Configuración WhatsApp ─────────────────────────────────────────────────────
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID")   # ej: 989708707553821
WA_ACCESS_TOKEN    = os.getenv("WA_ACCESS_TOKEN")       # Bearer token de Meta

# ── Lock por teléfono para evitar la ventana de historial desactualizado ──────
_phone_locks: dict[str, asyncio.Lock] = {}

def _get_phone_lock(telefono: str) -> asyncio.Lock:
    if telefono not in _phone_locks:
        _phone_locks[telefono] = asyncio.Lock()
    return _phone_locks[telefono]


# ── Debounce: acumular mensajes rápidos del mismo usuario ─────────────────────
# Estructura: {telefono: [(token_único, mensaje), ...]}
_pending_messages: dict[str, list] = {}

# ── Respuestas automáticas para mensajes no-texto ─────────────────────────────
MENSAJES_NO_TEXTO = {
    "[AUDIO]":    "Solo proceso texto por el momento 🎙️ ¿Me escribes tu pedido?",
    "[IMAGE]":    "No puedo ver imágenes, pero con gusto te ayudo 😊 ¿Qué deseas pedir?",
    "[VIDEO]":    "No proceso videos, pero cuéntame ¿qué deseas pedir? 🍕",
    "[STICKER]":  "Como soy un bot no entiendo stickers 😅 ¿En qué te puedo ayudar?",
    "[DOCUMENT]": "No proceso documentos. ¿En qué te puedo ayudar?",
}


class MessageRequest(BaseModel):
    telefono: str
    nombre_cliente: str
    mensaje: str


# ── Helper: enviar mensaje a WhatsApp con retry ────────────────────────────────
async def send_whatsapp_message(telefono: str, texto: str):
    """Llama a la Graph API de Meta con hasta 3 intentos y backoff exponencial."""
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
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    logger.info(f"Mensaje enviado a {telefono}")
                    return
                elif resp.status_code >= 500:
                    logger.warning(f"Meta API error {resp.status_code} (intento {attempt}/{max_attempts})")
                    if attempt < max_attempts:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    logger.error(f"Error enviando WA a {telefono}: {resp.status_code} {resp.text}")
                else:
                    # 4xx — no reintentable
                    logger.error(f"Error enviando WA a {telefono}: {resp.status_code} {resp.text}")
                    return
        except httpx.TimeoutException:
            logger.warning(f"Timeout enviando WA a {telefono} (intento {attempt}/{max_attempts})")
            if attempt < max_attempts:
                await asyncio.sleep(2 ** attempt)
            else:
                logger.error(f"Timeout definitivo enviando WA a {telefono} tras {max_attempts} intentos")
        except Exception as e:
            logger.error(f"Error inesperado enviando WA a {telefono}: {e}")
            return


# ── Lógica principal (ahora en background) ────────────────────────────────────
async def process_and_reply(telefono: str, nombre_cliente: str, mensaje: str):
    """
    Toda la lógica pesada ocurre aquí, en background.
    FastAPI ya respondió 200 OK a N8n antes de entrar aquí.

    Orden de guardas:
      1. Mensaje vacío → silencio
      2. Mensaje no-texto ([AUDIO], [IMAGE]…) → respuesta rápida sin OpenAI
      3. Debounce 2s → acumular mensajes rápidos consecutivos
      4. Lock por teléfono → historial siempre actualizado al procesar
    """
    # 1. Mensaje vacío — segunda línea de defensa (el endpoint ya valida,
    #    pero "   " pasa la validación de Pydantic)
    if not mensaje or not mensaje.strip():
        return

    # 2. Mensajes no-texto — respuesta inmediata sin tocar OpenAI ni historial
    if mensaje in MENSAJES_NO_TEXTO:
        await send_whatsapp_message(telefono, MENSAJES_NO_TEXTO[mensaje])
        return

    # 3. Debounce — acumular mensajes rápidos del mismo usuario.
    #    Usamos object() como token de identidad única para distinguir incluso
    #    mensajes con el mismo texto (evita el bug de comparación por valor).
    my_token = object()
    if telefono not in _pending_messages:
        _pending_messages[telefono] = []
    _pending_messages[telefono].append((my_token, mensaje))

    await asyncio.sleep(2)  # ventana de espera — FUERA del lock

    pending = _pending_messages.get(telefono, [])
    if not pending or pending[-1][0] is not my_token:
        return  # llegó un mensaje posterior, él se encarga de procesar todo

    # Somos el último mensaje en la ventana — tomar todos y limpiar
    todos = _pending_messages.pop(telefono, [(my_token, mensaje)])
    mensaje_final = "\n".join(t[1] for t in todos)

    # 4. Lock — garantiza que el historial esté actualizado antes de leer
    async with _get_phone_lock(telefono):
        try:
            clear_old_conversations(max_age_minutes=120)

            cliente             = get_or_create_client(telefono, nombre_cliente)
            menu_items          = get_menu()
            barrios             = get_barrios()
            pedidos_activos     = get_active_orders(cliente["id"])
            menu_formateado     = format_menu_for_ai(menu_items)
            barrios_formateados = format_barrios_for_ai(barrios)

            conversation_history = get_conversation_history(telefono)

            # Construir contexto de pedidos para el system prompt
            pedidos_activos_ctx = []
            for pedido in pedidos_activos:
                if pedido.get("items"):
                    items_desc = []
                    total      = pedido.get("total_order", 0)
                    precio_dom = pedido.get("precio_domicilio", 0)
                    for item in pedido["items"]:
                        nombre = item.get('product_name')
                        sabores_extra = item.get('sabores_extra')
                        if sabores_extra:
                            nombre += "/" + "/".join(sabores_extra)
                        items_desc.append(
                            f"{item.get('quantity')}x {nombre} {item.get('variant_name')}"
                        )
                    info = (
                        f"Items: {', '.join(items_desc)} | "
                        f"Subtotal: ${total:,.0f} | "
                        f"Domicilio: ${precio_dom:,.0f} | "
                        f"Total: ${total + precio_dom:,.0f} | "
                        f"Dirección: {pedido.get('address_delivery', 'sin definir')}"
                    )
                else:
                    info = "sin items"
                pedidos_activos_ctx.append({
                    "order_id": pedido["id"],
                    "estado": pedido["state"],
                    "info": info,
                })

            system_prompt = build_system_prompt(
                nombre_cliente=cliente.get("name", "Cliente"),
                direccion_guardada=cliente.get("address"),
                pedidos_activos=pedidos_activos_ctx,
                barrio_session=cliente.get("barrio") or "",
            )

            menu_ctx = build_menu_context(menu_formateado, barrios_formateados)

            respuesta, new_history, session_data = call_openai(
                mensaje_final,
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
