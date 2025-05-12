from django.db import models


class Vehicle(models.Model):
    """
    Model representing a vehicle.

    This model stores information about a vehicle, including its brand, model,
    license plate, and optional manufacturing year.

    Attributes:
        brand (CharField): The brand of the vehicle (max length: 100).
        model (CharField): The model of the vehicle (max length: 100).
        license_plate (CharField): The unique license plate of the vehicle (max length: 20).
        year (PositiveIntegerField): The manufacturing year of the vehicle (optional).

    Methods:
        __str__(): Returns a string representation of the vehicle, including its brand, model, and license plate.
    """

    brand = models.CharField("Marca", max_length=100)
    model = models.CharField("Modelo", max_length=100)
    license_plate = models.CharField("Placa", max_length=20, unique=True)
    year = models.PositiveIntegerField("Año", blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.license_plate}"
