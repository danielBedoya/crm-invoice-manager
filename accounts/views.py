from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.urls import reverse_lazy

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
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    """
    Custom logout view for handling user logout.

    This view redirects users to the login page after logging out.

    Attributes:
        next_page (str): URL to redirect to after logout.
    """
    next_page = reverse_lazy('login')
