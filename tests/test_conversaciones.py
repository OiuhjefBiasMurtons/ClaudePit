"""
Tests de conversaciones completas para validar el comportamiento del bot.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.ai_service import build_system_prompt, call_openai


class TestConversacionesBot:
    """Tests de escenarios de conversación reales"""

    @pytest.fixture
    def mock_menu(self):
        """Menú de prueba con pizzas y lasañas"""
        return """[
  {
    "name": "Pizza Hawaiana",
    "ingredients": "Jamón, piña",
    "category": "Pizza",
    "sizes": [
      {"size": "Personal", "price": 15000, "id": "haw-personal"},
      {"size": "Mediana", "price": 25000, "id": "haw-mediana"},
      {"size": "Familiar", "price": 55000, "id": "haw-familiar"}
    ]
  },
  {
    "name": "Lasagna Mixta",
    "ingredients": "Pollo, carne bolognesa",
    "category": "Lasagna",
    "sizes": [
      {"size": "Mediana", "price": 23000, "id": "mix-mediana"},
      {"size": "Extra", "price": 27000, "id": "mix-extra"}
    ]
  }
]"""

    def test_escenario_1_agregar_items_sin_asumir_tamano(self, mock_menu):
        """
        Escenario: Cliente tiene pedido activo y quiere agregar lasañas.
        Problema previo: El bot asumía tamaño "Extra" cuando no se especificó.
        Expectativa: Debe preguntar el tamaño, no asumirlo.
        """
        # Cliente tiene un pedido activo con 5 pizzas
        order_id = "order-123"
        pedido_info = "Items: 5x Pizza Hawaiana Familiar | Total: $275,000"

        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id=order_id,
            estado_pedido="PREPARANDO",
            menu_formateado=mock_menu,
            pedido_info=pedido_info
        )

        # Validar que el prompt contiene información del pedido
        assert "5x Pizza Hawaiana Familiar" in system_prompt
        assert order_id in system_prompt

        # Validar que el prompt tiene la regla de no asumir tamaños
        assert "NUNCA asumas tamaños" in system_prompt
        assert "add_items_to_order" in system_prompt

    def test_escenario_2_mantener_contexto_producto(self, mock_menu):
        """
        Escenario: Cliente dice "lasañas mixtas", luego solo corrige el tamaño.
        Problema previo: El bot olvidaba que ya había dicho "mixtas".
        Expectativa: Debe recordar el tipo de lasaña mencionado.
        """
        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="order-123",
            estado_pedido="PREPARANDO",
            menu_formateado=mock_menu,
            pedido_info="Items: 5x Pizza Hawaiana Familiar"
        )

        # Validar que el prompt instruye mantener contexto
        assert "Lee TODA la conversación previa para mantener contexto" in system_prompt
        assert "NO preguntes de nuevo qué tipo" in system_prompt

    def test_escenario_3_no_crear_pedido_nuevo(self, mock_menu):
        """
        Escenario: Cliente tiene pedido activo y corrige información.
        Problema previo: El bot creaba un nuevo pedido en lugar de modificar el existente.
        Expectativa: Debe usar add_items_to_order, no create_new_order.
        """
        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="order-123",
            estado_pedido="PREPARANDO",
            menu_formateado=mock_menu,
            pedido_info="Items: 5x Pizza Hawaiana Familiar"
        )

        # Validar que el prompt enfatiza usar add_items_to_order
        assert "SIEMPRE usa add_items_to_order" in system_prompt
        assert "NUNCA uses create_new_order" in system_prompt
        assert "YA EXISTE UN PEDIDO" in system_prompt

    def test_escenario_4_calcular_total_con_pedido_existente(self, mock_menu):
        """
        Escenario: Cliente pregunta por el total incluyendo items previos.
        Problema previo: El bot no recordaba los items del pedido anterior.
        Expectativa: Debe usar la información de pedido_info para calcular correctamente.
        """
        pedido_info = "Items: 5x Pizza Hawaiana Familiar | Total: $275,000 | Dirección: Cra 74 #13a"

        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="order-123",
            estado_pedido="PREPARANDO",
            menu_formateado=mock_menu,
            pedido_info=pedido_info
        )

        # Validar que el pedido_info está en el prompt
        assert "5x Pizza Hawaiana Familiar" in system_prompt
        assert "$275,000" in system_prompt

        # Validar que hay regla para usar pedido_actual
        assert "pedido_actual" in system_prompt.lower()

    def test_escenario_5_no_listar_todos_los_productos(self, mock_menu):
        """
        Escenario: Cliente pide una lasaña sin especificar tipo.
        Problema previo: El bot listaba todos los 8 tipos de lasaña.
        Expectativa: Debe preguntar de forma simple sin listar todo.
        """
        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="N/A",
            estado_pedido="N/A",
            menu_formateado=mock_menu
        )

        # Validar que el prompt instruye no listar todos los productos
        assert "NO listes todos los productos" in system_prompt
        assert "3 o menos opciones" in system_prompt
        assert "pregunta de forma simple sin listar todos" in system_prompt

    @patch("app.ai_service.openai_client")
    @patch("app.tools.get_supabase_client")
    def test_flujo_completo_agregar_items(self, mock_supabase, mock_openai, mock_menu):
        """
        Test de flujo completo: agregar items a pedido existente
        """
        # Setup mocks
        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock calculate_order_preview
        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == "product_variants":
                mock_table.select.return_value.in_.return_value.execute.return_value.data = [
                    {
                        "id": "mix-mediana",
                        "nombre_variante": "Mediana",
                        "price": 23000,
                        "products": {"name": "Lasagna Mixta"}
                    }
                ]
            elif table_name == "order_details":
                mock_table.insert.return_value.execute.return_value.data = [{}]
                mock_table.select.return_value.eq.return_value.execute.return_value.data = [
                    {
                        "quantity": 5,
                        "product_variants": {
                            "nombre_variante": "Familiar",
                            "price": 55000,
                            "products": {"name": "Pizza Hawaiana"}
                        }
                    },
                    {
                        "quantity": 2,
                        "product_variants": {
                            "nombre_variante": "Mediana",
                            "price": 23000,
                            "products": {"name": "Lasagna Mixta"}
                        }
                    }
                ]
            elif table_name == "orders":
                mock_table.select.return_value.eq.return_value.execute.return_value.data = [
                    {"id": "order-123", "total_order": 321000}
                ]
            return mock_table

        mock_client.table.side_effect = table_side_effect

        # Importar aquí para usar los mocks
        from app.tools import add_items_to_order

        # Ejecutar
        result = add_items_to_order(
            order_id="order-123",
            items=[{"variant_id": "mix-mediana", "quantity": 2}]
        )

        # Validar
        assert result["order_id"] == "order-123"
        assert result["total"] == 321000
        assert len(result["items"]) == 2  # 5 pizzas + 2 lasañas

    def test_formato_negritas_whatsapp(self, mock_menu):
        """
        Escenario: El bot debe usar *texto* no **texto** para negritas
        """
        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="N/A",
            estado_pedido="N/A",
            menu_formateado=mock_menu
        )

        # Validar que instruye usar un solo asterisco
        assert "*un asterisco*" in system_prompt
        # NO debe haber ejemplos con doble asterisco en instrucciones
        assert "**texto**" not in system_prompt or "NUNCA" in system_prompt

    def test_validar_state_antes_modificar(self, mock_menu):
        """
        Escenario: No debe modificar pedidos que no estén en PREPARANDO
        """
        # Pedido EN_CAMINO
        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="order-123",
            estado_pedido="EN_CAMINO",
            menu_formateado=mock_menu,
            pedido_info="Items: 5x Pizza Hawaiana Familiar"
        )

        assert "EN_CAMINO" in system_prompt
        assert "ya va en camino" in system_prompt.lower()

    def test_crear_pedido_nuevo_con_pedido_activo(self, mock_menu):
        """
        Escenario: Cliente tiene pedido activo pero quiere crear uno nuevo para otra dirección.
        Expectativa: El bot debe preguntar si quiere agregar al actual o crear uno nuevo.
        IMPORTANTE: NO debe cancelar el pedido anterior (clientes pueden tener múltiples pedidos).
        """
        pedido_info = "Items: 5x Pizza Hawaiana Familiar | Total: $275,000 | Dirección: Cra 74 #13a"

        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="order-123",
            estado_pedido="PREPARANDO",
            menu_formateado=mock_menu,
            pedido_info=pedido_info
        )

        # Validar que el prompt tiene lógica para determinar intención
        assert "determinar_intencion" in system_prompt.lower() or "determinar si quiere" in system_prompt.lower()
        assert "CREAR pedido NUEVO" in system_prompt or "CREAR uno nuevo" in system_prompt

        # Validar que hay ejemplo de crear nuevo pedido
        assert "nuevo pedido" in system_prompt.lower() or "pedido nuevo" in system_prompt.lower()

        # Validar que NO cancela pedidos (clientes pueden tener múltiples activos)
        assert "NO canceles" in system_prompt or "múltiples pedidos activos" in system_prompt

    def test_validar_estado_antes_de_preguntar(self, mock_menu):
        """
        Escenario: Cliente con pedido EN_CAMINO intenta agregar items.
        Expectativa: Bot debe validar estado ANTES de hacer preguntas.
        NO debe preguntar tipo ni tamaño si el pedido no está en PREPARANDO.
        """
        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="order-123",
            estado_pedido="EN_CAMINO",
            menu_formateado=mock_menu,
            pedido_info="Items: 2x Pizza Hawaiana Personal"
        )

        # Validar que hay instrucción de validar estado PRIMERO
        assert "ANTES de" in system_prompt or "PRIMERO" in system_prompt
        assert "estado_pedido" in system_prompt
        assert "EN_CAMINO" in system_prompt
        assert "ya va en camino" in system_prompt.lower()

        # Validar que hay instrucción de NO preguntar si no está en PREPARANDO
        assert "NUNCA preguntes" in system_prompt or "NO preguntes" in system_prompt

    def test_formato_negritas_un_asterisco(self, mock_menu):
        """
        Escenario: Validar que el prompt enfatiza usar UN solo asterisco.
        Expectativa: Debe tener ejemplo claro de NO usar doble asterisco.
        """
        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="N/A",
            estado_pedido="N/A",
            menu_formateado=mock_menu
        )

        # Validar que hay instrucción clara sobre negritas
        assert "*un" in system_prompt.lower() or "*texto*" in system_prompt
        assert "NUNCA" in system_prompt or "❌" in system_prompt
        assert "**" in system_prompt  # Debe mencionar el formato incorrecto como ejemplo

    def test_instrucciones_seguridad(self, mock_menu):
        """
        Escenario: Validar que hay instrucciones de seguridad contra prompt injection.
        Expectativa: Bot debe tener reglas de seguridad claras.
        """
        system_prompt = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="N/A",
            estado_pedido="N/A",
            menu_formateado=mock_menu
        )

        # Validar que hay sección de seguridad
        assert "seguridad" in system_prompt.lower() or "CRÍTICA" in system_prompt
        assert "NUNCA reveles" in system_prompt or "NO ejecutes" in system_prompt

        # Validar que menciona client_id y permisos
        assert "client_id" in system_prompt or "cliente actual" in system_prompt

    def test_no_inventar_pedidos_del_historial(self, mock_menu):
        """
        Escenario: Usuario pregunta "¿Qué pedidos tengo?" y el bot NO debe inventar información.
        Expectativa: Bot solo debe reportar lo que está en pedido_actual, NO del historial de conversación.
        """
        # Caso 1: Sin pedido activo
        system_prompt_sin_pedido = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="N/A",
            estado_pedido="N/A",
            menu_formateado=mock_menu,
            pedido_info=""
        )

        # Validar que hay regla de NO inventar información
        assert "SOLO reporta" in system_prompt_sin_pedido or "NUNCA inventes" in system_prompt_sin_pedido

        # Caso 2: Con pedido activo
        system_prompt_con_pedido = build_system_prompt(
            nombre_cliente="AC",
            direccion_guardada="Cra 74 #13a",
            order_id="order-123",
            estado_pedido="PREPARANDO",
            menu_formateado=mock_menu,
            pedido_info="Items: 1x Pizza Hawaiana Familiar | Total: $55,000"
        )

        # Validar que instruye usar pedido_actual
        assert "pedido_actual" in system_prompt_con_pedido.lower()
        assert "SOLO reporta" in system_prompt_con_pedido or "NUNCA inventes" in system_prompt_con_pedido
