"""
Main Application
Demonstrates the Autonomous Vehicle Charging Station system.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

import time
from datetime import datetime, timedelta
from models.vehicle import Vehicle, VehicleType
from models.charging_slot import ChargingSlot
from models.charging_station import ChargingStation
from services.queue_manager import QueueManager
from services.billing_service import BillingService
from services.notification_service import NotificationService
from services.reservation_service import ReservationService


def simulate_charging_scenario():
    """
    Simulate a complete charging station scenario with multiple vehicles.
    Demonstrates all system features including Observer pattern.
    """
    print("\n" + "=" * 80)
    print(" AUTONOMOUS VEHICLE CHARGING STATION MANAGEMENT SYSTEM")
    print("=" * 80 + "\n")

    # Initialize the charging station
    station = ChargingStation("CS-001", "Downtown Tech Hub")

    # Add charging slots
    station.add_slot(ChargingSlot("SLOT-A", 50.0))  # 50 kW fast charger
    station.add_slot(ChargingSlot("SLOT-B", 50.0))  # 50 kW fast charger
    station.add_slot(ChargingSlot("SLOT-C", 150.0)) # 150 kW ultra-fast charger
    print()

    # Initialize services
    queue_manager = QueueManager()
    billing_service = BillingService()
    notification_service = NotificationService("NS-001")
    reservation_service = ReservationService()

    # Attach notification service to station (Observer pattern)
    station.attach(notification_service)

    # Display initial pricing
    billing_service.display_pricing()

    # Create autonomous vehicles with different states
    print("Creating autonomous vehicles...\n")

    vehicle1 = Vehicle("AV-001", VehicleType.SEDAN, 60.0, 15.0)  # 25% charge
    vehicle2 = Vehicle("AV-002", VehicleType.SUV, 80.0, 10.0)    # 12.5% charge - Critical!
    vehicle3 = Vehicle("AV-003", VehicleType.TRUCK, 100.0, 50.0) # 50% charge
    vehicle4 = Vehicle("AV-004", VehicleType.BUS, 150.0, 30.0)   # 20% charge

    # Vehicle 5 has a reservation
    vehicle5 = Vehicle("AV-005", VehicleType.SEDAN, 60.0, 20.0, has_reservation=True)
    reservation_time = datetime.now() + timedelta(minutes=5)
    reservation_service.create_reservation(vehicle5, reservation_time, 1.5)

    print(f"\nCreated vehicles:")
    for vehicle in [vehicle1, vehicle2, vehicle3, vehicle4, vehicle5]:
        print(f"  - {vehicle}")

    print("\n" + "-" * 80)
    print(" SCENARIO: Multiple vehicles arrive at charging station")
    print("-" * 80 + "\n")

    # Display initial station status
    station.display_status()

    # Scenario 1: First three vehicles arrive and request charging
    print("\n>>> Vehicle AV-001 arrives and requests charging...")
    slot1 = station.assign_vehicle_to_slot(vehicle1)

    print("\n>>> Vehicle AV-002 arrives and requests charging...")
    slot2 = station.assign_vehicle_to_slot(vehicle2)

    print("\n>>> Vehicle AV-003 arrives and requests charging...")
    slot3 = station.assign_vehicle_to_slot(vehicle3)

    print("\n>>> Vehicle AV-004 arrives but all slots are occupied...")
    slot4 = station.assign_vehicle_to_slot(vehicle4)
    if slot4 is None:
        print("No slots available. Adding to queue...")
        queue_manager.add_vehicle(vehicle4)

    print("\n>>> Vehicle AV-005 (with reservation) arrives...")
    slot5 = station.assign_vehicle_to_slot(vehicle5)
    if slot5 is None:
        print("No slots available. Adding to priority queue (has reservation)...")
        queue_manager.add_vehicle(vehicle5)

    # Display queue status
    queue_manager.display_queue()

    # Display station status after all vehicles arrived
    station.display_status()

    # Scenario 2: Simulate charging process
    print("\n" + "-" * 80)
    print(" SCENARIO: Charging in progress")
    print("-" * 80 + "\n")

    print(">>> Simulating 30 minutes of charging...")
    station.process_charging(duration_hours=0.5)

    print("\n>>> Another 30 minutes of charging...")
    station.process_charging(duration_hours=0.5)

    # Scenario 3: First vehicle completes charging
    print("\n" + "-" * 80)
    print(" SCENARIO: Vehicle completes charging and leaves")
    print("-" * 80 + "\n")

    print(">>> Vehicle AV-001 has completed charging...")
    completed_vehicle = station.release_vehicle(slot1)

    if completed_vehicle:
        # Calculate billing
        duration = (completed_vehicle.charging_end_time - 
                   completed_vehicle.charging_start_time).total_seconds() / 3600
        power_consumed = slot1.total_power_consumed

        invoice = billing_service.generate_invoice(
            completed_vehicle,
            duration,
            power_consumed,
            is_peak_hour=True
        )

        # Process payment
        billing_service.process_payment(completed_vehicle, invoice.total_cost)
        station.total_revenue += invoice.total_cost

        print(f"\n  Invoice Details:")
        print(f"    Duration: {duration:.2f} hours")
        print(f"    Power Consumed: {power_consumed:.2f} kWh")
        print(f"    Total Cost: ${invoice.total_cost:.2f}")

    # Process queue - assign next vehicle
    print("\n>>> Processing queue for next vehicle...")
    if not queue_manager.is_empty():
        next_vehicle = queue_manager.get_next_vehicle()
        if next_vehicle:
            print(f"Assigning {next_vehicle.vehicle_id} to available slot...")
            station.assign_vehicle_to_slot(next_vehicle)

    # Display updated status
    station.display_status()
    queue_manager.display_queue()

    # Scenario 4: Display all statistics
    print("\n" + "-" * 80)
    print(" SYSTEM STATISTICS")
    print("-" * 80 + "\n")

    # Billing statistics
    revenue_stats = billing_service.get_revenue_stats()
    print("Billing Statistics:")
    print(f"  Total Revenue: ${revenue_stats['total_revenue']:.2f}")
    print(f"  Invoices Generated: {revenue_stats['invoices_generated']}")
    print(f"  Average per Invoice: ${revenue_stats['average_per_invoice']:.2f}")

    # Notification statistics
    print()
    notification_service.display_statistics()

    # Reservation statistics
    reservation_stats = reservation_service.get_statistics()
    print("Reservation Statistics:")
    print(f"  Total Reservations: {reservation_stats['total_reservations']}")
    print(f"  Active Reservations: {reservation_stats['active_reservations']}")
    print(f"  Fulfilled Reservations: {reservation_stats['fulfilled_reservations']}")
    print()

    # Recent notifications
    notification_service.display_recent_notifications(count=10)

    # Final station status
    print("\n" + "-" * 80)
    print(" FINAL STATION STATUS")
    print("-" * 80 + "\n")
    station.display_status()

    print("\n" + "=" * 80)
    print(" SIMULATION COMPLETE")
    print("=" * 80 + "\n")

    print("Key Features Demonstrated:")
    print("  ✓ Observer Pattern - Real-time notifications to vehicles and services")
    print("  ✓ Priority Queue Management - Based on battery level and reservations")
    print("  ✓ Dynamic Slot Allocation - Automatic assignment of available slots")
    print("  ✓ Billing Service - Automated cost calculation and payment processing")
    print("  ✓ Reservation System - Advanced booking for autonomous fleets")
    print("  ✓ Real-time Monitoring - Charging status and station utilization")
    print()


def main():
    """Main entry point for the application."""
    try:
        simulate_charging_scenario()
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        raise


if __name__ == "__main__":
    main()
