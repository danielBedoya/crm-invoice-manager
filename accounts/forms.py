from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from .models import FieldPermission

User = get_user_model()


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

    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class CrearUsuarioForm(forms.ModelForm):
    """
    Form for creating a new user.

    This form allows administrators to create a new user by providing their
    email, first name, last name, password, and assigning them to a group.

    Fields:
        email (EmailField): The user's email address.
        first_name (CharField): The user's first name.
        last_name (CharField): The user's last name.
        password (CharField): The user's password.
        group (ModelChoiceField): The group (role) to which the user will be assigned.

    Meta:
        model (User): The user model used for creating a new user.
        fields (list): Specifies the fields to include in the form.

    Methods:
        save(commit=True): Saves the user instance, sets the password, and assigns the user to the selected group.
    """

    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), label="Rol", empty_label="Selecciona un rol"
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            user.groups.add(self.cleaned_data["group"])
        return user


class RolePermissionForm(forms.Form):
    """
    Form for creating or editing roles with specific permissions.

    This form allows administrators to define a role name and assign permissions
    to the role. The permissions are limited to specific models such as 'client',
    'vehicle', 'contract', and 'invoice'.

    Fields:
        name (CharField): The name of the role.
        permissions (ModelMultipleChoiceField): A list of permissions associated with the role.

    Methods:
        __init__(*args, **kwargs): Initializes the form and filters the permissions
        to include only those related to the allowed models.
    """

    rol_name = forms.CharField(label="Nombre del rol", max_length=100)
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Permisos",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        allowed_models = ["client", "vehicle", "contract", "invoice"]
        content_types = ContentType.objects.filter(model__in=allowed_models)
        self.fields["permissions"].queryset = Permission.objects.filter(
            content_type__in=content_types
        )

    def get_permissions_grouped_by_model(self):
        model_name_map = {
            "client": "Cliente",
            "vehicle": "Vehículo",
            "contract": "Contrato",
            "invoice": "Factura",
        }
        grouped = {}

        for perm in self.fields["permissions"].queryset:
            raw_name = perm.content_type.model  # ej: 'client'
            visible_name = model_name_map.get(raw_name, raw_name.title())

            if visible_name not in grouped:
                grouped[visible_name] = {"model_name": raw_name, "permissions": []}

            grouped[visible_name]["permissions"].append(perm)

        return grouped
