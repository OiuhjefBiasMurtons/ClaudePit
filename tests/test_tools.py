import pytest
from unittest.mock import patch, MagicMock
from app.utils import format_menu_for_ai, generate_ticket_id
from app.tools import create_new_order


class TestFormatMenu:
    def test_format_menu_empty(self):
        """Verifica que retorna array vacío cuando no hay productos."""
        result = format_menu_for_ai([])
        assert result == "[]"

    def test_format_menu_single_product(self):
        """Verifica formateo de un producto con una variante como JSON."""
        import json
        menu_items = [
            {
                "producto": "Pizza Pepperoni",
                "description": "Pizza clásica con pepperoni",
                "food_type": "Pizza",
                "size": "Personal",
                "price": 15000,
                "id": "uuid-123"
            }
        ]
        result = format_menu_for_ai(menu_items)
        parsed = json.loads(result)

        assert len(parsed) == 1
        assert parsed[0]["name"] == "Pizza Pepperoni"
        assert parsed[0]["ingredients"] == "Pizza clásica con pepperoni"
        assert parsed[0]["category"] == "Pizza"
        assert len(parsed[0]["sizes"]) == 1
        assert parsed[0]["sizes"][0]["size"] == "Personal"
        assert parsed[0]["sizes"][0]["price"] == 15000
        assert parsed[0]["sizes"][0]["id"] == "uuid-123"

    def test_format_menu_multiple_variants(self):
        """Verifica formateo de producto con múltiples variantes como JSON."""
        import json
        menu_items = [
            {
                "producto": "Pizza Hawaiana",
                "description": "Con piña y jamón",
                "food_type": "Pizza",
                "size": "Personal",
                "price": 15000,
                "id": "uuid-1"
            },
            {
                "producto": "Pizza Hawaiana",
                "description": "Con piña y jamón",
                "food_type": "Pizza",
                "size": "Mediana",
                "price": 25000,
                "id": "uuid-2"
            }
        ]
        result = format_menu_for_ai(menu_items)
        parsed = json.loads(result)

        # Debe haber un solo producto con 2 tamaños
        assert len(parsed) == 1
        assert parsed[0]["name"] == "Pizza Hawaiana"
        assert len(parsed[0]["sizes"]) == 2
        # Ordenados por precio
        assert parsed[0]["sizes"][0]["price"] == 15000
        assert parsed[0]["sizes"][1]["price"] == 25000


class TestGenerateTicketId:
    def test_generate_ticket_id_format(self):
        """Verifica que el ticket ID tiene el formato correcto TDP-YYYYMMDD-NNN."""
        ticket_id = generate_ticket_id()

        assert ticket_id.startswith("TDP-")
        parts = ticket_id.split("-")
        assert len(parts) == 3
        assert len(parts[1]) == 8  # YYYYMMDD
        assert len(parts[2]) == 3  # NNN
        assert parts[1].isdigit()
        assert parts[2].isdigit()

    def test_generate_ticket_id_unique(self):
        """Verifica que genera IDs diferentes."""
        ids = [generate_ticket_id() for _ in range(10)]
        # Al menos algunos deberían ser diferentes (por el random)
        assert len(set(ids)) > 1


class TestCreateOrder:
    @patch("app.tools.get_supabase_client")
    @patch("app.tools.generate_ticket_id")
    def test_create_order_basic(self, mock_ticket_id, mock_supabase):
        """Verifica que create_new_order crea un pedido correctamente."""
        # Setup mocks
        mock_ticket_id.return_value = "TDP-20250120-001"

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock para validación de variant_ids, barrios, etc.
        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == "product_variants":
                # Mock para validación - retorna que el variant_id existe
                mock_table.select.return_value.in_.return_value.execute.return_value.data = [
                    {"id": "variant-1"}
                ]
            elif table_name == "barrios":
                # Mock para búsqueda de barrio
                mock_table.select.return_value.ilike.return_value.eq.return_value.execute.return_value.data = [
                    {"id": "barrio-uuid-1", "nombre": "Laureles", "precio_domicilio": 5000}
                ]
            elif table_name == "orders":
                # Mock para insert y select de orders
                mock_table.insert.return_value.execute.return_value.data = [
                    {"id": "order-uuid-123"}
                ]
                mock_table.select.return_value.eq.return_value.execute.return_value.data = [
                    {"id": "order-uuid-123", "total_order": 40000, "ticket_id": "TDP-20250120-001", "precio_domicilio": 5000}
                ]
            elif table_name == "order_details":
                mock_table.insert.return_value.execute.return_value.data = [{}]
            return mock_table

        mock_client.table.side_effect = table_side_effect

        # Execute
        result = create_new_order(
            client_id="client-uuid",
            items=[
                {"variant_id": "variant-1", "quantity": 2, "note": "sin cebolla"}
            ],
            delivery_address="Calle 123",
            barrio="Laureles"
        )

        # Verify
        assert result["order_id"] == "order-uuid-123"
        assert result["ticket_id"] == "TDP-20250120-001"
        assert result["subtotal"] == 40000
        assert result["precio_domicilio"] == 5000
        assert result["total"] == 45000
        assert result["address"] == "Calle 123"
        assert result["barrio"] == "Laureles"

        # Verify table calls
        assert mock_client.table.called

    @patch("app.tools.get_supabase_client")
    def test_create_order_invalid_barrio(self, mock_supabase):
        """Verifica que create_new_order rechaza barrios sin cobertura."""
        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock: barrio no encontrado
        mock_table = MagicMock()
        mock_table.select.return_value.ilike.return_value.eq.return_value.execute.return_value.data = []
        mock_client.table.return_value = mock_table

        result = create_new_order(
            client_id="client-uuid",
            items=[{"variant_id": "variant-1", "quantity": 1}],
            delivery_address="Calle 123",
            barrio="BarrioInexistente"
        )

        assert "error" in result
        assert "cobertura" in result["error"].lower()

    def test_create_order_missing_barrio(self):
        """Verifica que create_new_order rechaza pedidos sin barrio."""
        result = create_new_order(
            client_id="client-uuid",
            items=[{"variant_id": "variant-1", "quantity": 1}],
            delivery_address="Calle 123",
            barrio=""
        )

        assert "error" in result


class TestSecurityValidation:
    """Tests de validación de seguridad (client_id ownership)"""

    @patch("app.tools.get_supabase_client")
    def test_add_items_rejects_wrong_client(self, mock_supabase):
        """Verifica que add_items_to_order rechaza pedidos de otros clientes"""
        from app.tools import add_items_to_order

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock: el pedido pertenece a otro cliente
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value.data = [
            {"client_id": "other-client-uuid"}
        ]
        mock_client.table.return_value = mock_table

        # Ejecutar
        result = add_items_to_order(
            order_id="order-123",
            items=[{"variant_id": "variant-1", "quantity": 1}],
            client_id="my-client-uuid"
        )

        # Verificar que retorna error
        assert "error" in result
        assert "No tienes permiso" in result["error"]

    @patch("app.tools.get_supabase_client")
    def test_replace_item_rejects_wrong_client(self, mock_supabase):
        """Verifica que replace_item_in_order rechaza pedidos de otros clientes"""
        from app.tools import replace_item_in_order

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock: el pedido pertenece a otro cliente
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value.data = [
            {"client_id": "other-client-uuid"}
        ]
        mock_client.table.return_value = mock_table

        # Ejecutar
        result = replace_item_in_order(
            order_id="order-123",
            old_variant_id="old-variant",
            new_variant_id="new-variant",
            client_id="my-client-uuid"
        )

        # Verificar que retorna error
        assert "error" in result
        assert "No tienes permiso" in result["error"]

    @patch("app.tools.get_supabase_client")
    def test_update_address_rejects_wrong_client(self, mock_supabase):
        """Verifica que update_order_address rechaza pedidos de otros clientes"""
        from app.tools import update_order_address

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock: el pedido pertenece a otro cliente
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value.data = [
            {"client_id": "other-client-uuid"}
        ]
        mock_client.table.return_value = mock_table

        # Ejecutar
        result = update_order_address(
            order_id="order-123",
            new_address="Nueva direccion",
            client_id="my-client-uuid"
        )

        # Verificar que retorna error
        assert "error" in result
        assert "No tienes permiso" in result["error"]

    @patch("app.tools.get_supabase_client")
    def test_confirm_order_rejects_wrong_client(self, mock_supabase):
        """Verifica que confirm_order rechaza pedidos de otros clientes"""
        from app.tools import confirm_order

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock: el pedido pertenece a otro cliente
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value.data = [
            {"client_id": "other-client-uuid"}
        ]
        mock_client.table.return_value = mock_table

        # Ejecutar
        result = confirm_order(
            order_id="order-123",
            client_id="my-client-uuid"
        )

        # Verificar que retorna error
        assert "error" in result
        assert "No tienes permiso" in result["error"]

    @patch("app.tools.get_supabase_client")
    def test_cancel_order_rejects_wrong_client(self, mock_supabase):
        """Verifica que cancel_order rechaza pedidos de otros clientes"""
        from app.tools import cancel_order

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock: el pedido pertenece a otro cliente
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value.data = [
            {"client_id": "other-client-uuid"}
        ]
        mock_client.table.return_value = mock_table

        # Ejecutar
        result = cancel_order(
            order_id="order-123",
            client_id="my-client-uuid"
        )

        # Verificar que retorna error
        assert "error" in result
        assert "No tienes permiso" in result["error"]


class TestGetClientOrders:
    """Tests para la función get_client_orders"""

    @patch("app.tools.get_supabase_client")
    def test_get_client_orders_sin_pedidos(self, mock_supabase):
        """Verifica que retorna lista vacía cuando el cliente no tiene pedidos"""
        from app.tools import get_client_orders

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock: sin pedidos
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.in_.return_value.order.return_value.limit.return_value.execute.return_value.data = []
        mock_client.table.return_value = mock_table

        # Ejecutar
        result = get_client_orders(client_id="client-uuid")

        # Verificar
        assert result["count"] == 0
        assert result["orders"] == []
        assert "No tienes pedidos" in result["message"]

    @patch("app.tools.get_supabase_client")
    def test_get_client_orders_con_pedidos_activos(self, mock_supabase):
        """Verifica que retorna pedidos activos correctamente"""
        from app.tools import get_client_orders

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock de pedidos
        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == "orders":
                mock_table.select.return_value.eq.return_value.in_.return_value.order.return_value.limit.return_value.execute.return_value.data = [
                    {
                        "id": "order-123",
                        "ticket_id": "TDP-20250205-001",
                        "state": "PREPARANDO",
                        "total_order": 55000,
                        "address_delivery": "Cra 74 #120-39",
                        "payment_method": "efectivo",
                        "created_at": "2025-02-05T23:00:00"
                    }
                ]
            elif table_name == "order_details":
                mock_table.select.return_value.eq.return_value.execute.return_value.data = [
                    {
                        "quantity": 1,
                        "product_variants": {
                            "nombre_variante": "Familiar",
                            "price": 55000,
                            "products": {"name": "Pizza Hawaiana"}
                        }
                    }
                ]
            return mock_table

        mock_client.table.side_effect = table_side_effect

        # Ejecutar
        result = get_client_orders(client_id="client-uuid")

        # Verificar
        assert result["count"] == 1
        assert len(result["orders"]) == 1
        assert result["orders"][0]["order_id"] == "order-123"
        assert result["orders"][0]["state"] == "PREPARANDO"
        assert result["orders"][0]["total"] == 55000
        assert len(result["orders"][0]["items"]) == 1

    @patch("app.tools.get_supabase_client")
    def test_get_client_orders_filtra_quantity_negativa(self, mock_supabase):
        """Verifica que filtra items con quantity <= 0"""
        from app.tools import get_client_orders

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock con item corrupto
        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == "orders":
                mock_table.select.return_value.eq.return_value.in_.return_value.order.return_value.limit.return_value.execute.return_value.data = [
                    {
                        "id": "order-123",
                        "ticket_id": "TDP-20250205-001",
                        "state": "PREPARANDO",
                        "total_order": 55000,
                        "address_delivery": "Cra 74",
                        "payment_method": "efectivo",
                        "created_at": "2025-02-05T23:00:00"
                    }
                ]
            elif table_name == "order_details":
                mock_table.select.return_value.eq.return_value.execute.return_value.data = [
                    {
                        "quantity": -1,  # Corrupto
                        "product_variants": {
                            "nombre_variante": "Familiar",
                            "price": 55000,
                            "products": {"name": "Pizza Hawaiana"}
                        }
                    },
                    {
                        "quantity": 1,  # Válido
                        "product_variants": {
                            "nombre_variante": "Personal",
                            "price": 22000,
                            "products": {"name": "Pizza Margarita"}
                        }
                    }
                ]
            return mock_table

        mock_client.table.side_effect = table_side_effect

        # Ejecutar
        result = get_client_orders(client_id="client-uuid")

        # Verificar que solo retorna el item válido
        assert result["count"] == 1
        assert len(result["orders"][0]["items"]) == 1
        assert result["orders"][0]["items"][0]["product_name"] == "Pizza Margarita"

    @patch("app.tools.get_supabase_client")
    def test_get_client_orders_include_completed(self, mock_supabase):
        """Verifica que puede incluir pedidos completados"""
        from app.tools import get_client_orders

        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Mock con pedido entregado
        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == "orders":
                # Mock para include_completed=True (sin filtro de estado)
                mock_table.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value.data = [
                    {
                        "id": "order-456",
                        "ticket_id": "TDP-20250204-001",
                        "state": "ENTREGADO",
                        "total_order": 30000,
                        "address_delivery": "Cra 73",
                        "payment_method": "transferencia",
                        "created_at": "2025-02-04T20:00:00"
                    }
                ]
            elif table_name == "order_details":
                mock_table.select.return_value.eq.return_value.execute.return_value.data = []
            return mock_table

        mock_client.table.side_effect = table_side_effect

        # Ejecutar con include_completed=True
        result = get_client_orders(client_id="client-uuid", include_completed=True)

        # Verificar
        assert result["count"] == 1
        assert result["orders"][0]["state"] == "ENTREGADO"
