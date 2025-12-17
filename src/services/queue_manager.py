"""
Queue Manager Service
Manages priority queue for vehicles waiting for charging slots.
"""

import heapq
from typing import List, Optional
from models.vehicle import Vehicle


class QueueManager:
    """
    Manages a priority queue of vehicles waiting for charging slots.
    Uses heap data structure for efficient priority-based operations.
    """

    def __init__(self):
        """Initialize the queue manager with an empty priority queue."""
        self._queue: List[tuple] = []  # List of (priority, counter, vehicle) tuples
        self._counter = 0  # Counter to break ties and maintain FIFO for same priority
        self._vehicle_positions = {}  # Track vehicle positions for quick lookup

    def add_vehicle(self, vehicle: Vehicle) -> int:
        """
        Add a vehicle to the priority queue.

        Args:
            vehicle: Vehicle to add to the queue

        Returns:
            Position in the queue (0-indexed)
        """
        priority = vehicle.calculate_priority()
        heapq.heappush(self._queue, (priority, self._counter, vehicle))
        self._vehicle_positions[vehicle.vehicle_id] = self._counter
        self._counter += 1

        position = self.get_queue_position(vehicle)
        print(f"[QueueManager] Added {vehicle.vehicle_id} to queue at position {position}")
        return position

    def get_next_vehicle(self) -> Optional[Vehicle]:
        """
        Get and remove the next vehicle from the queue (highest priority).

        Returns:
            Next vehicle in queue, or None if queue is empty
        """
        if not self._queue:
            return None

        _, counter, vehicle = heapq.heappop(self._queue)
        if vehicle.vehicle_id in self._vehicle_positions:
            del self._vehicle_positions[vehicle.vehicle_id]

        print(f"[QueueManager] Removed {vehicle.vehicle_id} from queue")
        return vehicle

    def peek_next_vehicle(self) -> Optional[Vehicle]:
        """
        Look at the next vehicle without removing it from the queue.

        Returns:
            Next vehicle in queue, or None if queue is empty
        """
        if not self._queue:
            return None

        return self._queue[0][2]

    def get_queue_position(self, vehicle: Vehicle) -> int:
        """
        Get the current position of a vehicle in the queue.

        Args:
            vehicle: Vehicle to find

        Returns:
            Position in queue (0-indexed), or -1 if not found
        """
        if vehicle.vehicle_id not in self._vehicle_positions:
            return -1

        target_counter = self._vehicle_positions[vehicle.vehicle_id]

        # Find position by counting vehicles ahead
        position = 0
        for priority, counter, _ in self._queue:
            if counter == target_counter:
                return position
            position += 1

        return -1

    def remove_vehicle(self, vehicle: Vehicle) -> bool:
        """
        Remove a specific vehicle from the queue (e.g., if it leaves).

        Args:
            vehicle: Vehicle to remove

        Returns:
            True if vehicle was removed, False if not found
        """
        if vehicle.vehicle_id not in self._vehicle_positions:
            return False

        # Find and remove the vehicle
        for i, (priority, counter, v) in enumerate(self._queue):
            if v.vehicle_id == vehicle.vehicle_id:
                self._queue.pop(i)
                heapq.heapify(self._queue)
                del self._vehicle_positions[vehicle.vehicle_id]
                print(f"[QueueManager] Removed {vehicle.vehicle_id} from queue")
                return True

        return False

    def get_queue_size(self) -> int:
        """
        Get the current size of the queue.

        Returns:
            Number of vehicles in queue
        """
        return len(self._queue)

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        Returns:
            True if queue is empty, False otherwise
        """
        return len(self._queue) == 0

    def get_all_vehicles(self) -> List[Vehicle]:
        """
        Get list of all vehicles in the queue, in priority order.

        Returns:
            List of vehicles sorted by priority
        """
        return [vehicle for _, _, vehicle in sorted(self._queue)]

    def get_queue_status(self) -> dict:
        """
        Get detailed status of the queue.

        Returns:
            Dictionary containing queue statistics
        """
        vehicles = self.get_all_vehicles()

        return {
            "queue_size": len(vehicles),
            "vehicles": [
                {
                    "vehicle_id": v.vehicle_id,
                    "vehicle_type": v.vehicle_type.display_name,
                    "charge_percentage": v.get_charge_percentage(),
                    "priority": v.calculate_priority(),
                    "has_reservation": v.has_reservation,
                }
                for v in vehicles
            ],
        }

    def display_queue(self) -> None:
        """Print the current state of the queue."""
        print("\n" + "=" * 60)
        print("QUEUE STATUS")
        print("=" * 60)
        print(f"Total vehicles in queue: {self.get_queue_size()}")

        if self.is_empty():
            print("Queue is empty.")
        else:
            print("\nVehicles in queue (priority order):")
            for i, vehicle in enumerate(self.get_all_vehicles(), 1):
                print(
                    f"  {i}. {vehicle.vehicle_id} - {vehicle.vehicle_type.display_name} "
                    f"(Battery: {vehicle.get_charge_percentage():.1f}%, "
                    f"Priority: {vehicle.calculate_priority()})"
                )

        print("=" * 60 + "\n")

    def __str__(self) -> str:
        """String representation of the queue manager."""
        return f"QueueManager(size={self.get_queue_size()})"

    def __repr__(self) -> str:
        """Detailed representation of the queue manager."""
        return self.__str__()
