"""Init file for models package."""
from .vehicle import Vehicle, VehicleType
from .charging_slot import ChargingSlot
from .charging_station import ChargingStation

__all__ = ['Vehicle', 'VehicleType', 'ChargingSlot', 'ChargingStation']
