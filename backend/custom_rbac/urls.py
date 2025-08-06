from django.urls import path

from .views import AccessRolesRuleView, BusinessElementView, RoleView

urlpatterns = [
    path("roles/", RoleView.as_view(), name="roles"),
    path("elements/", BusinessElementView.as_view(), name="business-element"),
    path("access-roles/", AccessRolesRuleView.as_view(), name="access-roles"),
]
