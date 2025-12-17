"""
Charging Station Model
Main class coordinating all charging operations.
Implements Subject in the Observer pattern.
"""

from typing import List, Optional
from datetime import datetime
from models.charging_slot import ChargingSlot
from models.vehicle import Vehicle
from patterns.observer import Subject


class ChargingStation(Subject):
    """
    Central charging station that manages slots, queue, and notifications.
    Implements Observer pattern to notify vehicles and services.
    """

    def __init__(self, station_id: str, location: str):
        """
        Initialize the charging station.

        Args:
            station_id: Unique identifier for the station
            location: Physical location of the station
        """
        super().__init__()
        self.station_id = station_id
        self.location = location
        self.slots: List[ChargingSlot] = []
        self.total_vehicles_served = 0
        self.total_revenue = 0.0
        self.created_at = datetime.now()

    def add_slot(self, slot: ChargingSlot) -> None:
        """
        Add a charging slot to the station.

        Args:
            slot: ChargingSlot to add
        """
        self.slots.append(slot)
        print(f"[Station {self.station_id}] Added slot {slot.slot_id}")

    def get_available_slots(self) -> List[ChargingSlot]:
        """
        Get list of available charging slots.

        Returns:
            List of available ChargingSlot objects
        """
        return [slot for slot in self.slots if slot.is_available]

    def get_occupied_slots(self) -> List[ChargingSlot]:
        """
        Get list of occupied charging slots.

        Returns:
            List of occupied ChargingSlot objects
        """
        return [slot for slot in self.slots if not slot.is_available]

    def assign_vehicle_to_slot(self, vehicle: Vehicle) -> Optional[ChargingSlot]:
        """
        Assign a vehicle to an available slot.

        Args:
            vehicle: Vehicle to assign

        Returns:
            ChargingSlot if assignment successful, None otherwise
        """
        available_slots = self.get_available_slots()

        if not available_slots:
            self.notify(f"No slots available for vehicle {vehicle.vehicle_id}")
            return None

        # Assign to first available slot
        slot = available_slots[0]
        if slot.assign_vehicle(vehicle):
            self.attach(vehicle)  # Add vehicle as observer
            self.notify(
                f"Vehicle {vehicle.vehicle_id} assigned to slot {slot.slot_id}"
            )
            return slot

        return None

    def release_vehicle(self, slot: ChargingSlot) -> Optional[Vehicle]:
        """
        Release a vehicle from a charging slot.

        Args:
            slot: ChargingSlot to release

        Returns:
            Vehicle that was released, or None if slot was empty
        """
        vehicle = slot.release_vehicle()

        if vehicle:
            self.total_vehicles_served += 1
            self.notify(
                f"Vehicle {vehicle.vehicle_id} completed charging and released from slot {slot.slot_id}"
            )
            self.detach(vehicle)  # Remove vehicle as observer

        return vehicle

    def process_charging(self, duration_hours: float = 1.0) -> None:
        """
        Simulate charging process for all occupied slots.

        Args:
            duration_hours: Duration to simulate in hours
        """
        occupied_slots = self.get_occupied_slots()

        for slot in occupied_slots:
            power_consumed = slot.simulate_charging(duration_hours)
            vehicle = slot.current_vehicle

            if vehicle:
                charge_pct = vehicle.get_charge_percentage()
                self.notify(
                    f"Slot {slot.slot_id}: Vehicle {vehicle.vehicle_id} "
                    f"charged to {charge_pct:.1f}% ({power_consumed:.2f} kWh)"
                )

                # Check if charging is complete
                if slot.is_charging_complete():
                    self.notify(
                        f"Vehicle {vehicle.vehicle_id} charging complete!"
                    )

    def get_station_status(self) -> dict:
        """
        Get comprehensive station status.

        Returns:
            Dictionary containing station status information
        """
        total_slots = len(self.slots)
        available = len(self.get_available_slots())
        occupied = total_slots - available

        return {
            "station_id": self.station_id,
            "location": self.location,
            "total_slots": total_slots,
            "available_slots": available,
            "occupied_slots": occupied,
            "utilization_rate": (occupied / total_slots * 100) if total_slots > 0 else 0,
            "total_vehicles_served": self.total_vehicles_served,
            "total_revenue": self.total_revenue,
            "observers_count": len(self._observers),
        }

    def display_status(self) -> None:
        """Print the current status of the charging station."""
        status = self.get_station_status()
        print("\n" + "=" * 60)
        print(f"CHARGING STATION STATUS - {status['station_id']}")
        print("=" * 60)
        print(f"Location: {status['location']}")
        print(f"Total Slots: {status['total_slots']}")
        print(f"Available: {status['available_slots']} | Occupied: {status['occupied_slots']}")
        print(f"Utilization Rate: {status['utilization_rate']:.1f}%")
        print(f"Vehicles Served: {status['total_vehicles_served']}")
        print(f"Total Revenue: ${status['total_revenue']:.2f}")
        print(f"Active Observers: {status['observers_count']}")
        print("=" * 60)

        print("\nSlot Details:")
        for slot in self.slots:
            print(f"  {slot}")

        print("\n")

    def __str__(self) -> str:
        """String representation of the charging station."""
        return f"ChargingStation({self.station_id}, {self.location})"

    def __repr__(self) -> str:
        """Detailed representation of the charging station."""
        return self.__str__()
