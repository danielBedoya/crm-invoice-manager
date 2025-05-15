from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
import logging, re


logger = logging.getLogger("dashboard")


class RoleDashboardView(LoginRequiredMixin, View):
    """
    A Django view that renders a role-based dashboard for users. This view dynamically
    constructs the context based on the user's group memberships and associated field
    permissions. It ensures that users only see the models and fields they are authorized
    to access.

    Methods:
        get(request):
            Handles GET requests to render the dashboard. It builds the context by
            grouping models and fields based on the user's permissions.

        get_context_data(**kwargs):
            Placeholder method for constructing additional context for the role-based
            dashboard. To be implemented with logic for grouping models and fields
            according to `FieldPermission`.
    """

    template_name = "dashboard/role_dashboard.html"

    def get(self, request):
        try:
            user = request.user
            group = user.groups.first()
            normalized_name = re.sub(r"[^a-z0-9]+", "_", group.name.lower())
            context = self.get_context_data(normalized_name=normalized_name)
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error(f"Unexpected error during role-based dashboard rendering: {e}")
            return render(
                request,
                self.template_name,
                {
                    "error": f"Ocurrió un error inesperado al cargar el dashboard por roles: {str(e)}"
                },
            )

    def get_context_data(self, normalized_name=None, **kwargs):
        try:
            app_context_path = f"dashboard.role_context_builders.{normalized_name}"
            module = __import__(app_context_path, fromlist=["get_context"])
            context = module.get_context(self.request.user)

            create_instances = []
            for model in apps.get_models():
                content_type = ContentType.objects.get_for_model(model)
                perm_codename = f"{content_type.app_label}.add_{content_type.model}"
                if self.request.user.has_perm(perm_codename):
                    fields = []
                    for field in model._meta.fields:
                        if not field.auto_created and field.editable:
                            pattern = None
                            if field.choices:
                                field_type = "select"
                                field_choices = [
                                    {"value": choice[0], "label": choice[1]} for choice in field.choices
                                ]
                            elif field.is_relation and hasattr(field, 'remote_field') and field.remote_field.model:
                                field_type = "select"
                                related_model = field.remote_field.model
                                field_choices = [
                                    {"value": obj.pk, "label": str(obj)} for obj in related_model.objects.all()
                                ]
                            elif field.get_internal_type() in ["BooleanField", "NullBooleanField"]:
                                field_type = "checkbox"
                                field_choices = None
                            else:
                                field_type = "text"
                                field_choices = None
                                fname = field.name.lower()
                                if "email" in fname:
                                    field_type = "email"
                                elif "phone" in fname or "telefono" in fname:
                                    field_type = "tel"
                                    pattern = "[0-9]*"
                                elif "date" in fname:
                                    field_type = "date"
                                else:
                                    pattern = None

                            field_dict = {
                                "name": field.name,
                                "label": field.verbose_name.capitalize(),
                                "required": not field.blank,
                                "type": field_type,
                            }
                            if pattern:
                                field_dict["pattern"] = pattern
                            if field_choices:
                                field_dict["choices"] = field_choices

                            fields.append(field_dict)

                    if fields:
                        create_instances.append(
                            {
                                "model": model.__name__,
                                "action": f"{content_type.app_label}:create_{content_type.model}",
                                "nombre_modelo": model._meta.verbose_name.capitalize(),
                                "fields": fields,
                            }
                        )

            if create_instances:
                context["create_instances"] = create_instances

    
            rows = context.get("rows", [])
            paginator = Paginator(rows, context.get("pagination", 20))
            page_number = self.request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context["rows"] = page_obj.object_list
            context["page_obj"] = page_obj
            context["paginator"] = paginator
            context["is_paginated"] = page_obj.has_other_pages()

            return context
        except ImportError:
            logger.warning(f"No context builder found for: {normalized_name}")
            return {"title": "Generic dashboard", "headers": [], "rows": []}
