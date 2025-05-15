from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
import logging

from accounts.forms import CrearUsuarioForm

User = get_user_model()


class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View for creating a new user.

    This view allows superusers to create new users using a form. It ensures
    that only authenticated superusers can access this functionality.

    Attributes:
        template_name (str): Path to the template used for the user creation page.
        form_class (CrearUsuarioForm): The form class used for creating a new user.
        success_url (str): The URL to redirect to upon successful user creation.

    Methods:
        test_func(): Ensures that the current user is a superuser.
    """

    model = User
    template_name = "accounts/create_user.html"
    form_class = CrearUsuarioForm
    success_url = reverse_lazy("create_user")
    context_object_name = "users"

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        try:
            if not form.instance.username:
                form.instance.username = form.cleaned_data["email"]

            response = super().form_valid(form)
            messages.success(self.request, "Usuario creado exitosamente.")
            logging.info(f"Usuario creado: {form.instance.email}")
            return response
        except Exception as e:
            logging.exception(f"Error creating user: {e}")
            messages.error(self.request, f"Ocurrió un error al crear el usuario. {e}")
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        logging.warning("Formulario de creación de usuario inválido.")
        for field, errors in form.errors.items():
            for error in errors:
                logging.warning(f"Error in field {form.fields[field].label}: {error}")
                messages.error(self.request, f"{form.fields[field].label}: {error}")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["users"] = self.model.objects.all()
            logging.info(f"Listed users: {context['users'].count()}")
        except Exception as e:
            logging.exception(f"Error listing users: {e}")
        return context


class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View for deleting a user.

    This view allows superusers to delete users. It ensures that only
    authenticated superusers can perform this action.

    Methods:
        post(request, pk): Handles the deletion of a user with the given primary key (pk).
        test_func(): Ensures that the current user is a superuser.
    """

    def post(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            if not user.is_superuser:
                user.delete()
                messages.success(request, "Usuario eliminado.")
                logging.info(f"User {user.email} deleted.")
            else:
                messages.error(request, "No puedes eliminar un superusuario.")
                logging.warning(f"Trying to delete a super user: {user.email}")
            return redirect("create_user")
        except Exception as e:
            logging.exception(f"Error deleting user with id {pk}: {e}")
            messages.error(request, "Ocurrió un error al eliminar el usuario.")
            return redirect("create_user")

    def test_func(self):
        return self.request.user.is_superuser
