from django.urls import path

from .views import AccessRolesRuleView, BusinessElementView, RoleDetailView, RoleView

urlpatterns = [
    path("roles/", RoleView.as_view(), name="roles"),
    path("roles/<int:role_id>/", RoleDetailView.as_view(), name="roles"),
    path("elements/", BusinessElementView.as_view(), name="business-element"),
    path("access-roles/", AccessRolesRuleView.as_view(), name="access-roles"),
]
