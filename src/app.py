"""
Flask Web Application for Autonomous Vehicle Charging Station
"""

from flask import Flask, render_template, jsonify, request
import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from models.vehicle import Vehicle, VehicleType
from models.charging_slot import ChargingSlot
from models.charging_station import ChargingStation
from services.queue_manager import QueueManager
from services.billing_service import BillingService
from services.notification_service import NotificationService
from services.reservation_service import ReservationService

app = Flask(__name__)

# Initialize the charging station and services (global for demo)
station = ChargingStation("CS-001", "Downtown Tech Hub")
station.add_slot(ChargingSlot("SLOT-A", 50.0))
station.add_slot(ChargingSlot("SLOT-B", 50.0))
station.add_slot(ChargingSlot("SLOT-C", 150.0))

queue_manager = QueueManager()
billing_service = BillingService()
notification_service = NotificationService("NS-001")
reservation_service = ReservationService()

station.attach(notification_service)


@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')


@app.route('/api/station/status')
def get_station_status():
    """Get current charging station status"""
    status = station.get_station_status()
    return jsonify(status)


@app.route('/api/queue/status')
def get_queue_status():
    """Get current queue status"""
    vehicles = queue_manager.get_all_vehicles()
    
    queue_data = {
        'total': len(vehicles),
        'vehicles': [
            {
                'id': v.vehicle_id,
                'type': v.vehicle_type.name,
                'battery': round(v.get_charge_percentage(), 1),
                'priority': v.calculate_priority()
            }
            for v in vehicles
        ]
    }
    return jsonify(queue_data)


@app.route('/api/vehicle/add', methods=['POST'])
def add_vehicle():
    """Add a new vehicle to the station"""
    data = request.json
    
    vehicle_type = VehicleType[data['type'].upper()]
    vehicle = Vehicle(
        vehicle_id=data['id'],
        vehicle_type=vehicle_type,
        battery_capacity=float(data.get('capacity', 60.0)),
        current_charge=float(data.get('battery', 20.0))
    )
    
    # Try to assign to a slot
    slot = station.assign_vehicle_to_slot(vehicle)
    
    if slot:
        return jsonify({
            'success': True,
            'message': f'Vehicle {vehicle.vehicle_id} assigned to {slot.slot_id}',
            'slot': slot.slot_id
        })
    else:
        # Add to queue
        position = queue_manager.add_vehicle(vehicle)
        return jsonify({
            'success': True,
            'message': f'Vehicle {vehicle.vehicle_id} added to queue',
            'queue_position': position
        })


@app.route('/api/vehicle/remove/<vehicle_id>', methods=['POST'])
def remove_vehicle(vehicle_id):
    """Remove a vehicle from station or queue"""
    # Try to release from slot
    for slot in station.slots:
        if slot.current_vehicle and slot.current_vehicle.vehicle_id == vehicle_id:
            station.release_vehicle(slot)
            return jsonify({
                'success': True,
                'message': f'Vehicle {vehicle_id} released from slot'
            })
    
    # Try to remove from queue
    vehicle_to_remove = None
    for _, _, vehicle in queue_manager._queue:
        if vehicle.vehicle_id == vehicle_id:
            vehicle_to_remove = vehicle
            break
    
    if vehicle_to_remove and queue_manager.remove_vehicle(vehicle_to_remove):
        return jsonify({
            'success': True,
            'message': f'Vehicle {vehicle_id} removed from queue'
        })
    
    return jsonify({
        'success': False,
        'message': f'Vehicle {vehicle_id} not found'
    }), 404


@app.route('/api/billing/stats')
def get_billing_stats():
    """Get billing statistics"""
    stats = billing_service.get_revenue_stats()
    return jsonify(stats)


@app.route('/api/slots')
def get_slots():
    """Get all charging slots with current status"""
    slots_data = []
    for slot in station.slots:
        slot_info = {
            'id': slot.slot_id,
            'power': slot.power_rating,
            'available': slot.is_available,
            'vehicle': None
        }
        if slot.current_vehicle:
            slot_info['vehicle'] = {
                'id': slot.current_vehicle.vehicle_id,
                'type': slot.current_vehicle.vehicle_type.name,
                'battery': round(slot.current_vehicle.get_charge_percentage(), 1)
            }
        slots_data.append(slot_info)
    
    return jsonify(slots_data)


@app.route('/api/charge/<slot_id>', methods=['POST'])
def charge_vehicle(slot_id):
    """Simulate charging for a specific duration"""
    data = request.json
    duration = float(data.get('duration', 0.5))  # hours
    
    station.process_charging(duration)
    
    return jsonify({
        'success': True,
        'message': f'Charged for {duration} hours'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)