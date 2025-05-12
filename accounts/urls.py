from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CreateUserView,
    CreateAdvancedRoleView,
    DeleteRoleView,
    DeleteUserView
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("create-user/", CreateUserView.as_view(), name="create_user"),
    path(
        "create-advanced-rol/",
        CreateAdvancedRoleView.as_view(),
        name="create_advanced_rol",
    ),
    path('roles/<int:pk>/delete/', DeleteRoleView.as_view(), name='delete_role'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
]
