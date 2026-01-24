# 🍕 Pizzeria WhatsApp Bot

Bot inteligente de WhatsApp para gestionar pedidos de pizzería usando IA (OpenAI GPT-4) y Supabase como base de datos.

## ✨ Características

- 🤖 **Asistente IA**: Conversación natural con los clientes usando OpenAI GPT-4
- 📋 **Gestión de menú**: Muestra productos con variantes y precios
- 🛒 **Pedidos inteligentes**: Crea, modifica y confirma pedidos
- 💾 **Base de datos**: Almacenamiento en Supabase (PostgreSQL)
- 📍 **Direcciones de entrega**: Gestión de direcciones para cada pedido
- 🎫 **Tickets únicos**: Generación automática de IDs de pedido
- 📊 **Estados de orden**: PREPARANDO → EN_CAMINO → ENTREGADO / CANCELADO

## 🏗️ Arquitectura

```
pizzeria-bot/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app y endpoints
│   ├── config.py         # Configuración y variables de entorno
│   ├── database.py       # Conexión a Supabase y queries
│   ├── ai_service.py     # Integración con OpenAI
│   ├── tools.py          # Funciones de negocio (crear pedidos, etc)
│   ├── memory.py         # Gestión de conversaciones
│   └── utils.py          # Utilidades (formateo, generación de IDs)
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── SCHEMA.md            # Documentación del esquema de BD
```

## 🗄️ Esquema de Base de Datos

El proyecto usa Supabase (PostgreSQL) con las siguientes tablas:

- **clients**: Información de clientes (nombre, teléfono, dirección)
- **products**: Productos base (pizzas, bebidas, etc)
- **product_variants**: Variantes de productos (tamaños, sabores)
- **orders**: Órdenes de los clientes
- **order_details**: Items de cada orden

Ver [SCHEMA.md](SCHEMA.md) para detalles completos.

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/pizzeria-bot.git
cd pizzeria-bot
```

### 2. Crear entorno virtual

```bash
python -m venv Pit
```

### 3. Activar entorno virtual

**Linux/Mac:**
```bash
source Pit/bin/activate
```

**Windows:**
```bash
Pit\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Copiar el archivo de ejemplo y configurar tus credenciales:

```bash
cp .env.example .env
```

Editar `.env` con tus valores:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_service_role_key_aqui
OPENAI_API_KEY=sk-tu-api-key-de-openai
OPENAI_MODEL=gpt-4o-mini
```

⚠️ **IMPORTANTE**: Usa la **service_role key** de Supabase, no la anon key.

### 6. Configurar Base de Datos

1. Crea un proyecto en [Supabase](https://supabase.com)
2. Ejecuta las migraciones SQL (ver `SCHEMA.md`)
3. Configura Row-Level Security (RLS) según tus necesidades

## 🏃 Ejecutar el proyecto

### Modo desarrollo

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

### Modo producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🧪 Probar el endpoint

### Usando curl

```bash
curl -X POST http://localhost:8000/process-message \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "+573001234567",
    "nombre_cliente": "Juan Pérez",
    "mensaje": "Hola, quiero ver el menú"
  }'
```

### Respuesta esperada

```json
{
  "respuesta": "¡Hola, Juan! Aquí tienes el menú disponible:\n\n**Pizzas:**\n..."
}
```

## 🔌 Integración con WhatsApp

Para conectar el bot con WhatsApp, puedes usar:

1. **Twilio API**: Servicio de mensajería
2. **WhatsApp Business API**: API oficial
3. **Baileys**: Librería de WhatsApp Web

Ejemplo con webhook:
```python
@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    # Procesar mensaje de WhatsApp
    # Llamar a /process-message
    # Enviar respuesta
```

## 📝 API Endpoints

### POST `/process-message`

Procesa un mensaje del cliente y devuelve la respuesta del bot.

**Request:**
```json
{
  "telefono": "string",
  "nombre_cliente": "string",
  "mensaje": "string"
}
```

**Response:**
```json
{
  "respuesta": "string"
}
```

## 🛠️ Funcionalidades del Bot

El bot puede:

- ✅ Mostrar el menú completo con precios
- ✅ Crear nuevos pedidos
- ✅ Agregar items a pedidos existentes
- ✅ Actualizar dirección de entrega
- ✅ Confirmar pedidos
- ✅ Cancelar pedidos
- ✅ Mantener contexto de conversación
- ✅ Recordar pedidos activos del cliente

## 🔧 Configuración Avanzada

### Personalizar el modelo de IA

En `.env`:
```env
OPENAI_MODEL=gpt-4o-mini  # Más económico
# o
OPENAI_MODEL=gpt-4o       # Más potente
```

### Ajustar temperatura de respuestas

En `app/ai_service.py`:
```python
temperature=0.7  # Más creativo (0.0 - 1.0)
```

### Modificar tiempo de expiración de conversaciones

En `app/memory.py`:
```python
CONVERSATION_TIMEOUT = timedelta(minutes=30)
```

## 📊 Monitoreo

Los logs de uvicorn muestran:
- Peticiones entrantes
- Errores de la aplicación
- Llamadas a funciones de IA
- Queries a la base de datos

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

**Tu Nombre**
- GitHub: [@TU_USUARIO](https://github.com/TU_USUARIO)

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/)
- [Supabase](https://supabase.com/)
- [OpenAI](https://openai.com/)

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
