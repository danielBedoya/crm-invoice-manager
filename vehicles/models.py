import uuid
from django.db import models


class VehicleModel(models.Model):
    """
    Model representing a vehicle model and brand.

    Attributes:
        brand (CharField): The brand of the vehicle (max length: 100).
        model (CharField): The model of the vehicle (max length: 100).
    """
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    brand = models.CharField("Marca", max_length=100)
    model = models.CharField("Modelo", max_length=100)

    def __str__(self):
        return f"{self.brand} {self.model}"
    

class Vehicle(models.Model):
    """
    Model representing a vehicle.

    This model stores information about a vehicle, including its brand, model,
    license plate, and optional manufacturing year.

    Attributes:
        uid (UUIDField): A unique identifier for the vehicle (auto-generated).
        brand (CharField): The brand of the vehicle (max length: 100).
        model (CharField): The model of the vehicle (max length: 100).
        license_plate (CharField): The unique license plate of the vehicle (max length: 20).
        year (PositiveIntegerField): The manufacturing year of the vehicle (optional).

    Methods:
        __str__(): Returns a string representation of the vehicle, including its brand, model, and license plate.
    """
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, verbose_name="Marca y modelo")
    license_plate = models.CharField("Placa", max_length=20, unique=True)
    year = models.PositiveIntegerField("Año", blank=True, null=True)

    def __str__(self):
        return f"{self.vehicle_model} - {self.license_plate}"
