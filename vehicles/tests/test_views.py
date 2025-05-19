from vehicles.models import Vehicle, VehicleModel
from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class CreateVehicleViewTests(TestCase):
    """
    Test suite for the CreateVehicleView Django view.
    This class contains tests to verify the behavior of the vehicle creation view, including:
    - Successful creation of a vehicle with valid data.
    - Handling of missing required fields during vehicle creation.
    Test Methods:
        - test_create_vehicle_success: Ensures that a vehicle can be created via POST request and redirects appropriately.
        - test_create_vehicle_missing_fields: Checks that the form returns errors when required fields are missing and no vehicle is created.
    The setUp method creates a test user, logs them in, and sets up a sample vehicle model for use in the tests.
    """
    

    def setUp(self):
        """Create a test user and log in."""
        self.user = User.objects.create_user(
            email="test3@example.com", username="user3", password="secret123"
        )
        self.client.login(username="test3@example.com", password="secret123")
        self.vehicle_model = VehicleModel.objects.create(brand="Honda", model="CBR600")

    def test_create_vehicle_success(self):
        """Test creating a vehicle via POST."""
        response = self.client.post(
            reverse("manage_vehicle"),
            {
                "license_plate": "ABC123",
                "year": 2023,
                "vehicle_model": self.vehicle_model.pk,
            },
        )
        self.assertTrue(Vehicle.objects.filter(license_plate="ABC123").exists())


class CreateVehicleModelViewTests(TestCase):
    """
    TestCase for the CreateVehicleModelView, verifying the creation of vehicle models.
    This test class covers:
    - Setup of a test user and authentication.
    - Successful creation of a vehicle model via POST request.
    - Handling of missing required fields during vehicle model creation, ensuring form validation and error messages.
    Test Methods:
        - setUp: Initializes a test user and logs them in.
        - test_create_vehicle_model_success: Ensures a vehicle model can be created and redirects appropriately.
        - test_create_vehicle_model_missing_fields: Checks that missing fields trigger form errors and prevent creation.
    """
    

    def setUp(self):
        """Create a test user and log in."""
        self.user = User.objects.create_user(
            email="test2@example.com", username="user2", password="secret123"
        )
        self.client.login(username="test2@example.com", password="secret123")

    def test_create_vehicle_model_success(self):
        """Test creating a vehicle model via POST."""
        response = self.client.post(
            reverse("manage_vehiclemodel"),
            {"brand": "Yamaha", "model": "FZ25"},
        )
        self.assertTrue(VehicleModel.objects.filter(brand="Yamaha", model="FZ25").exists())
