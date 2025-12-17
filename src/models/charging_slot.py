"""
Charging Slot Model
Represents a physical charging slot at the station.
"""

from datetime import datetime
from typing import Optional
from models.vehicle import Vehicle


class ChargingSlot:
    """
    Represents a physical charging slot that can charge one vehicle at a time.
    """

    def __init__(self, slot_id: str, power_rating: float):
        """
        Initialize a charging slot.

        Args:
            slot_id: Unique identifier for the slot
            power_rating: Maximum charging power in kW
        """
        self.slot_id = slot_id
        self.power_rating = power_rating
        self.is_available = True
        self.current_vehicle: Optional[Vehicle] = None
        self.charging_start_time: Optional[datetime] = None
        self.total_power_consumed = 0.0

    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        """
        Assign a vehicle to this charging slot.

        Args:
            vehicle: Vehicle to assign to this slot

        Returns:
            True if assignment successful, False if slot is occupied
        """
        if not self.is_available:
            return False

        self.current_vehicle = vehicle
        self.is_available = False
        self.charging_start_time = datetime.now()
        vehicle.charging_start_time = self.charging_start_time

        print(f"[Slot {self.slot_id}] Assigned to {vehicle.vehicle_id}")
        return True

    def release_vehicle(self) -> Optional[Vehicle]:
        """
        Release the vehicle from this charging slot.

        Returns:
            The vehicle that was charging, or None if slot was empty
        """
        if self.current_vehicle is None:
            return None

        vehicle = self.current_vehicle
        vehicle.charging_end_time = datetime.now()

        print(
            f"[Slot {self.slot_id}] Released {vehicle.vehicle_id} "
            f"after {self.get_charging_duration():.2f} hours"
        )

        self.current_vehicle = None
        self.is_available = True
        self.charging_start_time = None

        return vehicle

    def get_charging_duration(self) -> float:
        """
        Get the duration the current vehicle has been charging.

        Returns:
            Charging duration in hours, or 0.0 if no vehicle is charging
        """
        if self.charging_start_time is None:
            return 0.0

        duration = datetime.now() - self.charging_start_time
        return duration.total_seconds() / 3600  # Convert to hours

    def simulate_charging(self, duration_hours: float) -> float:
        """
        Simulate charging for a given duration and calculate power consumed.

        Args:
            duration_hours: Duration to charge in hours

        Returns:
            Power consumed in kWh
        """
        if self.current_vehicle is None:
            return 0.0

        # Power consumed = power rating * time
        power_consumed = min(
            self.power_rating * duration_hours,
            self.current_vehicle.get_required_charge()
        )

        self.current_vehicle.update_charge(power_consumed)
        self.total_power_consumed += power_consumed

        return power_consumed

    def is_charging_complete(self) -> bool:
        """
        Check if the current vehicle's charging is complete.

        Returns:
            True if vehicle is fully charged or no vehicle is present
        """
        if self.current_vehicle is None:
            return True

        return self.current_vehicle.get_charge_percentage() >= 99.0

    def get_status(self) -> dict:
        """
        Get detailed status of the charging slot.

        Returns:
            Dictionary containing slot status information
        """
        status = {
            "slot_id": self.slot_id,
            "power_rating": self.power_rating,
            "is_available": self.is_available,
            "total_power_consumed": self.total_power_consumed,
        }

        if self.current_vehicle:
            status["current_vehicle"] = self.current_vehicle.vehicle_id
            status["charging_duration"] = self.get_charging_duration()
            status["vehicle_charge_percentage"] = self.current_vehicle.get_charge_percentage()

        return status

    def __str__(self) -> str:
        """String representation of the charging slot."""
        status = "Available" if self.is_available else f"Occupied by {self.current_vehicle.vehicle_id}"
        return f"Slot {self.slot_id} ({self.power_rating}kW): {status}"

    def __repr__(self) -> str:
        """Detailed representation of the charging slot."""
        return self.__str__()
