"""
Observer Pattern Implementation
Provides base classes for implementing the Observer design pattern.
"""

from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """
    Abstract base class for observers.
    Observers must implement the update method to receive notifications.
    """

    @abstractmethod
    def update(self, message: str) -> None:
        """
        Receive update from subject.

        Args:
            message: Notification message from the subject
        """
        pass


class Subject:
    """
    Subject class that maintains a list of observers and notifies them of changes.
    """

    def __init__(self):
        """Initialize the subject with an empty list of observers."""
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.

        Args:
            observer: Observer to attach
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Observer {observer.__class__.__name__} attached.")

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.

        Args:
            observer: Observer to detach
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Observer {observer.__class__.__name__} detached.")

    def notify(self, message: str) -> None:
        """
        Notify all observers about an event.

        Args:
            message: Message to send to all observers
        """
        print(f"[Subject] Notifying {len(self._observers)} observers: {message}")
        for observer in self._observers:
            observer.update(message)
