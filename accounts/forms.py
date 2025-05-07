from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
    """
    Custom login form for user authentication.

    This form overrides the default AuthenticationForm to use email as the
    username field and applies custom styling to the input fields.

    Fields:
        username (EmailField): The user's email address, used as the username.
        password (CharField): The user's password.

    Meta:
        model (User): The user model used for authentication.
        fields (list): Specifies the fields to include in the form.
    """
    
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']