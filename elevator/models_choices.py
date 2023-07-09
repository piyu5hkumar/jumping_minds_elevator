from django.db import models


class ElevatorDirections(models.TextChoices):
    """Choice class for Elevator Directions"""

    UP = "UP", "UP"
    DOWN = "DOWN", "DOWN"
    IDLE = "IDLE", "IDLE"
