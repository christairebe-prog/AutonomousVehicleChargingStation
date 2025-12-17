"""
Vehicle Model
Represents an autonomous vehicle that can charge at the station.
"""

from enum import Enum
from datetime import datetime
from typing import Optional
from patterns.observer import Observer


class VehicleType(Enum):
    """Enumeration of vehicle types with associated properties."""
    SEDAN = ("Sedan", 60.0, 1)
    SUV = ("SUV", 80.0, 1)
    TRUCK = ("Truck", 100.0, 2)
    BUS = ("Bus", 150.0, 3)

    def __init__(self, display_name: str, typical_capacity: float, priority_modifier: int):
        self.display_name = display_name
        self.typical_capacity = typical_capacity
        self.priority_modifier = priority_modifier


class Vehicle(Observer):
    """
    Represents an autonomous vehicle that needs charging.
    Implements Observer pattern to receive notifications from charging station.
    """

    def __init__(
        self,
        vehicle_id: str,
        vehicle_type: VehicleType,
        battery_capacity: float,
        current_charge: float,
        has_reservation: bool = False
    ):
        """
        Initialize a vehicle.

        Args:
            vehicle_id: Unique identifier for the vehicle
            vehicle_type: Type of vehicle (SEDAN, SUV, TRUCK, BUS)
            battery_capacity: Maximum battery capacity in kWh
            current_charge: Current charge level in kWh
            has_reservation: Whether the vehicle has a reservation
        """
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.battery_capacity = battery_capacity
        self.current_charge = current_charge
        self.has_reservation = has_reservation
        self.arrival_time: datetime = datetime.now()
        self.charging_start_time: Optional[datetime] = None
        self.charging_end_time: Optional[datetime] = None

    def get_required_charge(self) -> float:
        """
        Calculate the amount of charge needed to fill the battery.

        Returns:
            Required charge in kWh
        """
        return self.battery_capacity - self.current_charge

    def get_charge_percentage(self) -> float:
        """
        Get current charge level as a percentage.

        Returns:
            Charge percentage (0-100)
        """
        return (self.current_charge / self.battery_capacity) * 100

    def update_charge(self, amount: float) -> None:
        """
        Update the vehicle's charge level.

        Args:
            amount: Amount of charge to add in kWh
        """
        self.current_charge = min(self.current_charge + amount, self.battery_capacity)

    def calculate_priority(self) -> int:
        """
        Calculate priority score for queue management.
        Lower score = higher priority.

        Priority factors:
        - Reservation status (highest priority)
        - Battery level (lower charge = higher priority)
        - Vehicle type (larger vehicles get slight priority)

        Returns:
            Priority score
        """
        if self.has_reservation:
            return 0  # Highest priority

        # Lower charge percentage = higher priority
        charge_factor = int(self.get_charge_percentage())

        # Vehicle type modifier
        type_factor = self.vehicle_type.priority_modifier * 10

        return charge_factor + type_factor

    def update(self, message: str) -> None:
        """
        Receive notification from charging station.

        Args:
            message: Notification message
        """
        print(f"[Vehicle {self.vehicle_id}] Received notification: {message}")

    def __str__(self) -> str:
        """String representation of the vehicle."""
        return (
            f"Vehicle({self.vehicle_id}, {self.vehicle_type.display_name}, "
            f"Battery: {self.get_charge_percentage():.1f}%)"
        )

    def __repr__(self) -> str:
        """Detailed representation of the vehicle."""
        return self.__str__()

    def __lt__(self, other: 'Vehicle') -> bool:
        """
        Compare vehicles for priority queue ordering.

        Args:
            other: Another vehicle to compare

        Returns:
            True if this vehicle has higher priority (lower score)
        """
        return self.calculate_priority() < other.calculate_priority()
