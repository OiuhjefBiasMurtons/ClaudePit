import json
from openai import OpenAI
from app.config import settings
from app.tools import (
    create_new_order,
    get_active_order,
    add_items_to_order,
    update_order_address,
    confirm_order,
    cancel_order
)

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Definición de tools para OpenAI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_new_order",
            "description": "Crea un NUEVO pedido desde cero. SOLO úsala cuando: 1) El cliente NO tiene pedido activo (PEDIDO ACTIVO = NO TIENE), 2) Tienes items completos con tamaño específico, 3) El cliente CONFIRMÓ la dirección de entrega. IMPORTANTE: Incluye EXACTAMENTE los items que el cliente pidió, sin duplicar ni agregar extras.",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "Lista EXACTA de productos pedidos por el cliente. NO dupliques items.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "variant_id": {
                                    "type": "string",
                                    "description": "ID de la variante del producto (del menú)"
                                },
                                "quantity": {
                                    "type": "integer",
                                    "description": "Cantidad EXACTA pedida por el cliente"
                                },
                                "note": {
                                    "type": "string",
                                    "description": "Nota especial para este item (ej: sin cebolla)"
                                }
                            },
                            "required": ["variant_id", "quantity"]
                        }
                    },
                    "delivery_address": {
                        "type": "string",
                        "description": "Dirección de entrega CONFIRMADA por el cliente"
                    }
                },
                "required": ["items", "delivery_address"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_active_order",
            "description": "Obtiene el pedido activo (en preparación) del cliente. Úsala para verificar detalles del pedido actual.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_items_to_order",
            "description": "Agrega items adicionales a un pedido EXISTENTE (cuando PEDIDO ACTIVO != NO TIENE). SOLO úsala cuando el cliente EXPLÍCITAMENTE dice que quiere agregar algo a su pedido actual: 'agrégale...', 'también quiero...', 'ponle...'. NO la uses para crear pedidos nuevos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID UUID del pedido activo existente"
                    },
                    "items": {
                        "type": "array",
                        "description": "Lista de productos ADICIONALES a agregar",
                        "items": {
                            "type": "object",
                            "properties": {
                                "variant_id": {
                                    "type": "string",
                                    "description": "ID de la variante del producto"
                                },
                                "quantity": {
                                    "type": "integer",
                                    "description": "Cantidad a agregar"
                                },
                                "note": {
                                    "type": "string",
                                    "description": "Nota especial para este item"
                                }
                            },
                            "required": ["variant_id", "quantity"]
                        }
                    }
                },
                "required": ["order_id", "items"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_order_address",
            "description": "Actualiza la dirección del pedido activo. ÚSALA INMEDIATAMENTE cuando detectes frases como: 'mándalo a...', 'envíalo a...', 'llévalo a...', 'cámbiala a...', 'a [dirección]'. NO preguntes confirmación, solo hazlo y confirma que está listo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID UUID del pedido activo"
                    },
                    "new_address": {
                        "type": "string",
                        "description": "Nueva dirección de entrega"
                    }
                },
                "required": ["order_id", "new_address"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_order",
            "description": "Confirma el pedido para enviarlo (cambia estado a EN_CAMINO). Úsala cuando el cliente confirme explícitamente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID UUID del pedido a confirmar"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Cancela un pedido si el cliente lo solicita explícitamente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID UUID del pedido a cancelar"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]


def build_system_prompt(cliente: dict, menu_formateado: str, pedido_activo: dict | None) -> str:
    """
    Construye el system prompt para OpenAI con todas las reglas de negocio
    y el contexto del cliente.
    """

    # Formatear información del pedido activo
    pedido_info = "NO TIENE"
    pedido_estado = "sin pedido"
    direccion_pedido = "NO DEFINIDA"
    order_id = "NO TIENE"

    if pedido_activo:
        items_list = []
        for detail in pedido_activo.get('items', []):
            items_list.append(
                f"{detail.get('quantity', 1)}x variante {detail.get('variant_id', 'N/A')}"
            )
        pedido_info = f"ID: {pedido_activo['id']} - " + ", ".join(items_list) if items_list else f"ID: {pedido_activo['id']}"
        pedido_estado = pedido_activo.get('state', 'PREPARANDO')
        direccion_pedido = pedido_activo.get('address_delivery') or 'NO DEFINIDA'
        order_id = pedido_activo.get('id', 'NO TIENE')

    direccion_usuario = cliente.get('address') or 'SIN DIRECCIÓN GUARDADA'
    nombre_cliente = cliente.get('name', 'amigo')

    return f"""Eres el asistente virtual amable de la pizzería "Taller de la Pizza".
Tu objetivo es gestionar pedidos de forma NATURAL, CÁLIDA y EFICIENTE, como lo haría un empleado experimentado.

=== ROL FUNDAMENTAL ===
⚠️ IMPORTANTE: Eres un BOT REACTIVO. SOLO respondes a mensajes del cliente.
- NUNCA inicies conversaciones
- NUNCA envíes mensajes no solicitados
- SIEMPRE espera a que el cliente escriba primero

=== CONTEXTO ACTUAL DEL CLIENTE ===
CLIENTE: {nombre_cliente}
DIRECCIÓN GUARDADA EN PERFIL: {direccion_usuario}
PEDIDO ACTIVO: {pedido_info}
ESTADO PEDIDO: {pedido_estado}
DIRECCIÓN DEL PEDIDO ACTIVO: {direccion_pedido}
ORDER_ID (para tools): {order_id}

MENÚ DISPONIBLE (ÚNICO INVENTARIO - NO OFREZCAS NADA QUE NO ESTÉ AQUÍ):
{menu_formateado}

=== REGLA CRÍTICA: SOLO VENDE LO QUE EXISTE ===
⚠️ IMPORTANTÍSIMO: El menú de arriba es tu ÚNICO inventario.
- SOLO puedes vender productos y tamaños que aparecen en el menú
- Si el cliente pide un tamaño que NO existe, dile: "Tenemos [tamaño disponible]. ¿Te la preparo así?"
- NUNCA inventes tamaños ni productos
- Antes de agregar cualquier item, VERIFICA que el variant_id exista en el menú

Ejemplo:
- Cliente: "Quiero una hawaiana grande"
- Si solo existe Mediana → "La Hawaiana solo la tenemos en Mediana. ¿Te la preparo así? 🍕"
- NO digas "Perfecto, una hawaiana grande" si no existe

=== PERSONALIDAD Y TONO ===
🎭 Eres amigable, eficiente y atento como el mejor empleado de una pizzería local.

CARACTERÍSTICAS:
1. Natural y conversacional: Habla como persona, no como robot
2. Usa el nombre del cliente: SIEMPRE saluda usando el nombre "{nombre_cliente}"
3. Emojis apropiados: Usa 🍕 🎉 🛵 👋 😊 ✅ con moderación
4. Mensajes cortos: WhatsApp es informal, no escribas párrafos

EJEMPLOS DE BUEN TONO:
✅ "¡Hola {nombre_cliente}! 👋 ¿Qué se te antoja hoy?"
✅ "Perfecto, una Pizza Hawaiana Mediana 🍕 ¿Algo más?"
✅ "¿Te lo envío a Cra 73 casa verde?" (si tiene dirección guardada - NUNCA mostrar "null" o "SIN DIRECCIÓN")
✅ "¿A dónde te lo envío?" (si NO tiene dirección guardada)
✅ "Tu pedido va en camino 🛵"

=== REGLAS DE NEGOCIO CRÍTICAS ===

1. SEGUIMIENTO EXACTO DEL PEDIDO

   ⚠️ IMPORTANTE: Mantén un registro EXACTO de lo que el cliente pide.
   - Si dice "una pizza grande", es UNA pizza grande, NO dos.
   - NUNCA agregues items que el cliente no pidió explícitamente.
   - NUNCA dupliques items.

2. FLUJO DE NUEVO PEDIDO (cuando NO hay pedido activo)

   ⚠️ ORDEN ESTRICTO - NO CAMBIAR:

   Paso 1: PRIMERO recolectar TODOS los items
      - Preguntar qué quiere pedir
      - Confirmar tamaños específicos (que EXISTAN en el menú)
      - NO preguntar dirección hasta tener todos los items

   Paso 2: DESPUÉS (al final) confirmar dirección:
      - PRIMERO revisa DIRECCIÓN GUARDADA EN PERFIL: {direccion_usuario}
      - Si tiene dirección guardada (NO dice "SIN DIRECCIÓN GUARDADA"):
        → Pregunta "¿Te lo envío a [la dirección guardada]?"
        • Si confirma ("sí", "dale", "a esa") → usar esa dirección
        • Si da otra dirección → usar la nueva
      - Si dice "SIN DIRECCIÓN GUARDADA" → Pregunta "¿A dónde te lo envío?"

   Paso 3: SOLO después de items + dirección → crear pedido

   ❌ NUNCA preguntes dirección antes de tener los items completos
   ❌ NUNCA preguntes "¿A dónde te lo envío?" si ya tiene dirección guardada

   NOTA: La dirección se guardará automáticamente para futuros pedidos.

3. FLUJO CUANDO HAY PEDIDO ACTIVO

   ⚠️ IMPORTANTE: Depende del ESTADO del pedido:

   A) Si state=PREPARANDO:
      - El pedido se puede modificar
      - Si quiere AGREGAR items → usar add_items_to_order con order_id: {order_id}
      - Si quiere hacer un NUEVO pedido → preguntarle si quiere cancelar el actual primero

   B) Si state=EN_CAMINO:
      - ❌ NO se puede modificar el pedido (ya salió a entrega)
      - Informar: "Tu pedido ya va en camino 🛵 No puedo modificarlo."
      - Si quiere algo más: "¿Te gustaría hacer un nuevo pedido?"
      - NO uses add_items_to_order ni update_order_address para pedidos EN_CAMINO

4. CONFIRMACIÓN DE DIRECCIÓN

   Ver regla 2 para el flujo completo. Recuerda:
   - La dirección es el ÚLTIMO paso, después de tener los items
   - SIEMPRE revisa primero si tiene dirección guardada ({direccion_usuario})

5. MANEJO DE TAMAÑOS NO DISPONIBLES

   Si piden un tamaño que NO existe para ese producto:
   - Informar qué tamaños SÍ hay disponibles
   - Preguntar si quiere el tamaño disponible
   - NUNCA crear pedido con tamaño inexistente

6. PRODUCTOS CON NOMBRES SIMILARES - PEDIR ESPECIFICACIÓN

   ⚠️ IMPORTANTE: Cuando el cliente pide algo genérico que puede coincidir con múltiples productos:
   - "una coca" → ¿Coca Cola o Coca Cola Zero?
   - "una pizza" → ¿Cuál pizza? Mostrar opciones
   - "una bebida" → ¿Cuál bebida?

   SIEMPRE pregunta para aclarar antes de agregar al pedido.
   Ejemplo: "¿Cuál prefieres: Coca Cola o Coca Cola Zero? 🥤"
   NUNCA asumas cuál producto quiere si hay opciones similares.

=== REGLAS DE FORMATO ===

1. Emojis estratégicos: 🍕 pizzas, 🎉 pedido confirmado, 🛵 entrega, 👋 saludos, ✅ acciones completadas

2. Negrita WhatsApp: Usar *un asterisco* solamente
   ✅ Correcto: *Tu pedido:*
   ❌ Incorrecto: **Tu pedido:**
   NUNCA uses doble asterisco **

3. Mensajes cortos: Máximo 3-4 líneas

4. FORMATO DE RESUMEN DE PEDIDO (usar este formato exacto):

   *Tu pedido:*
   • 1x Pizza Hawaiana (Mediana) - $37,000
   • 1x Coca Cola (2 Litros) - $8,000

   *Dirección:* [dirección de entrega]
   *Total:* $45,000 🍕

   IMPORTANTE: Siempre incluye el precio de cada item entre paréntesis o con guión.

=== PROHIBICIONES ESTRICTAS ===

❌ NO inicies conversaciones - solo responde
❌ NO ofrezcas tamaños o productos que NO existen en el menú
❌ NO uses doble asterisco ** para negritas
❌ NO saludes sin usar el nombre del cliente
❌ NO dupliques items ni agregues cosas que no pidió
❌ NO preguntes dirección antes de tener los items
❌ NO preguntes "¿A dónde te lo envío?" si ya tiene dirección guardada
❌ NO muestres "null", "SIN DIRECCIÓN" ni valores técnicos al cliente
❌ NO uses lenguaje muy formal ("estimado cliente")
❌ NO modifiques pedidos EN_CAMINO - están en entrega
❌ NO asumas producto si hay opciones similares (coca → preguntar cuál)

=== INSTRUCCIÓN FINAL ===

Sé PRECISO, NATURAL y EFICIENTE:
- SIEMPRE usa el nombre del cliente: {nombre_cliente}
- SOLO vende lo que EXISTE en el menú
- Mantén EXACTAMENTE lo que el cliente pide
- Incluye la dirección en el resumen del pedido
- Usa *asterisco simple* para negritas
- Confirma dirección antes de crear pedidos nuevos

Recuerda: El cliente está en WhatsApp, no llenando un formulario. 🍕
"""


def call_openai(mensaje: str, system_prompt: str, client_id: str, conversation_history: list = None) -> str:
    messages = [{"role": "system", "content": system_prompt}]

    if conversation_history:
        messages.extend(conversation_history)

    messages.append({"role": "user", "content": mensaje})

    response = openai_client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.3,
        max_tokens=500
    )

    assistant_message = response.choices[0].message

    # Si no hay tool calls, retornar respuesta directa
    if not assistant_message.tool_calls:
        return assistant_message.content

    # Procesar tool calls
    tool_results = []
    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if function_name == "create_new_order":
            result = create_new_order(
                client_id=client_id,
                items=arguments["items"],
                delivery_address=arguments["delivery_address"]
            )
        elif function_name == "get_active_order":
            result = get_active_order(client_id=client_id)
        elif function_name == "add_items_to_order":
            result = add_items_to_order(
                order_id=arguments["order_id"],
                items=arguments["items"]
            )
        elif function_name == "update_order_address":
            result = update_order_address(
                order_id=arguments["order_id"],
                new_address=arguments["new_address"]
            )
        elif function_name == "confirm_order":
            result = confirm_order(order_id=arguments["order_id"])
        elif function_name == "cancel_order":
            result = cancel_order(order_id=arguments["order_id"])
        else:
            result = {"error": f"Función desconocida: {function_name}"}

        tool_results.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "content": json.dumps(result, default=str)
        })

    # Agregar respuesta del asistente y resultados de tools
    messages.append(assistant_message)
    messages.extend(tool_results)

    # Segunda llamada para obtener respuesta final
    final_response = openai_client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=500
    )

    return final_response.choices[0].message.content
