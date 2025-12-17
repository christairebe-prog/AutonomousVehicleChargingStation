"""
Reservation Service
Manages charging slot reservations for autonomous vehicles.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from models.vehicle import Vehicle


class Reservation:
    """Represents a charging slot reservation."""

    def __init__(
        self,
        reservation_id: str,
        vehicle_id: str,
        reserved_time: datetime,
        duration_hours: float,
    ):
        """
        Initialize a reservation.

        Args:
            reservation_id: Unique identifier for the reservation
            vehicle_id: ID of the vehicle making the reservation
            reserved_time: Time slot reserved
            duration_hours: Expected charging duration in hours
        """
        self.reservation_id = reservation_id
        self.vehicle_id = vehicle_id
        self.reserved_time = reserved_time
        self.duration_hours = duration_hours
        self.created_at = datetime.now()
        self.is_active = True
        self.is_fulfilled = False

    def is_expired(self) -> bool:
        """
        Check if reservation has expired (15 minutes grace period after reserved time).

        Returns:
            True if expired, False otherwise
        """
        grace_period = timedelta(minutes=15)
        return datetime.now() > (self.reserved_time + grace_period)

    def __str__(self) -> str:
        """String representation of the reservation."""
        return (
            f"Reservation {self.reservation_id}: Vehicle {self.vehicle_id} "
            f"at {self.reserved_time.strftime('%Y-%m-%d %H:%M')}"
        )


class ReservationService:
    """
    Service for managing charging slot reservations.
    Allows vehicles to reserve slots in advance.
    """

    def __init__(self):
        """Initialize the reservation service."""
        self._reservation_counter = 0
        self.reservations: Dict[str, Reservation] = {}
        self.vehicle_reservations: Dict[str, str] = {}  # vehicle_id -> reservation_id

    def create_reservation(
        self,
        vehicle: Vehicle,
        reserved_time: datetime,
        duration_hours: float = 1.0,
    ) -> Optional[str]:
        """
        Create a new reservation for a vehicle.

        Args:
            vehicle: Vehicle making the reservation
            reserved_time: Desired time slot
            duration_hours: Expected charging duration

        Returns:
            Reservation ID if successful, None if vehicle already has reservation
        """
        # Check if vehicle already has an active reservation
        if vehicle.vehicle_id in self.vehicle_reservations:
            existing_id = self.vehicle_reservations[vehicle.vehicle_id]
            if existing_id in self.reservations and self.reservations[existing_id].is_active:
                print(
                    f"[ReservationService] Vehicle {vehicle.vehicle_id} "
                    f"already has an active reservation"
                )
                return None

        # Create new reservation
        self._reservation_counter += 1
        reservation_id = f"RES-{self._reservation_counter:06d}"

        reservation = Reservation(
            reservation_id=reservation_id,
            vehicle_id=vehicle.vehicle_id,
            reserved_time=reserved_time,
            duration_hours=duration_hours,
        )

        self.reservations[reservation_id] = reservation
        self.vehicle_reservations[vehicle.vehicle_id] = reservation_id
        vehicle.has_reservation = True

        print(
            f"[ReservationService] Created reservation {reservation_id} "
            f"for {vehicle.vehicle_id} at {reserved_time.strftime('%Y-%m-%d %H:%M')}"
        )
        return reservation_id

    def cancel_reservation(self, reservation_id: str) -> bool:
        """
        Cancel a reservation.

        Args:
            reservation_id: ID of the reservation to cancel

        Returns:
            True if cancelled successfully, False if not found
        """
        if reservation_id not in self.reservations:
            print(f"[ReservationService] Reservation {reservation_id} not found")
            return False

        reservation = self.reservations[reservation_id]
        reservation.is_active = False

        # Remove from vehicle reservations
        if reservation.vehicle_id in self.vehicle_reservations:
            del self.vehicle_reservations[reservation.vehicle_id]

        print(f"[ReservationService] Cancelled reservation {reservation_id}")
        return True

    def check_reservation(self, vehicle: Vehicle) -> Optional[Reservation]:
        """
        Check if a vehicle has an active reservation.

        Args:
            vehicle: Vehicle to check

        Returns:
            Reservation object if active reservation exists, None otherwise
        """
        if vehicle.vehicle_id not in self.vehicle_reservations:
            return None

        reservation_id = self.vehicle_reservations[vehicle.vehicle_id]
        reservation = self.reservations.get(reservation_id)

        if reservation and reservation.is_active and not reservation.is_expired():
            return reservation

        return None

    def fulfill_reservation(self, reservation_id: str) -> bool:
        """
        Mark a reservation as fulfilled when vehicle starts charging.

        Args:
            reservation_id: ID of the reservation to fulfill

        Returns:
            True if fulfilled successfully, False if not found
        """
        if reservation_id not in self.reservations:
            return False

        reservation = self.reservations[reservation_id]
        reservation.is_fulfilled = True
        reservation.is_active = False

        print(f"[ReservationService] Fulfilled reservation {reservation_id}")
        return True

    def cleanup_expired_reservations(self) -> int:
        """
        Remove expired reservations.

        Returns:
            Number of expired reservations removed
        """
        expired_count = 0

        for reservation_id, reservation in list(self.reservations.items()):
            if reservation.is_active and reservation.is_expired():
                self.cancel_reservation(reservation_id)
                expired_count += 1

        if expired_count > 0:
            print(f"[ReservationService] Cleaned up {expired_count} expired reservations")

        return expired_count

    def get_active_reservations(self) -> list:
        """
        Get all active reservations.

        Returns:
            List of active Reservation objects
        """
        return [
            reservation
            for reservation in self.reservations.values()
            if reservation.is_active and not reservation.is_expired()
        ]

    def get_statistics(self) -> dict:
        """
        Get reservation statistics.

        Returns:
            Dictionary containing reservation statistics
        """
        active_reservations = self.get_active_reservations()
        fulfilled_count = sum(
            1 for r in self.reservations.values() if r.is_fulfilled
        )

        return {
            "total_reservations": len(self.reservations),
            "active_reservations": len(active_reservations),
            "fulfilled_reservations": fulfilled_count,
        }

    def display_reservations(self) -> None:
        """Display all active reservations."""
        active = self.get_active_reservations()

        print("\n" + "=" * 60)
        print("ACTIVE RESERVATIONS")
        print("=" * 60)
        print(f"Total Active: {len(active)}")

        if not active:
            print("No active reservations.")
        else:
            print("\nReservation Details:")
            for reservation in sorted(active, key=lambda r: r.reserved_time):
                print(f"  {reservation}")
                print(f"    Duration: {reservation.duration_hours} hours")
                print(f"    Created: {reservation.created_at.strftime('%Y-%m-%d %H:%M')}")

        print("=" * 60 + "\n")

    def __str__(self) -> str:
        """String representation of the reservation service."""
        return f"ReservationService(active={len(self.get_active_reservations())})"

    def __repr__(self) -> str:
        """Detailed representation of the reservation service."""
        return self.__str__()
