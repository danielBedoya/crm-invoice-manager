from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class LoginViewTests(TestCase):
    """Unit tests for the login view functionality."""

    def setUp(self):
        """Create a test user for login attempts."""
        logger.info("Setting up test user for LoginViewTests")
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="secret123"
        )

    def test_login_page_loads(self):
        """Test that the login page loads correctly."""
        logger.info("Running test_login_page_loads")
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Iniciar Sesión")
        logger.info("test_login_page_loads passed")

    def test_login_success(self):
        """Test successful login with valid credentials."""
        logger.info("Running test_login_success")
        response = self.client.post(
            reverse("login"), {"username": "test@example.com", "password": "secret123"}
        )
        self.assertRedirects(response, "/")  # Assumes LOGIN_REDIRECT_URL = '/'
        logger.info("test_login_success passed")

    def test_login_failure(self):
        """Test login failure with invalid credentials."""
        logger.info("Running test_login_failure")
        response = self.client.post(
            reverse("login"), {"username": "wrong@example.com", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Por favor, introduzca un email y clave correctos."
        )
        logger.info("test_login_failure passed")
