"""
Unit tests for BillingService.
Tests cost calculation, invoice generation, and payment processing.
"""

import pytest
import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from models.vehicle import Vehicle, VehicleType
from services.billing_service import BillingService, Invoice


class TestBillingService:
    """Test suite for BillingService class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.billing_service = BillingService()

    def test_initialization(self):
        """Test billing service initialization."""
        assert self.billing_service.connection_fee == 2.00
        assert self.billing_service.peak_hour_multiplier == 1.2
        assert self.billing_service.total_revenue == 0.0
        assert VehicleType.SEDAN in self.billing_service.pricing_config

    def test_calculate_cost_sedan(self):
        """Test cost calculation for sedan."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        cost = self.billing_service.calculate_cost(
            vehicle,
            duration=1.0,
            power_consumed=20.0,
            is_peak_hour=False
        )

        # 20 kWh * $0.30 + $2.00 connection fee = $8.00
        assert cost == 8.00

    def test_calculate_cost_peak_hour(self):
        """Test cost calculation during peak hours."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        cost = self.billing_service.calculate_cost(
            vehicle,
            duration=1.0,
            power_consumed=20.0,
            is_peak_hour=True
        )

        # (20 kWh * $0.30 * 1.2) + $2.00 = $9.20
        assert cost == 9.20

    def test_calculate_cost_with_reservation(self):
        """Test cost calculation with reservation discount."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0, has_reservation=True)
        cost = self.billing_service.calculate_cost(
            vehicle,
            duration=1.0,
            power_consumed=20.0,
            is_peak_hour=False
        )

        # ($6.00 + $2.00) * 0.95 (5% discount) = $7.60
        assert cost == 7.60

    def test_calculate_cost_different_vehicle_types(self):
        """Test cost calculation for different vehicle types."""
        sedan = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        suv = Vehicle("AV-002", VehicleType.SUV, 80.0, 40.0)
        truck = Vehicle("AV-003", VehicleType.TRUCK, 100.0, 50.0)
        bus = Vehicle("AV-004", VehicleType.BUS, 150.0, 75.0)

        power = 10.0
        sedan_cost = self.billing_service.calculate_cost(sedan, 1.0, power)
        suv_cost = self.billing_service.calculate_cost(suv, 1.0, power)
        truck_cost = self.billing_service.calculate_cost(truck, 1.0, power)
        bus_cost = self.billing_service.calculate_cost(bus, 1.0, power)

        # Different rates should result in different costs
        assert sedan_cost != suv_cost
        assert suv_cost != truck_cost
        assert truck_cost > bus_cost  # Bus has fleet discount

    def test_generate_invoice(self):
        """Test invoice generation."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        invoice = self.billing_service.generate_invoice(
            vehicle,
            duration=1.5,
            power_consumed=25.0,
            is_peak_hour=False
        )

        assert isinstance(invoice, Invoice)
        assert invoice.vehicle_id == "AV-001"
        assert invoice.charging_duration == 1.5
        assert invoice.power_consumed == 25.0
        assert invoice.total_cost > 0
        assert invoice.invoice_id.startswith("INV-")

    def test_process_payment_success(self):
        """Test successful payment processing."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        result = self.billing_service.process_payment(vehicle, 10.00)

        assert result is True
        assert self.billing_service.total_revenue == 10.00

    def test_process_payment_invalid_amount(self):
        """Test payment processing with invalid amount."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        result = self.billing_service.process_payment(vehicle, 0.00)

        assert result is False
        assert self.billing_service.total_revenue == 0.00

    def test_process_multiple_payments(self):
        """Test processing multiple payments."""
        vehicle1 = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        vehicle2 = Vehicle("AV-002", VehicleType.SUV, 80.0, 40.0)

        self.billing_service.process_payment(vehicle1, 10.00)
        self.billing_service.process_payment(vehicle2, 15.00)

        assert self.billing_service.total_revenue == 25.00

    def test_update_pricing(self):
        """Test updating pricing for a vehicle type."""
        old_rate = self.billing_service.pricing_config[VehicleType.SEDAN]
        new_rate = 0.35

        self.billing_service.update_pricing(VehicleType.SEDAN, new_rate)

        assert self.billing_service.pricing_config[VehicleType.SEDAN] == new_rate
        assert self.billing_service.pricing_config[VehicleType.SEDAN] != old_rate

    def test_get_revenue_stats(self):
        """Test getting revenue statistics."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)

        # Generate some invoices
        self.billing_service.generate_invoice(vehicle, 1.0, 20.0)
        self.billing_service.process_payment(vehicle, 8.00)

        self.billing_service.generate_invoice(vehicle, 1.0, 20.0)
        self.billing_service.process_payment(vehicle, 8.00)

        stats = self.billing_service.get_revenue_stats()

        assert stats["total_revenue"] == 16.00
        assert stats["invoices_generated"] == 2
        assert stats["average_per_invoice"] == 8.00

    def test_invoice_to_dict(self):
        """Test converting invoice to dictionary."""
        invoice = Invoice("INV-001", "AV-001", 1.5, 25.0, 10.50)
        invoice_dict = invoice.to_dict()

        assert invoice_dict["invoice_id"] == "INV-001"
        assert invoice_dict["vehicle_id"] == "AV-001"
        assert invoice_dict["charging_duration_hours"] == 1.5
        assert invoice_dict["power_consumed_kwh"] == 25.0
        assert invoice_dict["total_cost"] == 10.50
        assert "timestamp" in invoice_dict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
