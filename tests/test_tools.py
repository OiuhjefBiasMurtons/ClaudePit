import pytest
from unittest.mock import patch, MagicMock
from app.utils import format_menu_for_ai, generate_ticket_id
from app.tools import create_new_order


class TestFormatMenu:
    def test_format_menu_empty(self):
        """Verifica que retorna mensaje cuando no hay productos."""
        result = format_menu_for_ai([])
        assert result == "No hay productos disponibles."

    def test_format_menu_single_product(self):
        """Verifica formateo de un producto con una variante."""
        menu_items = [
            {
                "product_name": "Pizza Pepperoni",
                "product_description": "Pizza clásica con pepperoni",
                "variant_size": "Personal",
                "variant_price": 15.00,
                "variant_id": "uuid-123"
            }
        ]
        result = format_menu_for_ai(menu_items)

        assert "Pizza Pepperoni" in result
        assert "Pizza clásica con pepperoni" in result
        assert "Personal" in result
        assert "$15.00" in result
        assert "uuid-123" in result

    def test_format_menu_multiple_variants(self):
        """Verifica formateo de producto con múltiples variantes."""
        menu_items = [
            {
                "product_name": "Pizza Hawaiana",
                "product_description": "Con piña y jamón",
                "variant_size": "Personal",
                "variant_price": 15.00,
                "variant_id": "uuid-1"
            },
            {
                "product_name": "Pizza Hawaiana",
                "product_description": "Con piña y jamón",
                "variant_size": "Mediana",
                "variant_price": 25.00,
                "variant_id": "uuid-2"
            }
        ]
        result = format_menu_for_ai(menu_items)

        # Debe aparecer el nombre del producto una sola vez
        assert result.count("Pizza Hawaiana") == 1
        # Deben aparecer ambas variantes
        assert "Personal" in result
        assert "Mediana" in result
        assert "$15.00" in result
        assert "$25.00" in result


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

        # Mock insert order
        mock_client.table.return_value.insert.return_value.execute.return_value.data = [
            {"id": "order-uuid-123"}
        ]

        # Mock select updated order
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {"id": "order-uuid-123", "total_order": 40.00}
        ]

        # Execute
        result = create_new_order(
            client_id="client-uuid",
            items=[
                {"variant_id": "variant-1", "quantity": 2, "note": "sin cebolla"}
            ],
            delivery_address="Calle 123"
        )

        # Verify
        assert result["order_id"] == "order-uuid-123"
        assert result["ticket_id"] == "TDP-20250120-001"
        assert result["total"] == 40.00

        # Verify table calls
        assert mock_client.table.called
