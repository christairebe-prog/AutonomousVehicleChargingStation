"""
Unit tests for QueueManager service.
Tests priority queue functionality and vehicle management.
"""

import pytest
import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from models.vehicle import Vehicle, VehicleType
from services.queue_manager import QueueManager


class TestQueueManager:
    """Test suite for QueueManager class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.queue_manager = QueueManager()

    def test_initialization(self):
        """Test queue manager initialization."""
        assert self.queue_manager.get_queue_size() == 0
        assert self.queue_manager.is_empty() is True

    def test_add_vehicle(self):
        """Test adding a vehicle to the queue."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        position = self.queue_manager.add_vehicle(vehicle)

        assert position == 0
        assert self.queue_manager.get_queue_size() == 1
        assert self.queue_manager.is_empty() is False

    def test_priority_ordering(self):
        """Test that vehicles are ordered by priority."""
        # Create vehicles with different charge levels
        vehicle1 = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)  # 50% charge
        vehicle2 = Vehicle("AV-002", VehicleType.SEDAN, 60.0, 10.0)  # 16.7% charge - Higher priority
        vehicle3 = Vehicle("AV-003", VehicleType.SEDAN, 60.0, 50.0)  # 83.3% charge - Lower priority

        self.queue_manager.add_vehicle(vehicle1)
        self.queue_manager.add_vehicle(vehicle2)
        self.queue_manager.add_vehicle(vehicle3)

        # Vehicle with lowest charge should be first
        next_vehicle = self.queue_manager.get_next_vehicle()
        assert next_vehicle.vehicle_id == "AV-002"

        next_vehicle = self.queue_manager.get_next_vehicle()
        assert next_vehicle.vehicle_id == "AV-001"

        next_vehicle = self.queue_manager.get_next_vehicle()
        assert next_vehicle.vehicle_id == "AV-003"

    def test_reservation_priority(self):
        """Test that vehicles with reservations have highest priority."""
        vehicle_normal = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 10.0)
        vehicle_reserved = Vehicle("AV-002", VehicleType.SEDAN, 60.0, 50.0, has_reservation=True)

        self.queue_manager.add_vehicle(vehicle_normal)
        self.queue_manager.add_vehicle(vehicle_reserved)

        # Reserved vehicle should be first despite higher charge level
        next_vehicle = self.queue_manager.get_next_vehicle()
        assert next_vehicle.vehicle_id == "AV-002"
        assert next_vehicle.has_reservation is True

    def test_get_next_vehicle_empty_queue(self):
        """Test getting next vehicle from empty queue."""
        next_vehicle = self.queue_manager.get_next_vehicle()
        assert next_vehicle is None

    def test_peek_next_vehicle(self):
        """Test peeking at next vehicle without removing it."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        self.queue_manager.add_vehicle(vehicle)

        peeked = self.queue_manager.peek_next_vehicle()
        assert peeked.vehicle_id == "AV-001"
        assert self.queue_manager.get_queue_size() == 1  # Still in queue

    def test_remove_specific_vehicle(self):
        """Test removing a specific vehicle from the queue."""
        vehicle1 = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        vehicle2 = Vehicle("AV-002", VehicleType.SEDAN, 60.0, 20.0)

        self.queue_manager.add_vehicle(vehicle1)
        self.queue_manager.add_vehicle(vehicle2)

        result = self.queue_manager.remove_vehicle(vehicle1)
        assert result is True
        assert self.queue_manager.get_queue_size() == 1

    def test_remove_nonexistent_vehicle(self):
        """Test removing a vehicle that's not in the queue."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        result = self.queue_manager.remove_vehicle(vehicle)
        assert result is False

    def test_get_queue_position(self):
        """Test getting position of a vehicle in the queue."""
        vehicle1 = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 50.0)  # Low priority
        vehicle2 = Vehicle("AV-002", VehicleType.SEDAN, 60.0, 10.0)  # High priority

        self.queue_manager.add_vehicle(vehicle1)
        self.queue_manager.add_vehicle(vehicle2)

        # Vehicle2 should be at position 0 (higher priority)
        position2 = self.queue_manager.get_queue_position(vehicle2)
        assert position2 == 0

        # Vehicle1 should be at position 1 (lower priority)
        position1 = self.queue_manager.get_queue_position(vehicle1)
        assert position1 == 1

    def test_get_all_vehicles(self):
        """Test getting all vehicles in priority order."""
        vehicle1 = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        vehicle2 = Vehicle("AV-002", VehicleType.SEDAN, 60.0, 10.0)

        self.queue_manager.add_vehicle(vehicle1)
        self.queue_manager.add_vehicle(vehicle2)

        all_vehicles = self.queue_manager.get_all_vehicles()
        assert len(all_vehicles) == 2
        assert all_vehicles[0].vehicle_id == "AV-002"  # Higher priority first

    def test_vehicle_type_priority(self):
        """Test that vehicle type affects priority."""
        sedan = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        bus = Vehicle("AV-002", VehicleType.BUS, 150.0, 75.0)  # Same 50% charge

        self.queue_manager.add_vehicle(sedan)
        self.queue_manager.add_vehicle(bus)

        # Both at 50%, but bus has higher priority modifier
        next_vehicle = self.queue_manager.get_next_vehicle()
        assert next_vehicle.vehicle_id in ["AV-001", "AV-002"]

    def test_queue_status(self):
        """Test getting queue status information."""
        vehicle = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 30.0)
        self.queue_manager.add_vehicle(vehicle)

        status = self.queue_manager.get_queue_status()
        assert status["queue_size"] == 1
        assert len(status["vehicles"]) == 1
        assert status["vehicles"][0]["vehicle_id"] == "AV-001"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
