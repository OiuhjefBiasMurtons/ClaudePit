# 📦 Backup de Supabase - PitzBias

**Proyecto:** vdpongjfmldvjxokhiov  
**Fecha de backup:** 2026-01-29 23:22:52  
**Región:** us-east-2  
**Estado:** ACTIVE_HEALTHY

## 📋 Contenido del Backup

### 1. `schema_backup.sql`
Contiene la estructura completa de la base de datos:
- ✅ Tipos personalizados (ENUMs)
- ✅ Definición de todas las tablas
- ✅ Claves primarias y foráneas
- ✅ Configuración de Row Level Security (RLS)
- ✅ Índices para optimización

### 2. `data_backup.sql`
Contiene todos los datos actuales:
- **Clientes:** 1 registro
- **Productos:** 5 registros
- **Variantes de productos:** 8 registros
- **Órdenes:** 2 registros
- **Detalles de órdenes:** 4 registros

### 3. `restore_instructions.md`
Instrucciones detalladas para restaurar el backup

## 🗂️ Estructura de la Base de Datos

```
┌─────────────┐
│  clients    │
└──────┬──────┘
       │
       │ (1:N)
       │
┌──────▼──────┐
│   orders    │
└──────┬──────┘
       │
       │ (1:N)
       │
┌──────▼──────────┐
│ order_details   │
└──────┬──────────┘
       │
       │ (N:1)
       │
┌──────▼────────────┐
│ product_variants  │
└──────┬────────────┘
       │
       │ (N:1)
       │
┌──────▼──────┐
│  products   │
└─────────────┘
```

## 📊 Resumen de Datos

### Productos Activos
1. **Pizza Hawaiana** (Mediana: $37,000)
2. **Pizza De la Casa** (Grande: $45,000, Mediana: $37,000)
3. **Limonada de Coco** (Vaso: $12,000)
4. **Coca Cola** (Personal: $4,000, 1/2 Litro: $5,500, 2 Litros: $8,000)
5. **Coca Cola Zero** (Personal: $3,350)

### Órdenes
- **Orden #13:** EN_CAMINO - Total: $49,000
- **Orden #14:** PREPARANDO - Total: $45,000

## 🔄 Cómo Restaurar

### Opción 1: Restauración Completa (Base de datos nueva)
```bash
# 1. Ejecutar schema_backup.sql
# 2. Ejecutar data_backup.sql
```

### Opción 2: Restauración Solo de Datos
```bash
# Solo ejecutar data_backup.sql en una base existente
```

### Opción 3: Usando el MCP de Supabase
Ver `restore_instructions.md` para instrucciones detalladas

## ⚠️ Notas Importantes

1. **ticket_id** en la tabla `orders` es un campo `GENERATED ALWAYS AS IDENTITY`, por lo que al restaurar datos, debes:
   - Eliminar la columna `ticket_id` de los INSERTs, O
   - Usar `OVERRIDING SYSTEM VALUE` en el INSERT

2. **RLS está habilitado** en todas las tablas. Asegúrate de configurar las políticas apropiadas después de restaurar.

3. **UUIDs:** Los IDs son UUIDs específicos. Si restauras en una base nueva, estos IDs se mantendrán.

## 🔐 Información de Conexión

```
URL: https://vdpongjfmldvjxokhiov.supabase.co
Database Host: db.vdpongjfmldvjxokhiov.supabase.co
PostgreSQL Version: 17.6.1.054
```

## 📝 Changelog

- **2026-01-29:** Backup inicial creado
  - 1 cliente
  - 5 productos
  - 8 variantes
  - 2 órdenes activas
  - 4 items en órdenes

---

**Generado automáticamente por Antigravity**
