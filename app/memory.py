from datetime import datetime, timedelta

# Almacenamiento en memoria
conversations = {}


def add_message(telefono: str, role: str, content: str):
    """
    Agrega un mensaje a la conversación del usuario.

    role: "user" o "assistant"
    """
    if telefono not in conversations:
        conversations[telefono] = {
            "messages": [],
            "last_activity": datetime.now()
        }

    conversations[telefono]["messages"].append({
        "role": role,
        "content": content
    })
    conversations[telefono]["last_activity"] = datetime.now()


def get_conversation_history(telefono: str, limit: int = 10) -> list:
    """
    Obtiene el historial de conversación del usuario.
    Retorna los últimos `limit` mensajes.
    """
    if telefono not in conversations:
        return []

    messages = conversations[telefono]["messages"]
    return messages[-limit:]


def clear_old_conversations(max_age_minutes: int = 30):
    """
    Limpia conversaciones inactivas por más de max_age_minutes.
    """
    cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
    to_delete = []

    for telefono, data in conversations.items():
        if data["last_activity"] < cutoff:
            to_delete.append(telefono)

    for telefono in to_delete:
        del conversations[telefono]

    return len(to_delete)
