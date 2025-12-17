"""
Unit tests for ChargingStation.
Tests station management, slot allocation, and Observer pattern.
"""

import pytest
import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from models.vehicle import Vehicle, VehicleType
from models.charging_slot import ChargingSlot
from models.charging_station import ChargingStation
from services.notification_service import NotificationService


class TestChargingStation:
    """Test suite for ChargingStation class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.station = ChargingStation("CS-001", "Test Location")
        self.station.add_slot(ChargingSlot("SLOT-A", 50.0))
        self.station.add_slot(ChargingSlot("SLOT-B", 50.0))

    def test_initialization(self):
        """Test charging station initialization."""
        assert self.station.station_id == "CS-001"
        assert self.station.location == "Test Location"
        assert len(self.station.slots) == 2
        assert self.station.total_vehicles_served == 0

    def test_add_slot(self):
        """Test adding a charging slot."""
        initial_count = len(self.station.slots)
        self.station.add_slot(ChargingSlot("SLOT-C", 150.0))

        assert len(self.station.slots) == initial_count + 1

    def test_get_available_slots(self):
        """Test getting available slots."""
        available = self.station.get_available_slots()
        assert len(available) == 2

        # Occupy one slot
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        self.station.assign_vehicle_to_slot(vehicle)

        available = self.station.get_available_slots()
        assert len(available) == 1

    def test_get_occupied_slots(self):
        """Test getting occupied slots."""
        occupied = self.station.get_occupied_slots()
        assert len(occupied) == 0

        # Occupy one slot
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        self.station.assign_vehicle_to_slot(vehicle)

        occupied = self.station.get_occupied_slots()
        assert len(occupied) == 1

    def test_assign_vehicle_to_slot(self):
        """Test assigning a vehicle to a slot."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        slot = self.station.assign_vehicle_to_slot(vehicle)

        assert slot is not None
        assert slot.current_vehicle == vehicle
        assert slot.is_available is False

    def test_assign_vehicle_no_slots_available(self):
        """Test assigning vehicle when no slots are available."""
        vehicle1 = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        vehicle2 = Vehicle("AV-002", VehicleType.SEDAN, 60.0, 30.0)
        vehicle3 = Vehicle("AV-003", VehicleType.SEDAN, 60.0, 30.0)

        # Fill all slots
        self.station.assign_vehicle_to_slot(vehicle1)
        self.station.assign_vehicle_to_slot(vehicle2)

        # Try to assign third vehicle
        slot = self.station.assign_vehicle_to_slot(vehicle3)
        assert slot is None

    def test_release_vehicle(self):
        """Test releasing a vehicle from a slot."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        slot = self.station.assign_vehicle_to_slot(vehicle)

        released = self.station.release_vehicle(slot)

        assert released == vehicle
        assert slot.is_available is True
        assert slot.current_vehicle is None
        assert self.station.total_vehicles_served == 1

    def test_release_vehicle_empty_slot(self):
        """Test releasing vehicle from empty slot."""
        slot = self.station.slots[0]
        released = self.station.release_vehicle(slot)

        assert released is None
        assert self.station.total_vehicles_served == 0

    def test_process_charging(self):
        """Test processing charging for all occupied slots."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 10.0)
        slot = self.station.assign_vehicle_to_slot(vehicle)

        initial_charge = vehicle.current_charge
        self.station.process_charging(duration_hours=0.5)

        assert vehicle.current_charge > initial_charge

    def test_observer_pattern_attach(self):
        """Test attaching observers to the station."""
        notification_service = NotificationService("NS-001")
        initial_count = len(self.station._observers)

        self.station.attach(notification_service)

        assert len(self.station._observers) == initial_count + 1

    def test_observer_pattern_detach(self):
        """Test detaching observers from the station."""
        notification_service = NotificationService("NS-001")
        self.station.attach(notification_service)

        initial_count = len(self.station._observers)
        self.station.detach(notification_service)

        assert len(self.station._observers) == initial_count - 1

    def test_observer_pattern_notify(self):
        """Test notifying observers."""
        notification_service = NotificationService("NS-001")
        self.station.attach(notification_service)

        initial_notifications = notification_service.get_notification_count()
        self.station.notify("Test message")

        assert notification_service.get_notification_count() > initial_notifications

    def test_get_station_status(self):
        """Test getting station status."""
        status = self.station.get_station_status()

        assert status["station_id"] == "CS-001"
        assert status["location"] == "Test Location"
        assert status["total_slots"] == 2
        assert status["available_slots"] == 2
        assert status["occupied_slots"] == 0
        assert status["utilization_rate"] == 0

    def test_station_utilization_rate(self):
        """Test station utilization rate calculation."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        self.station.assign_vehicle_to_slot(vehicle)

        status = self.station.get_station_status()
        assert status["utilization_rate"] == 50.0  # 1 of 2 slots occupied

    def test_vehicle_added_as_observer(self):
        """Test that vehicle is added as observer when assigned."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        initial_observers = len(self.station._observers)

        self.station.assign_vehicle_to_slot(vehicle)

        assert len(self.station._observers) == initial_observers + 1

    def test_vehicle_removed_as_observer(self):
        """Test that vehicle is removed as observer when released."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        slot = self.station.assign_vehicle_to_slot(vehicle)

        initial_observers = len(self.station._observers)
        self.station.release_vehicle(slot)

        assert len(self.station._observers) == initial_observers - 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
