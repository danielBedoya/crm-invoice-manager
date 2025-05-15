from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
import logging

from accounts.forms import LoginForm

logger = logging.getLogger("accounts")


class CustomLoginView(LoginView):
    """
    Custom login view for handling user authentication.

    This view uses a custom login form and redirects authenticated users
    to the appropriate page.

    Attributes:
        template_name (str): Path to the template used for the login page.
        authentication_form (LoginForm): The custom form used for authentication.
        redirect_authenticated_user (bool): Whether to redirect already authenticated users.
    """

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Log successful login and proceed with normal behavior."""
        user = form.get_user()
        logger.info(f"User logged in successfully: {user.email}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Log failed login attempt and return invalid form response."""
        logger.warning("Invalid login attempt.")
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy("dashboard")
        return reverse_lazy("role_dashboard")


class CustomLogoutView(LogoutView):
    """
    Custom logout view for handling user logout.

    This view redirects users to the login page after logging out.

    Attributes:
        next_page (str): URL to redirect to after logout.
    """

    next_page = reverse_lazy("login")