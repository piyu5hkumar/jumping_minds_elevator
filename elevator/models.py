from django.db import models
from elevator.models_choices import ElevatorDirections
from uuid import uuid4
from utils.models import BasicModel


class Elevator(BasicModel):
    """Model class for Elevator"""

    serial_number = models.UUIDField(default=uuid4)
    number = models.PositiveIntegerField(null=True, db_index=True)
    is_operational = models.BooleanField(default=True)
    is_running = models.BooleanField(default=False)
    current_floor = models.IntegerField(default=0)
    destination_floor = models.IntegerField(null=True)
    is_maintenance = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    direction = models.CharField(
        max_length=20,
        choices=ElevatorDirections.choices,
        default=ElevatorDirections.IDLE,
    )

    def __repr__(self) -> str:
        return f"Elevator {self.pk}"


class UserRequest(BasicModel):
    """Model class for UserRequest"""

    elevator = models.ForeignKey(
        Elevator, on_delete=models.CASCADE, related_name="user_requests", null=True
    )
    floor = models.IntegerField()
    is_completed = models.BooleanField(default=False)  # Will be updated from celery

    def __repr__(self) -> str:
        return f"Request for Elevator {self.elevator.number} to Floor {self.floor}"
