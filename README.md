# Autonomous Vehicle Charging Station Management System

## Project Overview
A comprehensive management system for autonomous vehicle charging stations that handles vehicle queuing, charging slot allocation, real-time monitoring, and billing operations.

## Real-Life Problem Statement
With the rapid adoption of autonomous electric vehicles, charging infrastructure faces critical challenges:
- **High demand during peak hours** leading to long wait times
- **Inefficient charging slot allocation** causing underutilization
- **Lack of predictive scheduling** for autonomous fleet vehicles
- **Complex billing** for different vehicle types and charging speeds
- **Need for real-time monitoring** of charging status and station health

This system addresses these challenges by providing intelligent queue management, dynamic slot allocation, and automated billing for autonomous vehicle fleets.

## Features
- **Intelligent Queue Management**: Priority-based queue for different vehicle types
- **Dynamic Slot Allocation**: Optimizes charging station utilization
- **Real-time Monitoring**: Track charging status, power consumption, and station health
- **Automated Billing**: Calculate costs based on charging time, power consumed, and vehicle type
- **Reservation System**: Allow autonomous vehicles to reserve charging slots in advance
- **Notification System**: Alert vehicles when charging is complete or slots are available

## Technology Stack
- **Language**: Python 3.11+
- **Design Pattern**: Observer Pattern (for real-time notifications)
- **Version Control**: Git & GitHub
- **Containerization**: Docker
- **Testing**: pytest

## Project Structure
```
AutonomousVehicleChargingStation/
├── src/
│   ├── models/
│   │   ├── vehicle.py
│   │   ├── charging_slot.py
│   │   └── charging_station.py
│   ├── services/
│   │   ├── queue_manager.py
│   │   ├── billing_service.py
│   │   └── notification_service.py
│   ├── patterns/
│   │   └── observer.py
│   └── main.py
├── tests/
│   ├── test_queue_manager.py
│   ├── test_billing_service.py
│   └── test_charging_station.py
├── diagrams/
│   ├── use_case_diagram.puml
│   ├── class_diagram.puml
│   ├── activity_diagram.puml
│   └── sequence_diagram.puml
├── docs/
│   └── design_documentation.md
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Git
- Docker (for containerization)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/AutonomousVehicleChargingStation.git
cd AutonomousVehicleChargingStation
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
cd C:\Users\hp\Documents\AutonomousVehicleChargingStation; python src/app.py
```

### Running Tests
```bash
cd C:\Users\hp\Documents\AutonomousVehicleChargingStation; python -m pytest tests/ -v
```

### Docker Deployment
```bash
# Build the Docker image
docker build -t av-charging-station .

# Run the container
docker run -p 8000:8000 av-charging-station
```

## Design Pattern: Observer Pattern
This project implements the **Observer Pattern** to handle real-time notifications:
- **Subject**: ChargingStation (notifies observers about state changes)
- **Observers**: Vehicles, NotificationService (receive updates)
- **Benefits**: Loose coupling, scalable notification system

## Testing Strategy
- **Unit Tests**: Test individual components (queue manager, billing service)
- **Integration Tests**: Test interactions between components
- **Test Coverage**: Aim for >80% code coverage
## Best Practices 

I followed Google's Python coding standards:

- Clear naming conventions: descriptive variable and function names
- Type hints: all functions have proper type annotations
- Docstrings: every class and method has documentation
- Modular structure: separated concerns into models, services, and patterns
- SOLID principles: Single responsibility, Open/closed, Dependency inversion
- Clean code: no magic numbers, proper error handling, consistent formatting


## Coding Standards
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Write docstrings for all classes and functions
- Keep functions focused and under 50 lines

## Version Control
- Git is used for version control
- Feature branch workflow
- Meaningful commit messages following conventional commit


## License
MIT License
