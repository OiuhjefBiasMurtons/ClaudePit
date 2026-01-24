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
            "description": "Crea un nuevo pedido para el cliente. Usa esta función cuando el cliente confirme que quiere hacer un pedido con los productos seleccionados.",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "Lista de productos a ordenar",
                        "items": {
                            "type": "object",
                            "properties": {
                                "variant_id": {
                                    "type": "string",
                                    "description": "ID de la variante del producto (del menú)"
                                },
                                "quantity": {
                                    "type": "integer",
                                    "description": "Cantidad a ordenar"
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
                        "description": "Dirección de entrega del pedido"
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
            "description": "Obtiene el pedido activo (pendiente) del cliente actual. Usa esta función para verificar si el cliente ya tiene un pedido en curso.",
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
            "description": "Agrega más productos a un pedido existente. IMPORTANTE: Primero debes llamar a get_active_order para obtener el order_id del pedido activo del cliente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID UUID del pedido activo (obtenido de get_active_order). Ejemplo: 'a7800efb-397c-42da-a020-2563c73feaa7'"
                    },
                    "items": {
                        "type": "array",
                        "description": "Lista de productos a agregar",
                        "items": {
                            "type": "object",
                            "properties": {
                                "variant_id": {
                                    "type": "string",
                                    "description": "ID de la variante del producto"
                                },
                                "quantity": {
                                    "type": "integer",
                                    "description": "Cantidad a ordenar"
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
            "description": "Actualiza la dirección de entrega de un pedido. IMPORTANTE: Primero debes llamar a get_active_order para obtener el order_id del pedido activo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID UUID del pedido activo (obtenido de get_active_order['id']). Ejemplo: 'a7800efb-397c-42da-a020-2563c73feaa7'"
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
            "description": "Confirma el pedido para que sea procesado y enviado. IMPORTANTE: Primero debes llamar a get_active_order para obtener el order_id del pedido activo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID UUID del pedido activo (obtenido de get_active_order['id']). Ejemplo: 'a7800efb-397c-42da-a020-2563c73feaa7'"
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
            "description": "Cancela un pedido. IMPORTANTE: Primero debes llamar a get_active_order para obtener el order_id del pedido activo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID UUID del pedido activo (obtenido de get_active_order['id']). Ejemplo: 'a7800efb-397c-42da-a020-2563c73feaa7'"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]


def build_system_prompt(cliente: dict, menu_formateado: str, pedido_activo: dict | None) -> str:
    nombre = cliente.get("name", "Cliente")

    pedido_info = ""
    if pedido_activo:
        pedido_info = f"""
PEDIDO ACTIVO:
- Ticket: {pedido_activo.get('ticket_id', 'N/A')}
- Estado: {pedido_activo.get('state', 'N/A')}
- Total actual: ${pedido_activo.get('total_order', 0):.2f}
- Dirección: {pedido_activo.get('address_delivery', 'No especificada')}
"""
    else:
        pedido_info = "No hay pedido activo."

    return f"""Eres el asistente virtual de una pizzería. Tu nombre es PizzaBot.

CLIENTE ACTUAL:
- Nombre: {nombre}
- Teléfono: {cliente.get('cel', 'N/A')}

{pedido_info}

MENÚ DISPONIBLE:
{menu_formateado}

INSTRUCCIONES:
1. Sé amable y profesional
2. Ayuda al cliente a hacer pedidos
3. Muestra precios cuando menciones productos
4. Usa los IDs de variante cuando el cliente quiera ordenar
5. Si el cliente quiere ordenar, necesitas: productos con sus variantes y dirección de entrega
6. Confirma siempre el pedido antes de procesarlo
7. Responde en español
8. Sé conciso, esto es WhatsApp

REGLAS:
- Solo puedes vender lo que está en el menú
- No inventes productos ni precios
- Si no entiendes algo, pide aclaración
"""


def call_openai(mensaje: str, system_prompt: str, client_id: str, conversation_history: list = None) -> str:
    messages = [{"role": "system", "content": system_prompt}]

    if conversation_history:
        messages.extend(conversation_history)

    messages.append({"role": "user", "content": mensaje})

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
        temperature=0.7,
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
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    return final_response.choices[0].message.content
