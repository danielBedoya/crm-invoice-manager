from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.views.generic.edit import FormView
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict
import logging

from accounts.forms import RolePermissionForm
from clients.models import Client
from vehicles.models import Vehicle, VehicleModel
from contracts.models import Contract
from invoices.models import Invoice
from accounts.models import FieldPermission

logger = logging.getLogger(__name__)


class CreateAdvancedRoleView(FormView):
    """
    A view for creating advanced roles with specific permissions and field-level access.
    This view handles the creation of roles (Django Groups) with associated permissions
    and field-level access control. It provides a form for users to specify the role name,
    permissions, and allowed fields for the role. The view also manages the saving of
    these configurations and provides feedback to the user.
    Attributes:
        template_name (str): The path to the template used for rendering the form.
        form_class (Form): The form class used for role creation.
        success_url (str): The URL to redirect to upon successful form submission.
    Methods:
        __save_field_permissions(allowed_fields, group):
            Saves field-level permissions for a given group.
        form_valid(form):
            Handles the logic for processing a valid form submission.
        form_invalid(form):
            Handles the logic for processing an invalid form submission.
        get_context_data(**kwargs):
            Prepares and returns the context data for rendering the template.
    """

    template_name = "accounts/create_advanced_rol.html"
    form_class = RolePermissionForm
    success_url = reverse_lazy("create_advanced_rol")

    def __save_field_permissions(self, allowed_fields, group):
        try:
            fields_by_model = defaultdict(list)

            for full_field in allowed_fields:
                model_name, field_name = full_field.split("__", 1)
                fields_by_model[model_name].append(field_name)

            for model_name, fields in fields_by_model.items():
                content_type = ContentType.objects.get(model=model_name)
                field_permission, _ = FieldPermission.objects.get_or_create(
                    group=group, content_type=content_type
                )
                field_permission.set_allowed_fields(fields)
                field_permission.save()
                logger.info(
                    f"Permissions for model '{model_name}' saved for role '{group.name}'"
                )
        except Exception as e:
            logger.error(
                f"Error saving field permissions for group '{group.name}': {e}"
            )
            raise

    def form_valid(self, form):
        try:
            group, created = Group.objects.get_or_create(
                name=form.cleaned_data["rol_name"]
            )
            group.permissions.set(form.cleaned_data["permissions"])
            self.__save_field_permissions(
                self.request.POST.getlist("allowed_fields"), group
            )
            messages.success(self.request, "Role created successfully.")
            logger.info(f"Role '{group.name}' created successfully.")
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in form validation: {e}")
            messages.error(self.request, "There was an error creating the role.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.warning("Form invalid while creating role.")
        messages.error(
            self.request, "There are errors in the form. Please fix them and try again."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        try:
            models_list = [Client, Vehicle, Contract, Invoice, VehicleModel]
            context = super().get_context_data(**kwargs)
            context["field_options"] = {
                model._meta.model_name: [
                    field.name for field in model._meta.get_fields()
                ]
                for model in models_list
            }
            context["roles"] = Group.objects.all()
            context["field_permissions"] = {}

            for role in context["roles"]:
                field_permissions = FieldPermission.objects.filter(group=role)
                if not field_permissions.exists():
                    continue
                context["field_permissions"][role] = {
                    field_permissions.first()
                    .content_type.model: field_permissions.first()
                    .get_allowed_fields(),
                }
            logger.info("Roles and field permissions loaded successfully.")
            return context
        except Exception as e:
            logger.error(f"Error loading context data: {e}")
            return super().get_context_data(**kwargs)


class DeleteRoleView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View to handle the deletion of a role (Django Group).
    This view ensures that only superusers can delete roles and prevents the deletion
    of roles that have users assigned to them. If a role is successfully deleted,
    associated field permissions are also removed.
    Methods:
        test_func(): Checks if the current user is a superuser.
        post(request, *args, **kwargs): Handles the deletion of a role via a POST request.
    """

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        try:
            group_id = kwargs.get("pk")
            group = get_object_or_404(Group, pk=group_id)
            if group.user_set.exists():
                messages.error(request, "You cannot delete a role with users assigned.")
                logger.warning(
                    f"Attempt to delete role '{group.name}' with users assigned."
                )
            else:
                FieldPermission.objects.filter(group=group).delete()
                group.delete()
                messages.success(request, "Role deleted successfully.")
                logger.info(f"Role '{group.name}' deleted successfully.")
            return redirect("create_advanced_rol")
        except Exception as e:
            logger.error(f"Error deleting role: {e}")
            messages.error(request, "There was an error deleting the role.")
            return redirect("create_advanced_rol")
