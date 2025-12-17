"""
Billing Service
Handles cost calculation and payment processing for charging sessions.
"""

from datetime import datetime
from typing import Dict
from models.vehicle import Vehicle, VehicleType


class Invoice:
    """Represents a billing invoice for a charging session."""

    def __init__(
        self,
        invoice_id: str,
        vehicle_id: str,
        charging_duration: float,
        power_consumed: float,
        total_cost: float,
    ):
        """
        Initialize an invoice.

        Args:
            invoice_id: Unique identifier for the invoice
            vehicle_id: ID of the vehicle that was charged
            charging_duration: Duration of charging in hours
            power_consumed: Total power consumed in kWh
            total_cost: Total cost in currency units
        """
        self.invoice_id = invoice_id
        self.vehicle_id = vehicle_id
        self.charging_duration = charging_duration
        self.power_consumed = power_consumed
        self.total_cost = total_cost
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        """Convert invoice to dictionary format."""
        return {
            "invoice_id": self.invoice_id,
            "vehicle_id": self.vehicle_id,
            "charging_duration_hours": round(self.charging_duration, 2),
            "power_consumed_kwh": round(self.power_consumed, 2),
            "total_cost": round(self.total_cost, 2),
            "timestamp": self.timestamp.isoformat(),
        }

    def __str__(self) -> str:
        """String representation of the invoice."""
        return (
            f"Invoice {self.invoice_id}: Vehicle {self.vehicle_id}, "
            f"${self.total_cost:.2f}"
        )


class BillingService:
    """
    Service for calculating charging costs and processing payments.
    Implements different pricing strategies based on vehicle type and time.
    """

    def __init__(self):
        """Initialize the billing service with default pricing configuration."""
        self._invoice_counter = 0

        # Pricing configuration (per kWh)
        self.pricing_config: Dict[VehicleType, float] = {
            VehicleType.SEDAN: 0.30,  # $0.30 per kWh
            VehicleType.SUV: 0.32,    # $0.32 per kWh
            VehicleType.TRUCK: 0.35,  # $0.35 per kWh
            VehicleType.BUS: 0.28,    # $0.28 per kWh (fleet discount)
        }

        # Base connection fee (per session)
        self.connection_fee = 2.00

        # Peak hour multiplier (6 AM - 10 PM)
        self.peak_hour_multiplier = 1.2

        # Total revenue tracking
        self.total_revenue = 0.0

    def calculate_cost(
        self,
        vehicle: Vehicle,
        duration: float,
        power_consumed: float,
        is_peak_hour: bool = False,
    ) -> float:
        """
        Calculate the total cost for a charging session.

        Args:
            vehicle: Vehicle that was charged
            duration: Charging duration in hours
            power_consumed: Total power consumed in kWh
            is_peak_hour: Whether charging occurred during peak hours

        Returns:
            Total cost in currency units
        """
        # Base cost: power consumed * rate per kWh
        base_rate = self.pricing_config.get(vehicle.vehicle_type, 0.30)
        power_cost = power_consumed * base_rate

        # Apply peak hour multiplier if applicable
        if is_peak_hour:
            power_cost *= self.peak_hour_multiplier

        # Add connection fee
        total_cost = power_cost + self.connection_fee

        # Apply reservation discount (5% off)
        if vehicle.has_reservation:
            total_cost *= 0.95

        return round(total_cost, 2)

    def generate_invoice(
        self,
        vehicle: Vehicle,
        duration: float,
        power_consumed: float,
        is_peak_hour: bool = False,
    ) -> Invoice:
        """
        Generate an invoice for a charging session.

        Args:
            vehicle: Vehicle that was charged
            duration: Charging duration in hours
            power_consumed: Total power consumed in kWh
            is_peak_hour: Whether charging occurred during peak hours

        Returns:
            Invoice object
        """
        total_cost = self.calculate_cost(vehicle, duration, power_consumed, is_peak_hour)

        self._invoice_counter += 1
        invoice_id = f"INV-{self._invoice_counter:06d}"

        invoice = Invoice(
            invoice_id=invoice_id,
            vehicle_id=vehicle.vehicle_id,
            charging_duration=duration,
            power_consumed=power_consumed,
            total_cost=total_cost,
        )

        print(f"[BillingService] Generated {invoice}")
        return invoice

    def process_payment(self, vehicle: Vehicle, amount: float) -> bool:
        """
        Process payment for a charging session.

        Args:
            vehicle: Vehicle making the payment
            amount: Payment amount

        Returns:
            True if payment successful, False otherwise
        """
        # Simulate payment processing
        # In a real system, this would integrate with a payment gateway

        if amount <= 0:
            print(f"[BillingService] Payment failed: Invalid amount ${amount:.2f}")
            return False

        # Simulate successful payment
        self.total_revenue += amount
        print(
            f"[BillingService] Payment processed: ${amount:.2f} from {vehicle.vehicle_id}"
        )
        return True

    def update_pricing(self, vehicle_type: VehicleType, new_rate: float) -> None:
        """
        Update pricing for a specific vehicle type.

        Args:
            vehicle_type: Vehicle type to update
            new_rate: New rate per kWh
        """
        old_rate = self.pricing_config.get(vehicle_type, 0.0)
        self.pricing_config[vehicle_type] = new_rate
        print(
            f"[BillingService] Updated {vehicle_type.display_name} rate: "
            f"${old_rate:.2f} -> ${new_rate:.2f} per kWh"
        )

    def get_revenue_stats(self) -> dict:
        """
        Get revenue statistics.

        Returns:
            Dictionary containing revenue information
        """
        return {
            "total_revenue": round(self.total_revenue, 2),
            "invoices_generated": self._invoice_counter,
            "average_per_invoice": (
                round(self.total_revenue / self._invoice_counter, 2)
                if self._invoice_counter > 0
                else 0.0
            ),
        }

    def display_pricing(self) -> None:
        """Display current pricing configuration."""
        print("\n" + "=" * 60)
        print("BILLING SERVICE - PRICING CONFIGURATION")
        print("=" * 60)
        print(f"Connection Fee: ${self.connection_fee:.2f}")
        print(f"Peak Hour Multiplier: {self.peak_hour_multiplier}x")
        print("\nRates per kWh:")
        for vehicle_type, rate in self.pricing_config.items():
            print(f"  {vehicle_type.display_name}: ${rate:.2f}")
        print("\nDiscounts:")
        print("  Reservation: 5% off total")
        print("=" * 60 + "\n")

    def __str__(self) -> str:
        """String representation of the billing service."""
        return f"BillingService(revenue=${self.total_revenue:.2f})"

    def __repr__(self) -> str:
        """Detailed representation of the billing service."""
        return self.__str__()
