"""
Notification Service
Handles real-time notifications to vehicles and system administrators.
Implements Observer pattern to receive updates from charging station.
"""

from typing import List, Dict
from datetime import datetime
from patterns.observer import Observer


class NotificationService(Observer):
    """
    Service for sending notifications to vehicles and administrators.
    Implements Observer pattern to receive station events.
    """

    def __init__(self, service_id: str):
        """
        Initialize the notification service.

        Args:
            service_id: Unique identifier for this notification service
        """
        self.service_id = service_id
        self.notification_history: List[Dict] = []
        self.notification_channels = ["push", "sms", "email"]

    def update(self, message: str) -> None:
        """
        Receive notification from charging station (Observer pattern).

        Args:
            message: Notification message from the charging station
        """
        self.send_notification(message)

    def send_notification(self, message: str, channel: str = "push") -> None:
        """
        Send a notification through specified channel.

        Args:
            message: Notification message
            channel: Communication channel (push, sms, email)
        """
        if channel not in self.notification_channels:
            print(f"[NotificationService] Invalid channel: {channel}")
            return

        notification = {
            "timestamp": datetime.now(),
            "message": message,
            "channel": channel,
            "service_id": self.service_id,
        }

        self.notification_history.append(notification)

        # Simulate sending notification
        print(f"[NotificationService] [{channel.upper()}] {message}")

    def send_to_vehicle(self, vehicle_id: str, message: str) -> None:
        """
        Send a targeted notification to a specific vehicle.

        Args:
            vehicle_id: ID of the vehicle to notify
            message: Notification message
        """
        targeted_message = f"To Vehicle {vehicle_id}: {message}"
        self.send_notification(targeted_message)

    def send_alert(self, message: str, priority: str = "normal") -> None:
        """
        Send an alert notification with priority level.

        Args:
            message: Alert message
            priority: Priority level (low, normal, high, critical)
        """
        alert_message = f"[{priority.upper()} PRIORITY] {message}"
        self.send_notification(alert_message, "push")

        # For high priority, also send via SMS
        if priority in ["high", "critical"]:
            self.send_notification(alert_message, "sms")

    def get_notification_count(self) -> int:
        """
        Get total number of notifications sent.

        Returns:
            Count of notifications
        """
        return len(self.notification_history)

    def get_recent_notifications(self, count: int = 10) -> List[Dict]:
        """
        Get the most recent notifications.

        Args:
            count: Number of recent notifications to retrieve

        Returns:
            List of recent notification dictionaries
        """
        return self.notification_history[-count:]

    def clear_history(self) -> None:
        """Clear notification history."""
        self.notification_history.clear()
        print(f"[NotificationService] Notification history cleared")

    def get_statistics(self) -> dict:
        """
        Get notification statistics.

        Returns:
            Dictionary containing notification statistics
        """
        channel_counts = {}
        for notification in self.notification_history:
            channel = notification["channel"]
            channel_counts[channel] = channel_counts.get(channel, 0) + 1

        return {
            "service_id": self.service_id,
            "total_notifications": len(self.notification_history),
            "channels_breakdown": channel_counts,
            "available_channels": self.notification_channels,
        }

    def display_statistics(self) -> None:
        """Display notification statistics."""
        stats = self.get_statistics()
        print("\n" + "=" * 60)
        print(f"NOTIFICATION SERVICE - {stats['service_id']}")
        print("=" * 60)
        print(f"Total Notifications Sent: {stats['total_notifications']}")
        print("\nBreakdown by Channel:")
        for channel, count in stats['channels_breakdown'].items():
            print(f"  {channel.upper()}: {count}")
        print(f"\nAvailable Channels: {', '.join(stats['available_channels'])}")
        print("=" * 60 + "\n")

    def display_recent_notifications(self, count: int = 5) -> None:
        """
        Display recent notifications.

        Args:
            count: Number of recent notifications to display
        """
        recent = self.get_recent_notifications(count)
        print("\n" + "=" * 60)
        print(f"RECENT NOTIFICATIONS (Last {min(count, len(recent))})")
        print("=" * 60)

        if not recent:
            print("No notifications yet.")
        else:
            for notification in recent:
                timestamp = notification['timestamp'].strftime("%H:%M:%S")
                channel = notification['channel'].upper()
                message = notification['message']
                print(f"[{timestamp}] [{channel}] {message}")

        print("=" * 60 + "\n")

    def __str__(self) -> str:
        """String representation of the notification service."""
        return f"NotificationService({self.service_id})"

    def __repr__(self) -> str:
        """Detailed representation of the notification service."""
        return self.__str__()
