from datetime import datetime, timedelta, timezone
import logging

from app.database import get_supabase_client

logger = logging.getLogger(__name__)

MAX_MESSAGES = 20


def get_conversation_history(telefono: str, limit: int = 20) -> list:
    """Obtiene el historial de conversación desde Supabase."""
    try:
        supabase = get_supabase_client()
        result = supabase.table("conversation_history") \
            .select("messages") \
            .eq("telefono", telefono) \
            .execute()

        if not result.data:
            return []

        row: dict = result.data[0]  # type: ignore[assignment]
        messages: list = row.get("messages", [])
        return messages[-limit:]

    except Exception as e:
        logger.error(f"Error obteniendo historial de {telefono}: {e}")
        return []


def update_conversation_history(telefono: str, new_history: list) -> None:
    """Guarda el historial completo en Supabase (upsert)."""
    try:
        supabase = get_supabase_client()
        trimmed = new_history[-MAX_MESSAGES:]

        supabase.table("conversation_history").upsert({
            "telefono": telefono,
            "messages": trimmed,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).execute()

    except Exception as e:
        logger.error(f"Error guardando historial de {telefono}: {e}")


def clear_old_conversations(max_age_minutes: int = 120) -> int:
    """Elimina conversaciones inactivas hace más de max_age_minutes."""
    try:
        supabase = get_supabase_client()
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=max_age_minutes)).isoformat()

        result = supabase.table("conversation_history") \
            .delete() \
            .lt("updated_at", cutoff) \
            .execute()

        deleted = len(result.data) if result.data else 0
        if deleted:
            logger.info(f"Conversaciones antiguas eliminadas: {deleted}")
        return deleted

    except Exception as e:
        logger.error(f"Error limpiando conversaciones: {e}")
        return 0


def add_message(telefono: str, role: str, content: str) -> None:
    """Compatibilidad: agrega un mensaje individual al historial."""
    history = get_conversation_history(telefono)
    history.append({"role": role, "content": content})
    update_conversation_history(telefono, history)
